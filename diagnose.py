#!/usr/bin/env python3
"""
Financial Advisor AI - Diagnostic Script
This script helps diagnose common setup issues.
"""

import sys
import subprocess
import os

def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 8):
        print("   ❌ Python 3.8+ required!")
        return False
    else:
        print("   ✅ Python version OK")
        return True

def check_pip():
    """Check if pip is available"""
    print("\n🔍 Checking pip...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ pip available: {result.stdout.strip()}")
            return True
        else:
            print("   ❌ pip not available")
            return False
    except Exception as e:
        print(f"   ❌ Error checking pip: {e}")
        return False

def check_imports():
    """Check if required packages can be imported"""
    print("\n🔍 Checking required packages...")
    
    packages = {
        'streamlit': 'Streamlit web framework',
        'plotly': 'Plotly for visualizations',
        'pandas': 'Pandas for data handling',
        'numpy': 'NumPy for numerical computing',
        'requests': 'HTTP requests library',
    }
    
    optional_packages = {
        'google.genai': 'Google Gemini AI (optional for chatbot)'
    }
    
    all_ok = True
    
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ❌ {package} - {description} - NOT FOUND")
            all_ok = False
    
    for package, description in optional_packages.items():
        try:
            __import__(package)
            print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ⚠️  {package} - {description} - OPTIONAL")
    
    return all_ok

def check_files():
    """Check if required files exist"""
    print("\n🔍 Checking project files...")
    
    required_files = [
        'app.py',
        'calculators.py',
        'utils.py',
        'chatbot.py',
        'requirements.txt'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NOT FOUND")
            all_exist = False
    
    return all_exist

def suggest_fixes():
    """Suggest fixes for common issues"""
    print("\n💡 Common Solutions:")
    print("   1. Install missing packages:")
    print("      pip install plotly streamlit pandas numpy")
    print("")
    print("   2. Use Python 3 explicitly:")
    print("      pip3 install -r requirements.txt")
    print("")
    print("   3. Use virtual environment:")
    print("      python -m venv venv")
    print("      venv\\Scripts\\activate  (Windows)")
    print("      source venv/bin/activate  (Linux/Mac)")
    print("      pip install -r requirements.txt")
    print("")
    print("   4. Run setup script:")
    print("      python setup.py")

def main():
    """Main diagnostic function"""
    print("🏥 Financial Advisor AI - Diagnostic Tool")
    print("=" * 50)
    
    python_ok = check_python_version()
    pip_ok = check_pip()
    imports_ok = check_imports()
    files_ok = check_files()
    
    print("\n📊 Summary:")
    print(f"   Python version: {'✅' if python_ok else '❌'}")
    print(f"   Pip available: {'✅' if pip_ok else '❌'}")
    print(f"   Required packages: {'✅' if imports_ok else '❌'}")
    print(f"   Project files: {'✅' if files_ok else '❌'}")
    
    if python_ok and pip_ok and imports_ok and files_ok:
        print("\n🎉 Everything looks good! You can run:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  Issues found. See suggestions below:")
        suggest_fixes()

if __name__ == "__main__":
    main()