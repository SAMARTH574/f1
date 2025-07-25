#!/bin/bash

echo "🚀 Setting up Financial Advisor AI..."
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed!"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install requirements
echo "Installing required packages..."
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install packages!"
    echo "Try running: pip3 install plotly streamlit pandas numpy"
    exit 1
fi

echo "✅ All packages installed successfully!"

# Test the installation
echo "Testing installation..."
python3 -c "import plotly, streamlit, pandas, numpy; print('✅ All imports successful!')"

if [ $? -ne 0 ]; then
    echo "❌ Import test failed!"
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo "To run the application: streamlit run app.py"
echo ""