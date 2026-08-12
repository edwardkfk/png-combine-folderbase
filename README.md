# PNG Folder to PDF Converter

A lightweight and memory-efficient Python script designed to scan image folders, naturally sort image files (PNG/JPG/WEBP), and convert each target folder into an individual PDF file.

---

## 🌟 Key Features

- **Folder-Based Batch Processing**: Converts each subfolder in the root directory into its own dedicated PDF.
- **Nested Directory Support**: Handles both multi-tiered structures (e.g., Volume -> Chapter -> PNG) and flat structures (e.g., Volume -> PNG).
- **Natural Sorting**: Correctly sequences numerical filenames (e.g., 1, 2, 10 instead of 1, 10, 2).
- **Low RAM/VRAM Stream Handling**: Uses image streaming (`Image.load()` + generators) and garbage collection to process hundreds of high-res images safely without exhausting System RAM/VRAM or causing BSOD crashes.
- **Auto RGB Conversion**: Automatically converts RGBA / transparent PNGs to standard RGB for PDF compatibility.

---

## 📁 Directory Structure Example

Place `build_volumes.py` in the root folder containing your image subfolders:

```text
My_Images_Folder/
├── Volume_01/
│   ├── Chapter_01/
│   │   ├── 001.png
│   │   └── 002.png
│   └── Chapter_02/
│       └── 001.png
├── Volume_02/
│   ├── page1.jpg
│   └── page2.jpg
└── build_volumes.py

```
Running the script will generate:
- Volume_01.pdf
- Volume_02.pdf

---

## 🚀 Usage Guide

### 1. Prerequisites
Ensure Python 3.x is installed, then install the Pillow library via terminal/command prompt:

pip install Pillow

### 2. Script Placement
Copy build_volumes.py into the main directory containing your image subfolders.

### 3. Execution
Open Command Prompt / Terminal, navigate to your directory, and run:

cd "path/to/your/main/folder"
python build_volumes.py

---

## 💡 Advanced Usage (Custom Target Path)

If you prefer not to move build_volumes.py around, you can specify an absolute target directory directly inside the script:

if __name__ == "__main__":
    # Specify your target absolute folder path here
    target_dir = r"C:\Users\fung_\Downloads\Target_Images"
    process_volumes_safe(target_dir)
