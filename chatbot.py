import json
import logging
import os
from pathlib import Path

import google.generativeai as genai
import streamlit as st

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file if it exists"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print(f"Loaded environment variables from .env file. GEMINI_API_KEY present: {'GEMINI_API_KEY' in os.environ}")

# Load .env file when module is imported
load_env_file()

class FinancialChatbot:
    def __init__(self):
        # Note that the newest Gemini model series is "gemini-1.5-pro" or "gemini-1.5-flash"
        self.model = "gemini-1.5-flash"
        api_key = os.environ.get("GEMINI_API_KEY")
        
        print(f"Initializing FinancialChatbot. API key present: {bool(api_key)}")
        
        if not api_key:
            self.api_available = False
            print("No API key found in environment variables")
        else:
            try:
                genai.configure(api_key=api_key)
                self.model_instance = genai.GenerativeModel(self.model)
                self.api_available = True
                print("API key configured successfully")
            except Exception as e:
                self.api_available = False
                print(f"Error configuring API key: {e}")
        
        self.system_prompt = """
        You are a knowledgeable and helpful financial advisor AI assistant. Your role is to provide 
        accurate, practical financial guidance while being clear that you're providing general 
        information, not personalized financial advice.

        Key guidelines:
        1. Provide clear, actionable financial advice
        2. Explain complex financial concepts in simple terms
        3. Always remind users to consult with qualified financial professionals for personalized advice
        4. Focus on fundamental financial principles like budgeting, saving, investing, and debt management
        5. Be encouraging and supportive while being realistic about financial challenges
        6. Provide specific examples and calculations when helpful
        7. Stay current with general financial best practices

        Topics you can help with:
        - Budgeting and expense tracking
        - Saving strategies and emergency funds
        - Investment basics and portfolio management
        - Debt management and payoff strategies
        - Retirement planning and 401(k) advice
        - Insurance needs assessment
        - Tax planning basics
        - Home buying and mortgage decisions
        - General financial goal setting

        Always include appropriate disclaimers about seeking professional advice for specific situations.
        """

    def get_response(self, user_message):
        """Get AI response for user's financial question"""
        if not self.api_available:
            return "🔑 **API Key Required**: To use the AI Financial Advisor, please add your Gemini API key to the environment variables. You can get one from https://aistudio.google.com/app/apikey"
        
        try:
            prompt = f"{self.system_prompt}\n\nUser Question: {user_message}"
            
            response = self.model_instance.generate_content(prompt)
            
            return response.text or "I apologize, but I'm having trouble processing your request right now. Please try again."
            
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request right now. Error: {str(e)}. Please try again or contact support if the issue persists."

    def get_financial_analysis(self, financial_data):
        """Analyze financial data and provide insights"""
        if not self.api_available:
            return "🔑 **API Key Required**: To use the AI Financial Analysis, please add your Gemini API key to the environment variables."
        
        try:
            prompt = f"""
            {self.system_prompt}
            
            Please analyze the following financial information and provide insights and recommendations:
            
            {json.dumps(financial_data, indent=2)}
            
            Please provide:
            1. Overall financial health assessment
            2. Key strengths and areas for improvement
            3. Specific recommendations for optimization
            4. Priority actions to take
            
            Format your response as clear, actionable advice.
            """
            
            response = self.model_instance.generate_content(prompt)
            
            return response.text or "Unable to analyze financial data at this time."
            
        except Exception as e:
            return f"Unable to analyze financial data at this time. Error: {str(e)}"

    def explain_calculation(self, calculation_type, inputs, results):
        """Explain financial calculations in simple terms"""
        if not self.api_available:
            return "🔑 **API Key Required**: To use the AI Calculation Explanation, please add your Gemini API key to the environment variables."
        
        try:
            prompt = f"""
            {self.system_prompt}
            
            Please explain this {calculation_type} calculation in simple, easy-to-understand terms:
            
            Inputs: {json.dumps(inputs, indent=2)}
            Results: {json.dumps(results, indent=2)}
            
            Please provide:
            1. What these numbers mean
            2. Key insights from the calculation
            3. Practical implications
            4. Suggestions for optimization
            
            Keep the explanation accessible to someone without extensive financial knowledge.
            """
            
            response = self.model_instance.generate_content(prompt)
            
            return response.text or "Unable to explain calculation at this time."
            
        except Exception as e:
            return f"Unable to explain calculation at this time. Error: {str(e)}"
