import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import math

def loan_calculator(principal, annual_rate, years):
    """Calculate loan payments and total costs"""
    try:
        monthly_rate = annual_rate / 100 / 12
        num_payments = years * 12
        
        # Validate inputs
        if principal <= 0 or years <= 0:
            raise ValueError("Principal and years must be positive")
        if annual_rate < 0:
            raise ValueError("Interest rate cannot be negative")
        if num_payments > 1200:  # Limit to 100 years
            raise ValueError("Loan term too long (max 100 years)")
        
        if monthly_rate == 0:
            monthly_payment = principal / num_payments
        else:
            # Use more stable calculation to avoid overflow
            try:
                power_term = (1 + monthly_rate)**num_payments
                if power_term > 1e10:  # Prevent overflow
                    raise OverflowError("Interest rate and term combination too large")
                monthly_payment = principal * (monthly_rate * power_term) / (power_term - 1)
            except OverflowError:
                # Fallback calculation for very large terms
                monthly_payment = principal * monthly_rate
        
        total_paid = monthly_payment * num_payments
        total_interest = total_paid - principal
        
        return {
            'monthly_payment': monthly_payment,
            'total_paid': total_paid,
            'total_interest': total_interest,
            'principal': principal
        }
    except Exception as e:
        raise Exception(f"Error in loan calculation: {str(e)}")

def mortgage_calculator(home_price, down_payment, annual_rate, years, 
                       property_tax=0.0, insurance=0.0, pmi=0.0):
    """Calculate mortgage payments including taxes and insurance"""
    try:
        loan_amount = home_price - down_payment
        
        # Calculate base mortgage payment
        loan_result = loan_calculator(loan_amount, annual_rate, years)
        monthly_payment = loan_result['monthly_payment']
        
        # Add monthly taxes, insurance, and PMI
        monthly_tax = property_tax / 12
        monthly_insurance = insurance / 12
        total_monthly = monthly_payment + monthly_tax + monthly_insurance + pmi
        
        total_interest = loan_result['total_interest']
        total_cost = loan_result['total_paid'] + (property_tax * years) + (insurance * years) + (pmi * 12 * years)
        
        return {
            'loan_amount': loan_amount,
            'monthly_payment': monthly_payment,
            'total_monthly': total_monthly,
            'total_interest': total_interest,
            'total_cost': total_cost,
            'monthly_tax': monthly_tax,
            'monthly_insurance': monthly_insurance,
            'monthly_pmi': pmi
        }
    except Exception as e:
        raise Exception(f"Error in mortgage calculation: {str(e)}")

def investment_calculator(initial_investment, monthly_contribution, annual_return, years):
    """Calculate investment growth with regular contributions"""
    try:
        monthly_rate = annual_return / 100 / 12
        num_months = years * 12
        
        # Future value of initial investment
        if monthly_rate == 0:
            fv_initial = initial_investment
            fv_contributions = monthly_contribution * num_months
        else:
            fv_initial = initial_investment * (1 + monthly_rate)**num_months
            
            # Future value of monthly contributions (annuity)
            if num_months > 0:
                fv_contributions = monthly_contribution * (((1 + monthly_rate)**num_months - 1) / monthly_rate)
            else:
                fv_contributions = 0
        
        final_value = fv_initial + fv_contributions
        total_contributions = initial_investment + (monthly_contribution * num_months)
        total_earnings = final_value - total_contributions
        
        roi = (total_earnings / total_contributions) * 100 if total_contributions > 0 else 0
        
        return {
            'final_value': final_value,
            'total_contributions': total_contributions,
            'total_earnings': total_earnings,
            'roi': roi
        }
    except Exception as e:
        raise Exception(f"Error in investment calculation: {str(e)}")

def retirement_calculator(current_age, retirement_age, current_income, current_savings,
                         income_replacement_percent, monthly_contribution, expected_return):
    """Calculate retirement planning scenarios"""
    try:
        years_to_retirement = retirement_age - current_age
        years_in_retirement = 25  # Assume 25 years in retirement
        
        # Calculate required retirement savings (using 4% withdrawal rule)
        annual_retirement_income = current_income * (income_replacement_percent / 100)
        required_savings = annual_retirement_income / 0.04
        
        # Calculate projected savings at retirement
        projected_result = investment_calculator(current_savings, monthly_contribution, 
                                               expected_return, years_to_retirement)
        projected_savings = projected_result['final_value']
        
        return {
            'required_savings': required_savings,
            'projected_savings': projected_savings,
            'annual_retirement_income': annual_retirement_income,
            'years_to_retirement': years_to_retirement,
            'savings_gap': required_savings - projected_savings
        }
    except Exception as e:
        raise Exception(f"Error in retirement calculation: {str(e)}")

def compound_interest_calculator(principal, annual_rate, years, compound_frequency):
    """Calculate compound interest with different compounding frequencies"""
    try:
        rate = annual_rate / 100
        final_amount = principal * (1 + rate / compound_frequency)**(compound_frequency * years)
        interest_earned = final_amount - principal
        
        # Calculate effective annual rate
        effective_rate = ((1 + rate / compound_frequency)**compound_frequency - 1) * 100
        
        return {
            'final_amount': final_amount,
            'interest_earned': interest_earned,
            'effective_rate': effective_rate,
            'principal': principal
        }
    except Exception as e:
        raise Exception(f"Error in compound interest calculation: {str(e)}")

def debt_snowball_calculator(debts):
    """Calculate debt payoff using snowball method"""
    try:
        # debts should be a list of dictionaries with 'name', 'balance', 'min_payment', 'interest_rate'
        sorted_debts = sorted(debts, key=lambda x: x['balance'])  # Sort by balance (snowball)
        
        results = []
        total_extra = sum(debt.get('extra_payment', 0) for debt in debts)
        
        for i, debt in enumerate(sorted_debts):
            # Add extra payments from previously paid off debts
            extra_payment = debt.get('extra_payment', 0) + sum(
                d['min_payment'] + d.get('extra_payment', 0) 
                for d in sorted_debts[:i]
            )
            
            total_payment = debt['min_payment'] + extra_payment
            
            # Calculate payoff time
            if debt['interest_rate'] == 0:
                months_to_payoff = debt['balance'] / total_payment
            else:
                monthly_rate = debt['interest_rate'] / 100 / 12
                months_to_payoff = math.log(1 + (debt['balance'] * monthly_rate) / total_payment) / math.log(1 + monthly_rate)
            
            total_interest = (total_payment * months_to_payoff) - debt['balance']
            
            results.append({
                'name': debt['name'],
                'balance': debt['balance'],
                'monthly_payment': total_payment,
                'months_to_payoff': months_to_payoff,
                'total_interest': total_interest
            })
        
        return results
    except Exception as e:
        raise Exception(f"Error in debt snowball calculation: {str(e)}")

def emergency_fund_calculator(monthly_expenses, target_months=6, current_savings=0, monthly_savings=0):
    """Calculate emergency fund requirements and timeline"""
    try:
        target_amount = monthly_expenses * target_months
        amount_needed = max(0, target_amount - current_savings)
        
        if monthly_savings > 0 and amount_needed > 0:
            months_to_goal = amount_needed / monthly_savings
        else:
            months_to_goal = 0
        
        return {
            'target_amount': target_amount,
            'current_savings': current_savings,
            'amount_needed': amount_needed,
            'months_to_goal': months_to_goal,
            'monthly_expenses': monthly_expenses,
            'target_months': target_months
        }
    except Exception as e:
        raise Exception(f"Error in emergency fund calculation: {str(e)}")
