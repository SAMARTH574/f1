# Financial Advisor AI

A comprehensive financial planning application built with Python and Streamlit, featuring AI-powered financial advice and interactive calculators.

## Features

### 🤖 AI Financial Advisor
- Intelligent chatbot powered by Google Gemini AI
- Personalized financial advice and guidance
- Quick topic suggestions for common financial questions
- Responsible AI with appropriate disclaimers

### 🧮 Financial Calculators
- **Mortgage Calculator**: Home loan payments with taxes and insurance
- **Loan Calculator**: Monthly payments and amortization schedules
- **Investment Calculator**: Growth projections with different strategies
- **Retirement Planning**: Savings targets and timeline analysis
- **Compound Interest**: Compare different compounding frequencies

### 📊 Interactive Visualizations
- Dynamic charts using Plotly
- Payment breakdowns and growth projections
- Amortization schedules
- Investment comparison charts

### 🇮🇳 Localized for India
- All amounts displayed in Indian Rupees (₹)
- Realistic default values for Indian financial scenarios
- Appropriate interest rates and financial parameters

## Screenshots

![Financial Advisor Dashboard](https://via.placeholder.com/800x400?text=Financial+Advisor+Dashboard)

## Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (for AI chatbot features)

### Quick Setup

**Option 1: Automated Setup (Recommended)**

For Windows users:
```bash
# Double-click setup.bat or run in Command Prompt:
setup.bat
```

For Linux/Mac users:
```bash
# Make executable and run:
chmod +x setup.sh
./setup.sh
```

**Option 2: Manual Setup**

1. Clone the repository:
```bash
git clone https://github.com/SAMARTH574/f1.git
cd f1
```

2. Install dependencies:
```bash
# Using pip
pip install -r requirements.txt

# Or install individual packages if requirements.txt fails:
pip install streamlit plotly pandas numpy google-genai requests

# For Python 3 specifically:
pip3 install -r requirements.txt
```

3. Set up your Gemini API key:

**Get your API key:**
- Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create a new API key
- Copy the API key

**Add to environment:**
```bash
# Option 1: Create .env file (recommended)
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Option 2: Set environment variable (Windows Command Prompt)
set GEMINI_API_KEY=your_api_key_here

# Option 3: Set environment variable (Windows PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"

# Option 4: Set environment variable (Linux/Mac)
export GEMINI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run app.py --server.port 5000
```

## Configuration

Create a `.streamlit/config.toml` file with:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## Project Structure

```
financial-advisor-ai/
├── app.py                 # Main Streamlit application
├── chatbot.py            # AI chatbot implementation
├── calculators.py        # Financial calculation functions
├── utils.py              # Utility functions and formatting
├── requirements.txt      # Python dependencies
├── .streamlit/
│   └── config.toml      # Streamlit configuration
└── README.md            # Project documentation
```

## Usage

### AI Chatbot
1. Navigate to the "AI Financial Advisor" section
2. Ask questions about budgeting, investing, retirement planning, etc.
3. Use quick topic buttons for common questions
4. Chat history is maintained during your session

### Financial Calculators
1. Use the sidebar to navigate between different calculators
2. Enter your financial parameters
3. View detailed results with interactive charts
4. Export or analyze the generated data

## Features in Detail

### Mortgage Calculator
- Calculate monthly payments including principal and interest
- Factor in property taxes, insurance, and PMI
- Visual breakdown of payment components
- Total cost analysis over loan term

### Investment Calculator
- Project investment growth over time
- Compare conservative, moderate, and aggressive strategies
- Include monthly contributions
- Visualize compound growth vs contributions

### Retirement Planning
- Calculate required retirement savings
- Assess current savings trajectory
- Identify savings gaps and solutions
- Project savings growth to retirement age

## API Integration

This application uses Google Gemini AI for intelligent financial advice. To use the chatbot feature:

1. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/)
2. Set the `GEMINI_API_KEY` environment variable
3. The application will automatically detect and use the API key

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This application provides general financial information and should not be considered as professional financial advice. Always consult with qualified financial advisors before making important financial decisions.

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'plotly'**
```bash
# Solution 1: Install plotly specifically
pip install plotly

# Solution 2: Reinstall all requirements
pip install -r requirements.txt

# Solution 3: Use Python 3 explicitly
pip3 install plotly pandas streamlit numpy
```

**2. Command 'streamlit' not found**
```bash
# Install streamlit globally
pip install streamlit

# Or run with python module
python -m streamlit run app.py
```

**3. Python version issues**
- Ensure you have Python 3.8 or higher
- Use `python3` instead of `python` on some systems
- Check version: `python --version` or `python3 --version`

**4. Virtual Environment (Recommended)**
```bash
# Create virtual environment
python -m venv financial_advisor_env

# Activate (Windows)
financial_advisor_env\Scripts\activate

# Activate (Linux/Mac)
source financial_advisor_env/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/financial-advisor-ai/issues) section
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## Roadmap

- [ ] Add more calculator types (education savings, debt payoff)
- [ ] Implement user accounts and data persistence
- [ ] Add more visualization options
- [ ] Integration with real financial data APIs
- [ ] Mobile-responsive design improvements
- [ ] Multi-language support

## Technologies Used

- **Frontend**: Streamlit
- **AI/ML**: Google Gemini AI
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Language**: Python 3.11+

---

Made with ❤️ for better financial planning