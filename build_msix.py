import os
import shutil
import subprocess
from PIL import Image

build_dir = "msix_build"
os.makedirs(build_dir, exist_ok=True)

# 1. Copy EXE
shutil.copy(r"dist\ImageConverterStudio.exe", os.path.join(build_dir, "ImageConverterStudio.exe"))

# 2. Generate required MSIX icons
icon_src = "icon.png"
img = Image.open(icon_src)

def create_icon(size, name):
    bg = Image.new("RGBA", size, (0, 0, 0, 0)) # Transparent
    scaled = img.resize((int(size[0]*0.8), int(size[1]*0.8)), Image.Resampling.LANCZOS)
    bg.paste(scaled, ((size[0]-scaled.width)//2, (size[1]-scaled.height)//2), scaled if scaled.mode == 'RGBA' else None)
    bg.save(os.path.join(build_dir, name))

create_icon((50, 50), "StoreLogo.png")
create_icon((150, 150), "Square150x150Logo.png")
create_icon((44, 44), "Square44x44Logo.png")
create_icon((310, 150), "Wide310x150Logo.png")

# 3. Create AppxManifest.xml
manifest = """<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
         xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
         IgnorableNamespaces="uap rescap">

  <Identity Name="SubhanStore.ImageConverterStudio"
            Publisher="CN=033AC539-6559-4258-97EB-6268BC2B6B91"
            Version="1.0.0.0" 
            ProcessorArchitecture="x64"/>

  <Properties>
    <DisplayName>Image Converter Studio</DisplayName>
    <PublisherDisplayName>S. Tech Studio</PublisherDisplayName>
    <Logo>StoreLogo.png</Logo>
  </Properties>

  <Resources>
    <Resource Language="en-us"/>
  </Resources>

  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.17763.0" MaxVersionTested="10.0.19041.0"/>
  </Dependencies>

  <Capabilities>
    <rescap:Capability Name="runFullTrust"/>
  </Capabilities>

  <Applications>
    <Application Id="App"
                 Executable="ImageConverterStudio.exe"
                 EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements DisplayName="Image Converter Studio"
                          Description="Bulk convert, resize, and watermark images."
                          BackgroundColor="transparent"
                          Square150x150Logo="Square150x150Logo.png"
                          Square44x44Logo="Square44x44Logo.png">
        <uap:DefaultTile Wide310x150Logo="Wide310x150Logo.png" />
      </uap:VisualElements>
    </Application>
  </Applications>
</Package>
"""
with open(os.path.join(build_dir, "AppxManifest.xml"), "w", encoding="utf-8") as f:
    f.write(manifest)

# 4. Run makeappx.exe
makeappx_path = r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\makeappx.exe"
cmd = f'"{makeappx_path}" pack -d {build_dir} -p ImageConverterStudio.msix -o'
print(f"Running: {cmd}")
try:
    result = subprocess.run(cmd, check=True, shell=True, capture_output=True, text=True)
    print(result.stdout)
    print("Successfully built ImageConverterStudio.msix!")
except subprocess.CalledProcessError as e:
    print("Error packaging MSIX:")
    print(e.stderr)
