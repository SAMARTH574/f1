@echo off
echo 🚀 Setting up Financial Advisor AI...
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing required packages...
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install packages!
    echo Try running: pip install plotly streamlit pandas numpy
    pause
    exit /b 1
)

echo ✅ All packages installed successfully!

REM Test the installation
echo Testing installation...
python -c "import plotly, streamlit, pandas, numpy; print('✅ All imports successful!')"

if %errorlevel% neq 0 (
    echo ❌ Import test failed!
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo To run the application: streamlit run app.py
echo.
pause