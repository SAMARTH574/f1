# Financial Advisor AI - Replit Guide

## Overview

This is a Streamlit-based financial planning application that provides users with AI-powered financial advice and various financial calculators. The app combines interactive financial tools with an OpenAI-powered chatbot to help users make informed financial decisions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application
- **Layout**: Wide layout with expandable sidebar navigation
- **Visualization**: Plotly for interactive charts and graphs
- **State Management**: Streamlit session state for chat history and chatbot instance

### Backend Architecture
- **Core Logic**: Python-based modular architecture
- **AI Integration**: Google Gemini 2.5 Flash model for financial advice chatbot
- **Calculations**: Custom mathematical functions for financial computations
- **Data Processing**: Pandas and NumPy for financial data manipulation

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Entry point and navigation controller
- **Features**: Page routing, session state initialization, main UI layout
- **Navigation Options**: AI advisor, mortgage calculator, loan calculator, investment calculator, retirement planning, compound interest calculator

### 2. Financial Chatbot (`chatbot.py`)
- **AI Model**: Google Gemini 2.5 Flash (latest Gemini model)
- **System Prompt**: Configured as a knowledgeable financial advisor with appropriate disclaimers
- **Capabilities**: Budgeting advice, investment guidance, debt management, retirement planning
- **Safety**: Includes disclaimers about seeking professional financial advice
- **API Integration**: Uses Google Gemini API with graceful error handling for missing API keys

### 3. Financial Calculators (`calculators.py`)
- **Loan Calculator**: Monthly payments, total interest, amortization
- **Mortgage Calculator**: Home loans with taxes, insurance, and PMI
- **Investment Calculator**: Growth projections and returns
- **Retirement Calculator**: Savings targets and timeline planning
- **Compound Interest Calculator**: Investment growth over time

### 4. Utility Functions (`utils.py`)
- **Formatting**: Currency display and number formatting
- **Validation**: Input validation for positive numbers and percentages
- **Calculations**: Core financial mathematics functions
- **Amortization**: Detailed payment schedule generation

## Data Flow

1. **User Input**: Users interact through Streamlit interface (sidebar navigation, form inputs)
2. **Route Processing**: Main app routes to appropriate calculator or chatbot
3. **Calculation Engine**: Mathematical functions process financial inputs
4. **AI Processing**: OpenAI API processes natural language queries
5. **Result Display**: Formatted results shown via Streamlit components and Plotly visualizations
6. **Session Persistence**: Chat history and state maintained in Streamlit session

## External Dependencies

### Required Python Packages
- `streamlit`: Web application framework
- `pandas`: Data manipulation and analysis
- `plotly`: Interactive data visualization
- `numpy`: Numerical computations
- `google-genai`: Google Gemini AI integration
- `requests`: HTTP client for API calls

### API Services
- **Google Gemini API**: Gemini 2.5 Flash model for financial advice chatbot
- **Configuration**: Requires GEMINI_API_KEY environment variable

## Deployment Strategy

### Environment Setup
- Python environment with required dependencies
- OpenAI API key configuration
- Streamlit server deployment

### Recommended Deployment Platforms
- **Streamlit Cloud**: Native deployment platform
- **Replit**: Direct deployment with environment management
- **Heroku/Railway**: Container-based deployment options

### Configuration Requirements
- Environment variable: `GEMINI_API_KEY`
- Python version: 3.11+ (current setup)
- Memory requirements: Moderate (suitable for standard hosting)

### Security Considerations
- API key protection through environment variables
- Input validation for all financial calculations
- Appropriate disclaimers for AI-generated financial advice
- No sensitive user data storage (stateless design)

## Development Notes

- The application uses a modular design for easy maintenance and feature additions
- Financial calculations include error handling and edge case management
- The chatbot is configured with responsible AI guidelines for financial advice
- All currency formatting and validation functions are centralized in utils module
- The system is designed to be easily extensible with additional financial tools