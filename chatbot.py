import json
import logging
import os

from google import genai
from google.genai import types
import streamlit as st

class FinancialChatbot:
    def __init__(self):
        # Note that the newest Gemini model series is "gemini-2.5-flash" or "gemini-2.5-pro"
        self.model = "gemini-2.5-flash"
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            self.client = None
            self.api_available = False
        else:
            try:
                self.client = genai.Client(api_key=api_key)
                self.api_available = True
            except Exception as e:
                self.client = None
                self.api_available = False
        
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
        - Savings strategies and emergency funds
        - Basic investing principles
        - Debt management and payoff strategies
        - Retirement planning basics
        - Insurance needs
        - Credit score improvement
        - Tax planning fundamentals
        - Financial goal setting

        Always include appropriate disclaimers about seeking professional advice for specific situations.
        """

    def get_response(self, user_message):
        """Get AI response for user's financial question"""
        if not self.api_available:
            return "🔑 **API Key Required**: To use the AI Financial Advisor, please add your Gemini API key to the environment variables. You can get one from https://aistudio.google.com/app/apikey"
        
        try:
            prompt = f"{self.system_prompt}\n\nUser Question: {user_message}"
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
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
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
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
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text or "Unable to explain calculation at this time."
            
        except Exception as e:
            return f"Unable to explain calculation at this time. Error: {str(e)}"
