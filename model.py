# model.py

import pandas as pd

class InvestmentCalculator:
    def __init__(self, monthly_saving, number_of_period, interest_rate, starting_amount=0):
        self.monthly_saving = monthly_saving
        self.number_of_period = number_of_period
        self.interest_rate = interest_rate / 100  # convert to decimal
        self.starting_amount = starting_amount  # new variable for starting amount
        self.total_contribution = 0
        self.total_return = 0
        self.interest_return = 0
        self.savings_breakdown = pd.DataFrame()  # DataFrame to hold the monthly breakdown
    
    def calculate_apy_return(self):
        # Calculate monthly interest rate based on APY
        monthly_rate = (1 + self.interest_rate) ** (1 / 12) - 1

        # Initialize lists to hold the breakdown per month
        deposits = []
        interests = []
        ending_balances = []

        # Track the cumulative values
        current_contribution = self.starting_amount  # Start with initial amount
        current_balance = self.starting_amount  # The initial balance
        current_interest = 0

        # Calculate month-by-month savings
        for month in range(1, self.number_of_period + 1):
            # Calculate interest on the current balance
            interest_earned = current_balance * monthly_rate

            # Update balance with the new deposit and earned interest
            current_balance += self.monthly_saving + interest_earned
            current_contribution += self.monthly_saving  # Track only contributions
            current_interest += interest_earned
            
            current_balance = round(current_balance, 2)
            current_contribution = round(current_contribution, 2)
            current_interest = round(current_interest, 2)

            # Store values in lists
            deposits.append(current_contribution)
            interests.append(current_interest)
            ending_balances.append(current_balance)
        
        # Calculate total return and interest return
        self.total_contribution = current_contribution
        self.total_return = current_balance
        self.interest_return = current_interest

        # Store the monthly breakdown in a DataFrame
        self.savings_breakdown = pd.DataFrame({
            "Month": range(1, self.number_of_period + 1),
            "Deposit": deposits,
            "Interest": interests,
            "Ending Balance": ending_balances
        })
    
    def get_summary(self):
        return {
            "Total Return": round(self.total_return, 2),
            "Total Contribution": round(self.total_contribution, 2),
            "Interest Return": round(self.interest_return, 2)
        }
    
    def get_savings_breakdown(self):
        return self.savings_breakdown
