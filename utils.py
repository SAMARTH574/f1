import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

def format_currency(amount, currency_symbol="₹"):
    """Format number as currency string"""
    if amount < 0:
        return f"-{currency_symbol}{abs(amount):,.2f}"
    return f"{currency_symbol}{amount:,.2f}"

def validate_positive_number(value, field_name="Value"):
    """Validate that a number is positive"""
    if value < 0:
        raise ValueError(f"{field_name} must be positive")
    return True

def validate_percentage(value, field_name="Percentage"):
    """Validate that a percentage is reasonable"""
    if value < 0 or value > 100:
        raise ValueError(f"{field_name} must be between 0 and 100")
    return True

def calculate_monthly_payment(principal, annual_rate, years):
    """Calculate monthly payment for a loan"""
    monthly_rate = annual_rate / 100 / 12
    num_payments = years * 12
    
    if monthly_rate == 0:
        return principal / num_payments
    
    return principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
           ((1 + monthly_rate)**num_payments - 1)

def create_amortization_schedule(principal, annual_rate, years):
    """Create a detailed amortization schedule"""
    monthly_rate = annual_rate / 100 / 12
    num_payments = years * 12
    monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
    
    schedule = []
    remaining_balance = principal
    
    for payment_num in range(1, int(num_payments) + 1):
        interest_payment = remaining_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        
        # Ensure we don't go below zero due to rounding
        if remaining_balance < 0.01:
            principal_payment += remaining_balance
            remaining_balance = 0
        
        schedule.append({
            'Payment': payment_num,
            'Monthly_Payment': monthly_payment,
            'Principal': principal_payment,
            'Interest': interest_payment,
            'Remaining_Balance': remaining_balance
        })
        
        if remaining_balance <= 0:
            break
    
    return pd.DataFrame(schedule)

def calculate_financial_ratios(income, expenses, debt_payments, savings):
    """Calculate key financial ratios"""
    try:
        # Debt-to-income ratio
        debt_to_income = (debt_payments / income) * 100 if income > 0 else 0
        
        # Savings rate
        savings_rate = (savings / income) * 100 if income > 0 else 0
        
        # Expense ratio
        expense_ratio = (expenses / income) * 100 if income > 0 else 0
        
        # Available income after expenses and debt
        available_income = income - expenses - debt_payments
        
        return {
            'debt_to_income_ratio': debt_to_income,
            'savings_rate': savings_rate,
            'expense_ratio': expense_ratio,
            'available_income': available_income,
            'total_expenses': expenses + debt_payments
        }
    except Exception as e:
        raise Exception(f"Error calculating financial ratios: {str(e)}")

def inflation_adjusted_value(current_value, inflation_rate, years):
    """Calculate inflation-adjusted value"""
    return current_value * (1 + inflation_rate / 100) ** years

def present_value(future_value, discount_rate, years):
    """Calculate present value of future amount"""
    return future_value / (1 + discount_rate / 100) ** years

def annuity_present_value(payment, rate, periods):
    """Calculate present value of annuity"""
    if rate == 0:
        return payment * periods
    return payment * (1 - (1 + rate) ** -periods) / rate

def effective_annual_rate(nominal_rate, compounding_frequency):
    """Calculate effective annual rate from nominal rate"""
    return (1 + nominal_rate / compounding_frequency) ** compounding_frequency - 1

def loan_comparison(loans_data):
    """Compare multiple loan options"""
    comparisons = []
    
    for loan in loans_data:
        monthly_payment = calculate_monthly_payment(
            loan['principal'], loan['rate'], loan['years']
        )
        total_paid = monthly_payment * loan['years'] * 12
        total_interest = total_paid - loan['principal']
        
        comparisons.append({
            'loan_name': loan.get('name', 'Loan'),
            'principal': loan['principal'],
            'rate': loan['rate'],
            'years': loan['years'],
            'monthly_payment': monthly_payment,
            'total_paid': total_paid,
            'total_interest': total_interest
        })
    
    return pd.DataFrame(comparisons)

def budget_analyzer(income, expenses_dict):
    """Analyze budget and provide recommendations"""
    total_expenses = sum(expenses_dict.values())
    remaining_income = income - total_expenses
    
    # Calculate expense percentages
    expense_percentages = {
        category: (amount / income) * 100 
        for category, amount in expenses_dict.items()
    }
    
    # Standard budget percentages (50/30/20 rule as baseline)
    recommendations = {
        'housing': {'recommended': 30, 'max': 35},
        'transportation': {'recommended': 15, 'max': 20},
        'food': {'recommended': 12, 'max': 15},
        'utilities': {'recommended': 8, 'max': 10},
        'entertainment': {'recommended': 5, 'max': 10},
        'savings': {'recommended': 20, 'max': float('inf')}
    }
    
    analysis = {
        'total_income': income,
        'total_expenses': total_expenses,
        'remaining_income': remaining_income,
        'expense_percentages': expense_percentages,
        'savings_rate': (remaining_income / income) * 100 if income > 0 else 0
    }
    
    return analysis

def tax_bracket_calculator(income, filing_status='single', tax_year=2024):
    """Calculate estimated federal income tax (simplified)"""
    # 2024 tax brackets for single filers (simplified)
    brackets_single = [
        (11000, 0.10),
        (44725, 0.12),
        (95375, 0.22),
        (182050, 0.24),
        (231250, 0.32),
        (578125, 0.35),
        (float('inf'), 0.37)
    ]
    
    brackets_married = [
        (22000, 0.10),
        (89450, 0.12),
        (190750, 0.22),
        (364200, 0.24),
        (462500, 0.32),
        (693750, 0.35),
        (float('inf'), 0.37)
    ]
    
    brackets = brackets_single if filing_status == 'single' else brackets_married
    
    tax_owed = 0
    remaining_income = income
    previous_limit = 0
    
    for limit, rate in brackets:
        if remaining_income <= 0:
            break
            
        taxable_in_bracket = min(remaining_income, limit - previous_limit)
        tax_owed += taxable_in_bracket * rate
        remaining_income -= taxable_in_bracket
        previous_limit = limit
    
    effective_rate = (tax_owed / income) * 100 if income > 0 else 0
    
    return {
        'gross_income': income,
        'tax_owed': tax_owed,
        'after_tax_income': income - tax_owed,
        'effective_tax_rate': effective_rate
    }

def retirement_withdrawal_calculator(portfolio_value, withdrawal_rate=4):
    """Calculate safe retirement withdrawal amounts"""
    annual_withdrawal = portfolio_value * (withdrawal_rate / 100)
    monthly_withdrawal = annual_withdrawal / 12
    
    return {
        'portfolio_value': portfolio_value,
        'withdrawal_rate': withdrawal_rate,
        'annual_withdrawal': annual_withdrawal,
        'monthly_withdrawal': monthly_withdrawal
    }
