#setup.py

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_package(package_name, import_name=None):
    #Check if a package is installed
    if import_name is None:
        import_name = package_name
    
    try:
        spec = importlib.util.find_spec(import_name)
        if spec is not None:
            print(f"✅ {package_name} is installed")
            return True
        else:
            print(f"❌ {package_name} is not installed")
            return False
    except ImportError:
        print(f"❌ {package_name} is not installed")
        return False

def install_packages():
    #Install required packages
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def check_microphone():
    #Check if microphone is available
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        p.terminate()
        
        if device_count > 0:
            print("✅ Microphone devices detected")
            return True
        else:
            print("❌ No microphone devices found")
            return False
    except Exception as e:
        print(f"❌ Error checking microphone: {e}")
        return False

def main():
    #Main setup function
    print("=" * 60)
    print("Instascroller MVP Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check required packages
    print("\n🔍 Checking dependencies...")
    packages = [
        ("SpeechRecognition", "speech_recognition"),
        ("PyAudio", "pyaudio"),
        ("PyAutoGUI", "pyautogui")
    ]
    
    missing_packages = []
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            missing_packages.append(package_name)
    
    # Install missing packages
    if missing_packages:
        print(f"\n📦 Missing packages: {', '.join(missing_packages)}")
        if input("Would you like to install them now? (y/n): ").lower().startswith('y'):
            if not install_packages():
                print("\n❌ Setup failed. Please install packages manually:")
                print("pip install -r requirements.txt")
                sys.exit(1)
        else:
            print("\n⚠️  Please install missing packages manually:")
            print("pip install -r requirements.txt")
            sys.exit(1)
    
    # Check microphone
    print("\n🎤 Checking microphone...")
    check_microphone()
    
    # Final instructions
    print("\n" + "=" * 60)
    print("Setup Complete! 🎉")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open Instagram in your desktop browser")
    print("2. Run: python instascroller.py")
    print("3. Follow the voice commands")
    print("\nFor troubleshooting, see the README.md file")


if __name__ == "__main__":
    main()
