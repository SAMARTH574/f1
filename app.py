import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import custom modules
from chatbot import FinancialChatbot
from calculators import (
    loan_calculator,
    mortgage_calculator,
    investment_calculator,
    retirement_calculator,
    compound_interest_calculator
)
from utils import format_currency, validate_positive_number, create_amortization_schedule

# Page configuration
st.set_page_config(
    page_title="Financial Advisor AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None

# Initialize chatbot only when needed
def get_chatbot():
    if st.session_state.chatbot is None or not st.session_state.chatbot.api_available:
        st.session_state.chatbot = FinancialChatbot()
    return st.session_state.chatbot

def main():
    # Header
    st.title("💰 Financial Advisor AI")
    st.markdown("### Your Personal Financial Planning Assistant")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a tool:",
        [
            "🤖 AI Financial Advisor",
            "🏠 Mortgage Calculator",
            "💳 Loan Calculator",
            "📈 Investment Calculator",
            "🏖️ Retirement Planning",
            "💰 Compound Interest"
        ]
    )
    
    # Disclaimer
    st.sidebar.markdown("---")
    st.sidebar.warning(
        "⚠️ **Disclaimer**: This application provides general financial information "
        "and should not be considered as professional financial advice. "
        "Please consult with a qualified financial advisor for personalized guidance."
    )
    
    # Main content based on page selection
    if page == "🤖 AI Financial Advisor":
        show_chatbot_page()
    elif page == "🏠 Mortgage Calculator":
        show_mortgage_calculator()
    elif page == "💳 Loan Calculator":
        show_loan_calculator()
    elif page == "📈 Investment Calculator":
        show_investment_calculator()
    elif page == "🏖️ Retirement Planning":
        show_retirement_calculator()
    elif page == "💰 Compound Interest":
        show_compound_interest_calculator()

def show_chatbot_page():
    st.header("🤖 AI Financial Advisor Chat")
    
    # Get chatbot instance
    chatbot = get_chatbot()
    
    # Debug: Show API status
    if not chatbot.api_available:
        st.error("🔑 **API Key Issue**: The AI Financial Advisor is not properly configured. Please check your API key setup.")
        st.info("To fix this issue:\n1. Ensure you have a valid Gemini API key\n2. Check that the `.env` file contains your API key\n3. Restart the application")
    
    # Chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for i, (role, message) in enumerate(st.session_state.chat_history):
                if role == "user":
                    st.markdown(f"**You:** {message}")
                else:
                    st.markdown(f"**Financial Advisor:** {message}")
                st.markdown("---")
        
        # Chat input
        user_input = st.text_input("Ask me anything about finance:", key="chat_input")
        
        col_send, col_clear = st.columns([1, 1])
        with col_send:
            if st.button("Send", type="primary") and user_input:
                # Add user message to history
                st.session_state.chat_history.append(("user", user_input))
                
                # Get AI response
                with st.spinner("Thinking..."):
                    response = chatbot.get_response(user_input)
                    st.session_state.chat_history.append(("assistant", response))
                
                st.rerun()
        
        with col_clear:
            if st.button("Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
    
    with col2:
        st.subheader("Quick Topics")
        topics = [
            "How to start investing?",
            "Calculate my retirement needs",
            "Best savings strategies",
            "Understanding credit scores",
            "Emergency fund planning",
            "Tax planning tips"
        ]
        
        for topic in topics:
            if st.button(topic, key=f"topic_{topic}"):
                st.session_state.chat_history.append(("user", topic))
                with st.spinner("Thinking..."):
                    response = chatbot.get_response(topic)
                    st.session_state.chat_history.append(("assistant", response))
                st.rerun()

def show_mortgage_calculator():
    st.header("🏠 Mortgage Calculator")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Loan Details")
        home_price = st.number_input("Home Price (₹)", min_value=0.0, value=2500000.0, step=10000.0)
        down_payment = st.number_input("Down Payment (₹)", min_value=0.0, value=500000.0, step=10000.0)
        interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=6.5, step=0.1)
        loan_term = st.selectbox("Loan Term", [15, 20, 25, 30], index=3)
        
        # Additional costs
        st.subheader("Additional Costs")
        property_tax = st.number_input("Annual Property Tax (₹)", min_value=0.0, value=30000.0, step=1000.0)
        insurance = st.number_input("Annual Home Insurance (₹)", min_value=0.0, value=10000.0, step=1000.0)
        pmi = st.number_input("PMI (₹/month)", min_value=0.0, value=0.0, step=100.0)
    
    with col2:
        if st.button("Calculate Mortgage", type="primary"):
            try:
                result = mortgage_calculator(home_price, down_payment, interest_rate, loan_term, 
                                           property_tax, insurance, pmi)
                
                st.subheader("Results")
                st.metric("Monthly Payment (P&I)", format_currency(result['monthly_payment']))
                st.metric("Total Monthly Payment", format_currency(result['total_monthly']))
                st.metric("Total Interest Paid", format_currency(result['total_interest']))
                st.metric("Total Cost of Loan", format_currency(result['total_cost']))
                
                # Payment breakdown chart
                fig = go.Figure(data=[
                    go.Bar(name='Principal & Interest', x=['Monthly Payment'], 
                          y=[result['monthly_payment']]),
                    go.Bar(name='Property Tax', x=['Monthly Payment'], 
                          y=[property_tax/12]),
                    go.Bar(name='Insurance', x=['Monthly Payment'], 
                          y=[insurance/12]),
                    go.Bar(name='PMI', x=['Monthly Payment'], 
                          y=[pmi])
                ])
                fig.update_layout(title="Monthly Payment Breakdown", barmode='stack')
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error calculating mortgage: {str(e)}")

def show_loan_calculator():
    st.header("💳 Loan Calculator")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        loan_amount = st.number_input("Loan Amount (₹)", min_value=0.0, value=200000.0, step=10000.0)
        interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=8.5, step=0.1)
        loan_term = st.number_input("Loan Term (years)", min_value=1, value=5, step=1)
        
        loan_type = st.selectbox("Loan Type", ["Personal Loan", "Auto Loan", "Student Loan", "Other"])
    
    with col2:
        if st.button("Calculate Loan", type="primary"):
            try:
                result = loan_calculator(loan_amount, interest_rate, loan_term)
                
                st.subheader("Results")
                st.metric("Monthly Payment", format_currency(result['monthly_payment']))
                st.metric("Total Interest", format_currency(result['total_interest']))
                st.metric("Total Amount Paid", format_currency(result['total_paid']))
                
                # Create amortization schedule
                schedule = create_amortization_schedule(loan_amount, interest_rate, loan_term)
                
                # Show first few payments
                st.subheader("Amortization Schedule (First 12 Payments)")
                st.dataframe(schedule.head(12))
                
                # Payment breakdown over time
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=schedule['Payment'], y=schedule['Principal'], 
                                       mode='lines', name='Principal'))
                fig.add_trace(go.Scatter(x=schedule['Payment'], y=schedule['Interest'], 
                                       mode='lines', name='Interest'))
                fig.update_layout(title="Principal vs Interest Over Time", 
                                xaxis_title="Payment Number", yaxis_title="Amount (₹)")
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error calculating loan: {str(e)}")

def show_investment_calculator():
    st.header("📈 Investment Calculator")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        initial_investment = st.number_input("Initial Investment (₹)", min_value=0.0, value=100000.0, step=5000.0)
        monthly_contribution = st.number_input("Monthly Contribution (₹)", min_value=0.0, value=5000.0, step=500.0)
        annual_return = st.number_input("Expected Annual Return (%)", min_value=0.0, value=7.0, step=0.5)
        investment_period = st.number_input("Investment Period (years)", min_value=1, value=20, step=1)
        
        st.subheader("Investment Strategy")
        strategy = st.selectbox("Investment Type", 
                               ["Conservative (3-5%)", "Moderate (5-8%)", "Aggressive (8-12%)", "Custom"])
        
        if strategy != "Custom":
            if strategy == "Conservative (3-5%)":
                annual_return = 4.0
            elif strategy == "Moderate (5-8%)":
                annual_return = 6.5
            elif strategy == "Aggressive (8-12%)":
                annual_return = 10.0
    
    with col2:
        if st.button("Calculate Investment", type="primary"):
            try:
                result = investment_calculator(initial_investment, monthly_contribution, 
                                             annual_return, investment_period)
                
                st.subheader("Results")
                st.metric("Final Value", format_currency(result['final_value']))
                st.metric("Total Contributions", format_currency(result['total_contributions']))
                st.metric("Total Earnings", format_currency(result['total_earnings']))
                st.metric("Return on Investment", f"{result['roi']:.1f}%")
                
                # Growth chart
                years = list(range(investment_period + 1))
                values = []
                contributions = []
                
                for year in years:
                    year_result = investment_calculator(initial_investment, monthly_contribution, 
                                                      annual_return, year)
                    values.append(year_result['final_value'])
                    contributions.append(year_result['total_contributions'])
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=years, y=values, mode='lines', name='Total Value'))
                fig.add_trace(go.Scatter(x=years, y=contributions, mode='lines', name='Contributions'))
                fig.update_layout(title="Investment Growth Over Time", 
                                xaxis_title="Years", yaxis_title="Amount (₹)")
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error calculating investment: {str(e)}")

def show_retirement_calculator():
    st.header("🏖️ Retirement Planning Calculator")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        current_age = st.number_input("Current Age", min_value=18, max_value=100, value=30)
        retirement_age = st.number_input("Retirement Age", min_value=current_age+1, max_value=100, value=65)
        current_income = st.number_input("Current Annual Income (₹)", min_value=0.0, value=500000.0, step=10000.0)
        current_savings = st.number_input("Current Retirement Savings (₹)", min_value=0.0, value=200000.0, step=10000.0)
        
        st.subheader("Retirement Goals")
        income_replacement = st.slider("Income Replacement in Retirement (%)", 40, 100, 80)
        monthly_contribution = st.number_input("Monthly Retirement Contribution (₹)", min_value=0.0, value=5000.0, step=500.0)
        expected_return = st.number_input("Expected Annual Return (%)", min_value=0.0, value=7.0, step=0.5)
    
    with col2:
        if st.button("Calculate Retirement", type="primary"):
            try:
                result = retirement_calculator(current_age, retirement_age, current_income, 
                                             current_savings, income_replacement, 
                                             monthly_contribution, expected_return)
                
                st.subheader("Results")
                st.metric("Years to Retirement", retirement_age - current_age)
                st.metric("Required Retirement Savings", format_currency(result['required_savings']))
                st.metric("Projected Savings at Retirement", format_currency(result['projected_savings']))
                
                if result['projected_savings'] >= result['required_savings']:
                    st.success("✅ You're on track for retirement!")
                    surplus = result['projected_savings'] - result['required_savings']
                    st.metric("Surplus", format_currency(surplus))
                else:
                    st.warning("⚠️ You may need to save more for retirement")
                    shortfall = result['required_savings'] - result['projected_savings']
                    st.metric("Shortfall", format_currency(shortfall))
                    
                    # Calculate additional monthly savings needed
                    years_left = retirement_age - current_age
                    additional_monthly = shortfall / (years_left * 12)
                    st.metric("Additional Monthly Savings Needed", format_currency(additional_monthly))
                
                # Retirement savings projection chart
                years = list(range(current_age, retirement_age + 1))
                savings_values = []
                
                for age in years:
                    years_invested = age - current_age
                    if years_invested == 0:
                        savings_values.append(current_savings)
                    else:
                        temp_result = investment_calculator(current_savings, monthly_contribution, 
                                                          expected_return, years_invested)
                        savings_values.append(temp_result['final_value'])
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=years, y=savings_values, mode='lines', name='Projected Savings'))
                fig.add_hline(y=result['required_savings'], line_dash="dash", 
                            annotation_text="Required Savings Target")
                fig.update_layout(title="Retirement Savings Projection", 
                                xaxis_title="Age", yaxis_title="Savings (₹)")
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error calculating retirement: {str(e)}")

def show_compound_interest_calculator():
    st.header("💰 Compound Interest Calculator")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        principal = st.number_input("Principal Amount (₹)", min_value=0.0, value=50000.0, step=1000.0)
        annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.0, step=0.1)
        years = st.number_input("Time Period (years)", min_value=1, value=10, step=1)
        
        st.subheader("Compounding Frequency")
        compound_frequency = st.selectbox("Compounding", 
                                        ["Annually", "Semi-annually", "Quarterly", 
                                         "Monthly", "Weekly", "Daily"])
        
        frequency_map = {
            "Annually": 1,
            "Semi-annually": 2,
            "Quarterly": 4,
            "Monthly": 12,
            "Weekly": 52,
            "Daily": 365
        }
        n = frequency_map[compound_frequency]
    
    with col2:
        if st.button("Calculate Compound Interest", type="primary"):
            try:
                result = compound_interest_calculator(principal, annual_rate, years, n)
                
                st.subheader("Results")
                st.metric("Final Amount", format_currency(result['final_amount']))
                st.metric("Total Interest Earned", format_currency(result['interest_earned']))
                st.metric("Effective Annual Rate", f"{result['effective_rate']:.2f}%")
                
                # Compare different compounding frequencies
                frequencies = {"Annual": 1, "Semi-annual": 2, "Quarterly": 4, 
                             "Monthly": 12, "Weekly": 52, "Daily": 365}
                
                comparison_data = []
                for freq_name, freq_value in frequencies.items():
                    comp_result = compound_interest_calculator(principal, annual_rate, years, freq_value)
                    comparison_data.append({
                        "Frequency": freq_name,
                        "Final Amount": comp_result['final_amount'],
                        "Interest Earned": comp_result['interest_earned']
                    })
                
                df = pd.DataFrame(comparison_data)
                
                st.subheader("Compounding Frequency Comparison")
                st.dataframe(df)
                
                # Growth over time chart
                time_periods = list(range(1, years + 1))
                amounts = []
                
                for period in time_periods:
                    period_result = compound_interest_calculator(principal, annual_rate, period, n)
                    amounts.append(period_result['final_amount'])
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=time_periods, y=amounts, mode='lines+markers', 
                                       name='Compound Growth'))
                fig.add_trace(go.Scatter(x=time_periods, 
                                       y=[principal * (1 + annual_rate/100)**year for year in time_periods], 
                                       mode='lines', name='Simple Interest'))
                fig.update_layout(title="Compound vs Simple Interest Growth", 
                                xaxis_title="Years", yaxis_title="Amount (₹)")
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error calculating compound interest: {str(e)}")

if __name__ == "__main__":
    main()
