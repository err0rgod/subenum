import os
import sys
import subprocess

def main():
    print("🔧 Setting up Python virtual environment...")

    # Create venv if it doesn't exist
    if not os.path.isdir("venv"):
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created.")
    else:
        print("ℹ️  Virtual environment already exists.")

    # Activate venv and install requirements
    print("📦 Installing requirements...")
    pip_path = "./venv/bin/pip"
    req_file = "requirements.txt"
    if not os.path.isfile(req_file):
        print(f"❌ {req_file} not found!")
        sys.exit(1)
    subprocess.run([pip_path, "install", "-r", req_file], check=True)
    print("✅ All requirements installed.")

    print("\n🎉 Setup complete! To activate your environment, run:")
    print("   source venv/bin/activate")

if __name__ == "__main__":
    main()