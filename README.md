# Image Converter Pro

Image Converter Pro is a powerful, standalone desktop application built with Python and Tkinter. It allows you to easily batch convert, resize, crop, edit, and watermark images with a simple and modern user interface.

## Features

* **Multi-Format Support**: Convert between popular image formats including PNG, JPEG, WEBP, BMP, GIF, TIFF, ICO, PDF, EPS, and PPM.
* **Batch Processing**: Convert entire folders of images at once, with an option to recursively process subfolders.
* **Format Auto-Detection**: Keep the original image format using the "Same as Source" option.
* **Resize & Crop**: 
  * Scale images by percentage.
  * Resize to exact dimensions (Width x Height).
  * Crop images perfectly to the center square.
* **Transformations & Filters**:
  * Rotate (90°, 180°) and Flip (Horizontal, Vertical) images.
  * Apply basic filters like Blur, Sharpen, Contour, Emboss, and Edge Enhance.
  * Convert images to Grayscale.
* **Adjustments**: Fine-tune Brightness, Contrast, and Sharpness.
* **Watermarking**: Instantly stamp custom text onto your images.
* **Advanced Output Options**:
  * Batch rename files with custom Prefixes and Suffixes.
  * Preserve original EXIF metadata.
  * Enable Lossless mode for WEBP format.
  * Option to automatically delete original files after a successful conversion.

## How to Run (Python)

If you have Python installed, you can run the application directly from the source code.

### Prerequisites

You must have the `Pillow` library installed.

```bash
pip install pillow
```

### Running the App

```bash
python image_converter.py
```

## How to Build the Executable (.exe)

You can compile the script into a standalone `.exe` file that works on any Windows PC without requiring Python to be installed.

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the application:
   ```bash
   python -m PyInstaller --noconsole --onefile image_converter.py
   ```
3. The executable will be generated inside the `dist` folder (`dist/image_converter.exe`).
