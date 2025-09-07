# Windows Installation Script for Instascroller MVP
# This script handles PyAudio installation issues on Windows

import sys
import subprocess
import platform

def install_pyaudio_windows():
    """Install PyAudio on Windows using pre-compiled wheel"""
    python_version = f"{sys.version_info.major}{sys.version_info.minor}"
    architecture = "win_amd64" if platform.machine().endswith('64') else "win32"
    
    # Try different wheel URLs for different Python versions
    wheel_urls = [
        f"https://download.lfd.uci.edu/pythonlibs/archived/pyaudio-0.2.11-cp{python_version}-cp{python_version}-{architecture}.whl",
        f"https://files.pythonhosted.org/packages/ab/42/b4f04721c5c5bfc196ce156b3c768998ef8c0ae3654ed29ea5020c749a6b/PyAudio-0.2.11-cp{python_version}-cp{python_version}-{architecture}.whl"
    ]
    
    print("🔧 Installing PyAudio for Windows...")
    
    for url in wheel_urls:
        try:
            print(f"Trying: {url}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", url])
            print("✅ PyAudio installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed with URL: {url}")
            continue
    
    print("❌ Could not install PyAudio with pre-compiled wheels")
    print("\nAlternative solutions:")
    print("1. Install Microsoft Visual C++ Build Tools")
    print("2. Use conda: conda install pyaudio")
    print("3. Use pipwin: pip install pipwin && pipwin install pyaudio")
    return False

def install_other_packages():
    """Install other required packages"""
    packages = ["SpeechRecognition==3.10.0", "pyautogui==0.9.54"]
    
    print("📦 Installing other packages...")
    try:
        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def main():
    """Main installation function for Windows"""
    print("=" * 60)
    print("Instascroller MVP - Windows Installation")
    print("=" * 60)
    
    if platform.system() != "Windows":
        print("❌ This script is designed for Windows only")
        return
    
    print(f"🐍 Python version: {sys.version}")
    print(f"💻 Architecture: {platform.machine()}")
    
    # Install PyAudio first (most problematic on Windows)
    if not install_pyaudio_windows():
        print("\n⚠️  PyAudio installation failed. You may need to:")
        print("1. Install Microsoft Visual C++ Build Tools")
        print("2. Or use the manual installation method in README.md")
        return
    
    # Install other packages
    if not install_other_packages():
        print("\n❌ Installation failed for other packages")
        return
    
    print("\n" + "=" * 60)
    print("🎉 Installation Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open Instagram in your desktop browser")
    print("2. Run: python instascroller.py")
    print("3. Follow the voice commands")
    print("\nFor troubleshooting, see the README.md file")

if __name__ == "__main__":
    main()
