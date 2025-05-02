import os
import tkinter as tk
from tkinter import messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image

# Supported image types
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')

def compress_image(input_path, quality):
    try:
        img = Image.open(input_path)
        img_format = img.format
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_compressed{ext}"

        if img_format in ['JPEG', 'JPG', 'WEBP']:
            img.save(output_path, format=img_format, quality=quality, optimize=True)
        elif img_format == 'PNG':
            img.save(output_path, format='PNG', optimize=True)
        elif img_format in ['BMP', 'TIFF']:
            # Convert to JPEG to actually compress
            output_path = f"{base}_compressed.jpg"
            img = img.convert("RGB")
            img.save(output_path, format='JPEG', quality=quality, optimize=True)
        else:
            return f"Unsupported format: {os.path.basename(input_path)}"

        original_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        return f"{os.path.basename(input_path)}: {original_size//1024}KB → {new_size//1024}KB"
    except Exception as e:
        return f"Error with {os.path.basename(input_path)}: {e}"

def handle_drop(event):
    file_list = root.tk.splitlist(event.data)
    messages = []
    quality = int(quality_slider.get())
    for file in file_list:
        ext = os.path.splitext(file)[1].lower()
        if os.path.isfile(file) and ext in SUPPORTED_FORMATS:
            result = compress_image(file, quality)
            messages.append(result)
        else:
            messages.append(f"Skipped: {os.path.basename(file)} (unsupported format)")
    messagebox.showinfo("Compression Complete", "\n".join(messages))

# GUI Setup
root = TkinterDnD.Tk()
root.title("Image Compressor")
root.geometry("400x250")
root.resizable(False, False)

# Drop Area
drop_label = tk.Label(root, text="Drag & Drop Images Here", font=("Arial", 14),
                      relief="ridge", borderwidth=2)
drop_label.pack(expand=True, fill="both", padx=20, pady=(20, 10))

drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind('<<Drop>>', handle_drop)

# Slider Area
slider_frame = tk.Frame(root)
slider_frame.pack(fill="x", padx=20, pady=(0, 10))

tk.Label(slider_frame, text="Compression Quality:").pack(anchor="w")

quality_slider = ttk.Scale(slider_frame, from_=10, to=95, orient="horizontal")
quality_slider.set(75)
quality_slider.pack(fill="x")

# Quality Value Display
def update_quality_label(event=None):
    current_value_label.config(text=f"{int(quality_slider.get())}%")

current_value_label = tk.Label(slider_frame, text="75%")
current_value_label.pack(anchor="e")
quality_slider.bind("<Motion>", update_quality_label)
quality_slider.bind("<ButtonRelease-1>", update_quality_label)

# Run GUI
root.mainloop()
