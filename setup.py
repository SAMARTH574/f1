#!/usr/bin/env python3
"""
Financial Advisor AI - Setup Script
This script helps you set up the project dependencies.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def test_imports():
    """Test if all critical imports work"""
    try:
        print("Testing imports...")
        import streamlit
        import plotly
        import pandas
        import numpy
        print("✅ All critical imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def setup_env_file():
    """Set up environment file if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("📋 Creating .env file from template...")
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created! Please add your Gemini API key.")
            return False
        else:
            print("⚠️  .env.example not found. Creating basic .env file...")
            with open('.env', 'w') as f:
                f.write("# Add your Gemini API key here\n")
                f.write("GEMINI_API_KEY=your_api_key_here\n")
            print("✅ .env file created! Please add your Gemini API key.")
            return False
    else:
        print("✅ .env file already exists")
        return True

def main():
    """Main setup function"""
    print("🚀 Setting up Financial Advisor AI...")
    print("=" * 50)
    
    if not check_python_version():
        sys.exit(1)
    
    if not install_requirements():
        sys.exit(1)
    
    if not test_imports():
        print("⚠️  Some imports failed. Try running: pip install -r requirements.txt")
        sys.exit(1)
    
    env_ready = setup_env_file()
    
    print("\n🎉 Setup completed successfully!")
    if not env_ready:
        print("\n🔑 NEXT STEP: Add your Gemini API key to the .env file")
        print("   1. Get your API key from: https://aistudio.google.com/app/apikey")
        print("   2. Open .env file and replace 'your_api_key_here' with your actual key")
        print("   3. Save the file")
    print("\n🚀 To run the application: streamlit run app.py")

if __name__ == "__main__":
    main()