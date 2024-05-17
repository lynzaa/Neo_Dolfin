import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Define variables
monthly_due_date = 5  # Assume the due date is the 5th of each month
monthly_repayment_amount = 100  # Monthly repayment amount in currency
transaction_limit = 1000  # Transaction/account limit in currency
interest_value = 10  # Interest value for late payment in currency
late_payment_value = 50  # Penalty for late payment in currency
account_number = 'CC123456789'  # Sample account number
user_id = 'UserB'

# Generate credit card dataset
def generate_credit_card_data(start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date, freq='MS')
    data = {'Date of Transaction': [], 'Description': [], 'Amount': [], 'Balance of Account': [], 
            'User ID': [], 'Transaction Type': [], 'Merchant Name': [], 'Transaction Category': [], 
            'Transaction Currency': [], 'Transaction Location': []}
    balance = 0  # Initial balance is assumed to be 0
    for date in dates:
        # Check if it's the due date
        if date.day == monthly_due_date:
            # Assume a random chance of late payment
            if random.random() < 0.5:  # 50% chance of late payment
                description = 'Late Payment'
                amount = -(monthly_repayment_amount + late_payment_value)
                balance -= monthly_repayment_amount + late_payment_value
                transaction_type = 'Late Payment'
            else:
                description = 'Repayment'
                amount = -monthly_repayment_amount
                balance -= monthly_repayment_amount
                transaction_type = 'Repayment'
        else:
            # Assume random transactions throughout the month
            description = 'Charge' if random.random() < 0.5 else 'Transaction'
            amount = random.uniform(-transaction_limit, transaction_limit)
            balance += amount
            if amount < 0:
                transaction_type = 'Purchase'
            else:
                transaction_type = 'Repayment'

        data['Date of Transaction'].append(date)
        data['Description'].append(description)
        data['Amount'].append(amount)
        data['Balance of Account'].append(balance)
        data['User ID'].append(user_id)
        data['Transaction Type'].append(transaction_type)
        data['Merchant Name'].append(random.choice(['Amazon', 'Walmart', 'Starbucks', 'Uber', 'Netflix']))
        data['Transaction Category'].append(random.choice(['Shopping', 'Food', 'Transportation', 'Entertainment']))
        data['Transaction Currency'].append('USD')  # Assuming transactions are in USD
        data['Transaction Location'].append(random.choice(['New York', 'Los Angeles', 'Chicago', 'Miami', 'San Francisco']))

    return pd.DataFrame(data)

# Generate data for two years (24 months)
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)
credit_card_data = generate_credit_card_data(start_date, end_date)

# Save data to Excel
credit_card_data.to_excel('credit_card_data.xlsx', index=False)
