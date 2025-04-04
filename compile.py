import os
import sys
import subprocess
import platform
from PIL import Image

def get_resource_path(filename):
    """Get the correct path for images and resources when running as an EXE."""
    if getattr(sys, 'frozen', False):  # Running as EXE
        return os.path.join(sys._MEIPASS, filename)
    return filename  # Running as script

def convert_png_to_ico():
    """Convert logo.png to a multi-size .ico file"""
    if not os.path.exists("logo.ico"):
        try:
            img = Image.open(get_resource_path("logo.png"))
            img.save("logo.ico", sizes=[(256, 256), (64, 64), (32, 32), (16, 16)])
            print("✅ Converted logo.png to logo.ico")
            return True
        except Exception as e:
            print(f"❌ Failed to convert logo: {e}")
            return False
    return True

def compile_all_in_one():
    """Compile all Python files into one .exe"""
    
    # Use `;` for Windows, `:` for Linux/Mac
    sep = ";" if platform.system() == "Windows" else ":"

    # Ensure 'dist' folder exists
    os.makedirs("dist", exist_ok=True)

    print("🔨 Combining all files into one executable...")

    try:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile", "--windowed",
            "--icon=logo.ico",
            f"--add-data=logo.png{sep}.",  # ✅ Include images
            f"--add-data=creds.json{sep}.",  # ✅ Include JSON
            f"--add-data=panels{sep}panels" if os.path.exists("panels") else "",
            f"--add-data=components{sep}components" if os.path.exists("components") else "",
            "--distpath", "dist",
            "--name", "Star - EXE",
            "main.py"
        ]

        # Remove empty args (caused by missing folders)
        cmd = [arg for arg in cmd if arg]

        subprocess.run(cmd, check=True)

        # Verify output
        exe_path = os.path.join("dist", "Star - EXE.exe")
        if os.path.exists(exe_path):
            print(f"✅ Success! Single executable created: {exe_path}")
            return True
        else:
            print("❌ Executable not created (check errors above)")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller failed (Error: {e})")
        return False

def clean_up():
    """Remove temporary files"""
    for item in ["build", "__pycache__"]:
        if os.path.exists(item):
            try:
                import shutil
                shutil.rmtree(item)
                print(f"🧹 Removed {item}/")
            except Exception as e:
                print(f"⚠️ Could not delete {item}: {e}")

    for spec in [f for f in os.listdir() if f.endswith(".spec")]:
        try:
            os.remove(spec)
            print(f"🧹 Removed {spec}")
        except Exception as e:
            print(f"⚠️ Could not delete {spec}: {e}")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🛠️  Single-File EXE Compiler")
    print("="*50 + "\n")

    if not os.path.exists("logo.png"):
        print("❌ Error: logo.png not found in this directory!")
    else:
        if convert_png_to_ico():
            if compile_all_in_one():
                clean_up()
                print("\n⭐ Done! All code merged into one executable.")

    input("\nPress Enter to exit...")
