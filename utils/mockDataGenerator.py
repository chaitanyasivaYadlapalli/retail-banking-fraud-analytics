import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for identical results
np.random.seed(42)
num_records = 100000

print("Generating raw banking datasets...")

# 1. Generate Customer Profile Dimension Data (500 customers)
customer_ids = [f"CUST_{i:04d}" for i in range(1, 501)]
risk_scores = np.random.randint(300, 850, size=500) # Credit/Risk scores

df_customers = pd.DataFrame({
    'customer_id': customer_ids,
    'credit_risk_score': risk_scores,
    'account_type': np.random.choice(['Checking', 'Savings', 'Credit Card'], size=500)
})

# 2. Generate Transaction Ledger Fact Data
start_time = datetime(2026, 6, 1, 9, 0, 0)
transaction_pool = []

for i in range(num_records):
    cust = np.random.choice(customer_ids)
    tx_time = start_time + timedelta(minutes=int(np.random.randint(0, 1440 * 5))) # spread over 5 days
    amount = float(np.random.exponential(scale=50)) # most transactions are small
    
    # Inject an anomaly: Simulate high-amount fraud spikes every 100th record
    if i % 100 == 0:
        amount = float(np.random.randint(3000, 5000))
        
    transaction_pool.append({
        'transaction_id': f"TX_{i:06d}",
        'customer_id': cust,
        'timestamp': tx_time,
        'amount': round(amount, 2),
        'location': np.random.choice(['Toronto', 'Scarborough', 'Mississauga', 'Vancouver', 'Online']),
        'system_inserted_at': tx_time + timedelta(seconds=int(np.random.randint(5, 30)))
    })

df_transactions = pd.DataFrame(transaction_pool)

# Inject 1500 Duplicate Data Anomalies (Same transaction_id, but modified system times)
duplicates = df_transactions.sample(n=1500, random_state=42).copy()
duplicates['amount'] = duplicates['amount'] * 1.05  # slightly changed amount
duplicates['system_inserted_at'] = duplicates['system_inserted_at'] + timedelta(minutes=2)
df_transactions = pd.concat([df_transactions, duplicates], ignore_index=True)

# Save to local CSV files (This simulates your raw cloud landing zone)
df_customers.to_csv('landing_customer_profiles.csv', index=False)
df_transactions.to_csv('landing_transaction_ledger.csv', index=False)

print("SUCCESS: Created 'landing_customer_profiles.csv' and 'landing_transaction_ledger.csv'")
