import os
import re
import gc
import traceback
from PIL import Image

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def process_volumes_safe(base_dir):
    vol_folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    vol_folders.sort(key=natural_sort_key)

    if not vol_folders:
        print("⚠️ 未找到任何 VOL 資料夾，請確認路徑！")
        return

    print(f"🔍 找到 {len(vol_folders)} 個 VOL 資料夾，開始處理...\n")

    for vol in vol_folders:
        vol_path = os.path.join(base_dir, vol)
        output_pdf_path = os.path.join(base_dir, f"{vol}.pdf")

        # 1. 搜集該 Volume 下的所有圖片路徑
        ch_folders = [f for f in os.listdir(vol_path) if os.path.isdir(os.path.join(vol_path, f))]
        ch_folders.sort(key=natural_sort_key)

        image_files = []
        if ch_folders:
            for ch in ch_folders:
                ch_path = os.path.join(vol_path, ch)
                files = [os.path.join(ch_path, f) for f in os.listdir(ch_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
                files.sort(key=natural_sort_key)
                image_files.extend(files)
        else:
            files = [os.path.join(vol_path, f) for f in os.listdir(vol_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            files.sort(key=natural_sort_key)
            image_files.extend(files)

        if not image_files:
            print(f"⚠️ 跳過 {vol}（找不到圖片）")
            continue

        print(f"📦 處理中 [{vol}]: 共有 {len(image_files)} 張圖片...")

        try:
            # 2. 開啟第一張圖片並強制載入像素數據
            first_img = Image.open(image_files[0])
            first_img.load()
            if first_img.mode != 'RGB':
                first_img = first_img.convert('RGB')

            # 3. 逐張載入像素並轉換（既省 RAM，又不會過早關閉檔案）
            def image_stream():
                for img_path in image_files[1:]:
                    try:
                        img = Image.open(img_path)
                        img.load()  # 強制將圖片像素寫入記憶體，防止檔案被意外關閉
                        if img.mode != 'RGB':
                            conv_img = img.convert('RGB')
                            img.close()
                            yield conv_img
                        else:
                            yield img
                    except Exception as img_err:
                        print(f"❌ 讀取單張圖片失敗: {img_path}, 錯誤: {img_err}")

            # 4. 寫入 PDF
            first_img.save(
                output_pdf_path,
                "PDF",
                save_all=True,
                append_images=image_stream()
            )
            
            first_img.close()
            print(f"✅ 成功生成: {vol}.pdf\n")

        except Exception as e:
            print(f"❌ 處理 {vol} 時出錯: {e}")
            traceback.print_exc()  # 印出詳細報錯訊息，方便排查
            print()

        # 5. 手動釋放記憶體
        gc.collect()

    print("🎉 所有 Volume 已處理完畢！")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    process_volumes_safe(current_dir)