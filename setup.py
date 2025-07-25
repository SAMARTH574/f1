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
    
    print("\n🎉 Setup completed successfully!")
    print("To run the application: streamlit run app.py")

if __name__ == "__main__":
    main()