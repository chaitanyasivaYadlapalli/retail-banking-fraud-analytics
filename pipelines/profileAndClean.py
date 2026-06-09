import pandas as pd
import os

# Ensure the output directory exists
os.makedirs('clean_data_warehouse', exist_ok=True)

print("Loading raw files into data quality layer...")
df_raw_tx = pd.read_csv('landing_transaction_ledger.csv')
df_raw_cust = pd.read_csv('landing_customer_profiles.csv')

# --- DATA PROFILING & TIE-BREAKING DEDUPLICATION ---
df_raw_tx = df_raw_tx.sort_values(by=['transaction_id', 'system_inserted_at'], ascending=[True, False])

# Drop duplicates, keeping the absolute latest system update
df_clean_tx = df_raw_tx.drop_duplicates(subset=['transaction_id'], keep='first').copy()
print(f"Data Quality Resolution: Removed duplicates. Clean ledger rows = {len(df_clean_tx)}")

# --- EXPORT SEPARATE RELATIONAL TABLES FOR POWER BI ---
df_clean_tx.to_csv('clean_data_warehouse/dim_fact_transaction_ledger.csv', index=False)

# 2. Export the Dimension Table (Customer Profiles)
df_raw_cust.to_csv('clean_data_warehouse/dim_customer_profiles.csv', index=False)

print("SUCCESS: Relational Star Schema tables exported to 'clean_data_warehouse/' folder.")
