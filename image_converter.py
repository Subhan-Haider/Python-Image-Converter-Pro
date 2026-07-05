import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter Pro")
        self.root.geometry("600x700")
        self.root.configure(padx=20, pady=20)
        
        # Variables
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.target_format = tk.StringVar(value="Same as Source")
        self.input_filter = tk.StringVar(value="All Supported")
        self.delete_original = tk.BooleanVar(value=False)
        self.process_subfolders = tk.BooleanVar(value=False)
        
        # Transform & Enhance
        self.grayscale = tk.BooleanVar(value=False)
        self.rotate = tk.StringVar(value="None")
        self.flip = tk.StringVar(value="None")
        self.watermark_text = tk.StringVar(value="")
        self.filter_mode = tk.StringVar(value="None")
        
        # Adjustments
        self.brightness = tk.DoubleVar(value=1.0)
        self.contrast = tk.DoubleVar(value=1.0)
        self.sharpness = tk.DoubleVar(value=1.0)
        
        # Output Settings
        self.quality = tk.IntVar(value=85)
        self.prefix = tk.StringVar(value="")
        self.suffix = tk.StringVar(value="")
        self.preserve_exif = tk.BooleanVar(value=False)
        self.webp_lossless = tk.BooleanVar(value=False)
        
        # Resize & Crop
        self.resize_mode = tk.StringVar(value="Percentage")
        self.resize_percent = tk.StringVar(value="100")
        self.resize_width = tk.StringVar(value="")
        self.resize_height = tk.StringVar(value="")
        self.crop_center = tk.BooleanVar(value=False)
        
        # Style
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10))
        style.configure("TLabel", font=("Arial", 10))
        
        # Folders UI
        ttk.Label(root, text="Input Folder:").pack(anchor="w", pady=(0, 2))
        input_frame = ttk.Frame(root)
        input_frame.pack(fill="x", pady=(0, 10))
        ttk.Entry(input_frame, textvariable=self.input_folder, state='readonly').pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="Browse", command=self.browse_input).pack(side="right")
        
        ttk.Label(root, text="Output Folder:").pack(anchor="w", pady=(0, 2))
        output_frame = ttk.Frame(root)
        output_frame.pack(fill="x", pady=(0, 15))
        ttk.Entry(output_frame, textvariable=self.output_folder, state='readonly').pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="Browse", command=self.browse_output).pack(side="right")
        
        # Settings Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, pady=(0, 15))
        
        # Tab 1: Format & Output
        tab_format = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_format, text="Output")
        
        ttk.Label(tab_format, text="Input Filter:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Combobox(tab_format, textvariable=self.input_filter, values=["All Supported", "PNG", "JPEG", "WEBP", "BMP", "GIF", "TIFF", "ICO", "PDF", "EPS", "PPM"], state="readonly", width=18).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(tab_format, text="Target Format:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Combobox(tab_format, textvariable=self.target_format, values=["Same as Source", "PNG", "JPEG", "WEBP", "BMP", "GIF", "TIFF", "ICO", "PDF", "EPS", "PPM"], state="readonly", width=18).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(tab_format, text="Quality (JPEG/WEBP):").grid(row=2, column=0, sticky="w", pady=5)
        q_frame = ttk.Frame(tab_format)
        q_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        ttk.Scale(q_frame, from_=1, to=100, variable=self.quality, orient="horizontal", length=120).pack(side="left")
        ttk.Label(q_frame, textvariable=self.quality).pack(side="left", padx=(5,0))
        
        ttk.Label(tab_format, text="Rename (Pre/Suffix):").grid(row=3, column=0, sticky="w", pady=5)
        r_frame = ttk.Frame(tab_format)
        r_frame.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        ttk.Entry(r_frame, textvariable=self.prefix, width=10).pack(side="left", padx=(0, 5))
        ttk.Entry(r_frame, textvariable=self.suffix, width=10).pack(side="left")
        
        # Tab 2: Resize & Crop
        tab_resize = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_resize, text="Resize")
        
        ttk.Radiobutton(tab_resize, text="By Percentage (%)", variable=self.resize_mode, value="Percentage").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(tab_resize, textvariable=self.resize_percent, width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Radiobutton(tab_resize, text="Exact Dimensions (W x H)", variable=self.resize_mode, value="Exact").grid(row=1, column=0, sticky="w", pady=5)
        dim_frame = ttk.Frame(tab_resize)
        dim_frame.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Entry(dim_frame, textvariable=self.resize_width, width=6).pack(side="left")
        ttk.Label(dim_frame, text="x").pack(side="left", padx=2)
        ttk.Entry(dim_frame, textvariable=self.resize_height, width=6).pack(side="left")
        
        ttk.Checkbutton(tab_resize, text="Crop to Center Square", variable=self.crop_center).grid(row=2, column=0, columnspan=2, sticky="w", pady=15)
        
        # Tab 3: Transform & Enhance
        tab_enhance = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_enhance, text="Transform")
        
        ttk.Label(tab_enhance, text="Rotate:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Combobox(tab_enhance, textvariable=self.rotate, values=["None", "90 Left", "90 Right", "180"], state="readonly", width=15).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(tab_enhance, text="Flip:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Combobox(tab_enhance, textvariable=self.flip, values=["None", "Horizontal", "Vertical"], state="readonly", width=15).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(tab_enhance, text="Text Watermark:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(tab_enhance, textvariable=self.watermark_text, width=25).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(tab_enhance, text="Image Filter:").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Combobox(tab_enhance, textvariable=self.filter_mode, values=["None", "Blur", "Contour", "Detail", "Edge Enhance", "Sharpen", "Emboss"], state="readonly", width=15).grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Checkbutton(tab_enhance, text="Convert to Grayscale", variable=self.grayscale).grid(row=4, column=0, columnspan=2, sticky="w", pady=10)
        
        # Tab 4: Adjustments
        tab_adj = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_adj, text="Adjust")
        
        def reset_adj():
            self.brightness.set(1.0)
            self.contrast.set(1.0)
            self.sharpness.set(1.0)
            
        ttk.Label(tab_adj, text="Brightness:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Scale(tab_adj, from_=0.0, to=2.0, variable=self.brightness, orient="horizontal", length=150).grid(row=0, column=1, padx=5)
        
        ttk.Label(tab_adj, text="Contrast:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Scale(tab_adj, from_=0.0, to=2.0, variable=self.contrast, orient="horizontal", length=150).grid(row=1, column=1, padx=5)
        
        ttk.Label(tab_adj, text="Sharpness:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Scale(tab_adj, from_=0.0, to=2.0, variable=self.sharpness, orient="horizontal", length=150).grid(row=2, column=1, padx=5)
        
        ttk.Button(tab_adj, text="Reset to Normal", command=reset_adj).grid(row=3, column=0, columnspan=2, pady=10)

        # Tab 5: Advanced
        tab_adv = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_adv, text="Advanced")
        
        ttk.Checkbutton(tab_adv, text="Process Subfolders (Recursive)", variable=self.process_subfolders).grid(row=0, column=0, sticky="w", pady=5)
        ttk.Checkbutton(tab_adv, text="Delete Original File after Conversion", variable=self.delete_original).grid(row=1, column=0, sticky="w", pady=5)
        ttk.Checkbutton(tab_adv, text="Preserve EXIF Metadata", variable=self.preserve_exif).grid(row=2, column=0, sticky="w", pady=5)
        ttk.Checkbutton(tab_adv, text="WEBP Lossless Mode", variable=self.webp_lossless).grid(row=3, column=0, sticky="w", pady=5)
        
        # Convert Button
        self.convert_btn = tk.Button(root, text="Convert Images", command=self.convert_images, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="flat", cursor="hand2")
        self.convert_btn.pack(fill="x", ipady=10, pady=(5, 10))
        
        # Status Label
        self.status_label = ttk.Label(root, text="Ready to convert", foreground="gray")
        self.status_label.pack()

        # Definitions
        self.ext_map = {
            "PNG": [".png"], "JPEG": [".jpg", ".jpeg"], "WEBP": [".webp"], 
            "BMP": [".bmp"], "GIF": [".gif"], "TIFF": [".tiff", ".tif"], 
            "ICO": [".ico"], "PDF": [".pdf"], "EPS": [".eps"], "PPM": [".ppm", ".pbm", ".pgm", ".pnm"]
        }
        self.all_exts = [ext for exts in self.ext_map.values() for ext in exts]

    def browse_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder.set(folder)
            if not self.output_folder.get(): self.output_folder.set(folder)

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder: self.output_folder.set(folder)

    def get_files_to_convert(self, input_dir):
        files = []
        filter_val = self.input_filter.get()
        valid_exts = tuple(self.all_exts) if filter_val == "All Supported" else tuple(self.ext_map.get(filter_val, []))
            
        if self.process_subfolders.get():
            for root, _, filenames in os.walk(input_dir):
                for f in filenames:
                    if f.lower().endswith(valid_exts):
                        files.append(os.path.join(root, f))
        else:
            for f in os.listdir(input_dir):
                if f.lower().endswith(valid_exts):
                    files.append(os.path.join(input_dir, f))
        return files

    def convert_images(self):
        input_dir, output_dir = self.input_folder.get(), self.output_folder.get()
        
        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Please select both input and output folders.")
            return
            
        files_to_convert = self.get_files_to_convert(input_dir)
        if not files_to_convert:
            messagebox.showinfo("Info", "No matching images found in the input folder.")
            return
            
        self.convert_btn.config(state="disabled", text="Converting...")
        self.status_label.config(text=f"Converting 0 of {len(files_to_convert)} files...", foreground="black")
        self.root.update()
        
        success_count, error_count = 0, 0
        t_format_choice = self.target_format.get()
        prefix, suffix = self.prefix.get(), self.suffix.get()
        
        for i, img_path in enumerate(files_to_convert):
            try:
                img = Image.open(img_path)
                exif_data = img.info.get('exif') if self.preserve_exif.get() else None
                
                # Determine target format
                if t_format_choice == "Same as Source":
                    if img.format:
                        current_fmt = img.format.lower()
                        t_format = 'jpeg' if current_fmt == 'jpeg' else current_fmt
                    else:
                        ext = os.path.splitext(img_path)[1].lower()
                        t_format = ext[1:] if ext else 'png'
                else:
                    t_format = t_format_choice.lower()
                
                # Crop to Center Square
                if self.crop_center.get():
                    width, height = img.size
                    new_dim = min(width, height)
                    left = (width - new_dim) / 2
                    top = (height - new_dim) / 2
                    right = (width + new_dim) / 2
                    bottom = (height + new_dim) / 2
                    img = img.crop((left, top, right, bottom))
                
                # Resize
                mode = self.resize_mode.get()
                if mode == "Percentage":
                    scale_pct = float(self.resize_percent.get())
                    if scale_pct != 100.0:
                        new_w = int(img.width * (scale_pct / 100.0))
                        new_h = int(img.height * (scale_pct / 100.0))
                        if new_w > 0 and new_h > 0:
                            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                elif mode == "Exact":
                    w_str, h_str = self.resize_width.get(), self.resize_height.get()
                    if w_str and h_str and w_str.isdigit() and h_str.isdigit():
                        img = img.resize((int(w_str), int(h_str)), Image.Resampling.LANCZOS)
                
                # Adjustments (Brightness, Contrast, Sharpness)
                b_val = self.brightness.get()
                if b_val != 1.0: img = ImageEnhance.Brightness(img).enhance(b_val)
                c_val = self.contrast.get()
                if c_val != 1.0: img = ImageEnhance.Contrast(img).enhance(c_val)
                s_val = self.sharpness.get()
                if s_val != 1.0: img = ImageEnhance.Sharpness(img).enhance(s_val)

                # Rotate & Flip
                rot, flp = self.rotate.get(), self.flip.get()
                if rot == "90 Left": img = img.rotate(90, expand=True)
                elif rot == "90 Right": img = img.rotate(-90, expand=True)
                elif rot == "180": img = img.rotate(180, expand=True)
                    
                if flp == "Horizontal": img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                elif flp == "Vertical": img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                    
                # Grayscale
                if self.grayscale.get():
                    img = img.convert("L")
                    
                # Filters
                filt = self.filter_mode.get()
                if filt == "Blur": img = img.filter(ImageFilter.BLUR)
                elif filt == "Contour": img = img.filter(ImageFilter.CONTOUR)
                elif filt == "Detail": img = img.filter(ImageFilter.DETAIL)
                elif filt == "Edge Enhance": img = img.filter(ImageFilter.EDGE_ENHANCE)
                elif filt == "Sharpen": img = img.filter(ImageFilter.SHARPEN)
                elif filt == "Emboss": img = img.filter(ImageFilter.EMBOSS)
                    
                # Add Watermark
                watermark = self.watermark_text.get()
                if watermark:
                    draw = ImageDraw.Draw(img)
                    w, h = img.size
                    text_x = max(10, w - 100) # Fallback
                    text_y = max(10, h - 30)
                    draw.text((text_x, text_y), watermark, fill=(255, 255, 255, 128))
                
                # Pre-processing for formats
                if t_format in ['jpeg', 'jpg', 'pdf', 'eps'] and img.mode in ('RGBA', 'P', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode in ('RGBA', 'LA'):
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                    
                # Setup output path
                rel_path = os.path.relpath(os.path.dirname(img_path), input_dir)
                target_dir = output_dir if rel_path == "." else os.path.join(output_dir, rel_path)
                os.makedirs(target_dir, exist_ok=True)
                    
                name, orig_ext = os.path.splitext(os.path.basename(img_path))
                out_ext = ".jpg" if t_format == 'jpeg' else (orig_ext if t_format_choice == "Same as Source" else f".{t_format}")
                
                output_path = os.path.join(target_dir, f"{prefix}{name}{suffix}{out_ext}")
                
                # Save Options
                save_kwargs = {}
                if t_format in ['jpeg', 'jpg', 'webp']: save_kwargs['quality'] = self.quality.get()
                if t_format == 'webp' and self.webp_lossless.get(): save_kwargs['lossless'] = True
                if exif_data: save_kwargs['exif'] = exif_data
                
                save_fmt = 'JPEG' if t_format.upper() == 'JPG' else t_format.upper()
                img.save(output_path, format=save_fmt, **save_kwargs)
                success_count += 1
                
                # Delete original
                if self.delete_original.get() and os.path.abspath(img_path) != os.path.abspath(output_path):
                    img.close()
                    os.remove(img_path)
                    
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
                error_count += 1
                
            self.status_label.config(text=f"Converting {i+1} of {len(files_to_convert)} files...")
            self.root.update()
            
        self.status_label.config(text="Conversion Complete!", foreground="green")
        self.convert_btn.config(state="normal", text="Convert Images")
        
        msg = f"Successfully converted {success_count} images."
        if error_count > 0: msg += f"\nFailed to convert {error_count} images (see console)."
        messagebox.showinfo("Success", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
