import os
from PIL import Image

source = "icon.png"
out_dir = "StoreAssets"
os.makedirs(out_dir, exist_ok=True)
img = Image.open(source)

# Helper to paste centered icon on a dark background
def create_centered_logo(size, icon_size, filename):
    bg = Image.new("RGBA", size, (45, 45, 45, 255)) # Dark gray background
    scaled = img.resize(icon_size, Image.Resampling.LANCZOS)
    bg.paste(scaled, ((size[0]-icon_size[0])//2, (size[1]-icon_size[1])//2), scaled if scaled.mode == 'RGBA' else None)
    bg.save(os.path.join(out_dir, filename))

# 9:16 Poster Art (720x1080)
create_centered_logo((720, 1080), (400, 400), "9_16_PosterArt.png")

# 1:1 Box Art (1080x1080)
create_centered_logo((1080, 1080), (600, 600), "1_1_BoxArt.png")

# 1:1 App tile icon (300x300)
create_centered_logo((300, 300), (200, 200), "1_1_AppTile.png")

print("Updated Microsoft Store assets generated successfully!")
