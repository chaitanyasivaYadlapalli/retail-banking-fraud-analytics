import duckdb
import pandas as pd

# Load our clean reporting dataset
clean_mart = pd.read_csv('clean_banking_analytics_mart.csv')

# SQL Query using Advanced Analytics Functions
sql_query = """
WITH CalculatedVelocities AS (
    SELECT 
        customer_id,
        transaction_id,
        timestamp,
        amount,
        location,
        credit_risk_score,
        -- Calculate historical average spend per individual customer
        AVG(amount) OVER(PARTITION BY customer_id) as customer_avg_spend,
        -- Calculate the standard deviation of spend to isolate anomalous fluctuations
        STDDEV(amount) OVER(PARTITION BY customer_id) as customer_stddev_spend
    FROM clean_mart
)
SELECT 
    customer_id,
    transaction_id,
    timestamp,
    amount,
    location,
    credit_risk_score,
    round(customer_avg_spend, 2) as avg_spend,
    CASE 
        -- Flag if transaction is > 3 standard deviations from average AND customer has high credit risk
        WHEN amount > (customer_avg_spend + (3 * customer_stddev_spend)) AND credit_risk_score < 600 
            THEN 'CRITICAL RISK / FRAUD VECTOR ALERT'
        -- Flag if transaction is > 3 standard deviations but customer risk profile is fine
        WHEN amount > (customer_avg_spend + (3 * customer_stddev_spend)) 
            THEN 'SUSPICIOUS TRANSACTION VOLOCITY OUTLIER'
        ELSE 'NORMAL SYSTEM ACTIVITY'
    END as fraud_risk_classification
FROM CalculatedVelocities
ORDER BY amount DESC;
"""

print("Executing SQL Risk Analytics Engine...")
sql_results = duckdb.query(sql_query).to_df()

# Display the high-risk entries caught by our framework
anomalies = sql_results[sql_results['fraud_risk_classification'] != 'NORMAL SYSTEM ACTIVITY']

print("\n=== ENTERPRISE RISK ASSESSMENT TARGETS CATCH ===")
print(anomalies[['customer_id', 'transaction_id', 'amount', 'credit_risk_score', 'fraud_risk_classification']].head(10))

# Save results for downstream visualization tools (e.g., PowerBI)
sql_results.to_csv('final_fraud_risk_manifest.csv', index=False)
print("\nSUCCESS: Final analysis written to 'final_fraud_risk_manifest.csv'")