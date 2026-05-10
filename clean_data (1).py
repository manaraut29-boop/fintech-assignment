"""
QuickPay FinTech - Data Cleaning Script
Task: Clean raw transaction data for analysis
"""

import pandas as pd
import numpy as np
import os

def load_data(filepath):
    """Load transaction data from CSV."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} records from {filepath}")
    return df

def clean_transactions(df):
    """Apply all cleaning steps to transaction data."""

    print("\n--- Cleaning Steps ---")

   
    before = len(df)
    df.drop_duplicates(subset=["transaction_id"], inplace=True)
    print(f"[1] Removed duplicates: {before - len(df)} rows dropped")

   
    before = len(df)
    df.dropna(subset=["transaction_id", "merchant_id", "amount"], inplace=True)
    print(f"[2] Dropped missing critical fields: {before - len(df)} rows dropped")

   
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df.dropna(subset=["amount"], inplace=True)
    print(f"[3] Cleaned 'amount' column to numeric")

 
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["date"], inplace=True)
    print(f"[4] Parsed 'date' column to datetime")


    df["status"] = df["status"].str.strip().str.lower()
    valid_statuses = ["success", "failed", "pending", "refunded"]
    df = df[df["status"].isin(valid_statuses)]
    print(f"[5] Standardized 'status' column. Valid statuses: {valid_statuses}")

   
    before = len(df)
    df = df[df["amount"] > 0]
    print(f"[6] Removed non-positive amounts: {before - len(df)} rows dropped")

   
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].str.strip()
    print(f"[7] Stripped whitespace from string columns: {list(str_cols)}")

    print(f"\nCleaning complete. Final dataset: {len(df)} records")
    return df

def generate_cleaning_report(original, cleaned):
    """Print a summary report of cleaning."""
    print("\n====== CLEANING REPORT ======")
    print(f"Original records  : {len(original)}")
    print(f"Cleaned records   : {len(cleaned)}")
    print(f"Records removed   : {len(original) - len(cleaned)}")
    print(f"Null values left  : {cleaned.isnull().sum().sum()}")
    print(f"Duplicate txn IDs : {cleaned.duplicated(subset=['transaction_id']).sum()}")
    print("==============================\n")

def main():
    # Simulate sample data if real file not present
    if not os.path.exists("data/transactions.csv"):
        os.makedirs("data", exist_ok=True)
        print("Sample data not found. Generating synthetic data...\n")
        import random
        from datetime import datetime, timedelta

        records = []
        for i in range(200):
            records.append({
                "transaction_id": f"TXN{1000 + i}" if i % 20 != 0 else f"TXN{1000 + i - 1}",  # intentional duplicates
                "merchant_id": f"M{random.randint(1, 10):03}",
                "amount": round(random.uniform(-50, 5000), 2),
                "date": (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d"),
                "status": random.choice(["success", "failed", "pending", "refunded", "UNKNOWN", None]),
                "currency": "INR"
            })

        pd.DataFrame(records).to_csv("data/transactions.csv", index=False)
        print("Synthetic transactions.csv created in data/\n")

    original_df = load_data("data/transactions.csv")
    cleaned_df = clean_transactions(original_df.copy())
    generate_cleaning_report(original_df, cleaned_df)

    os.makedirs("data", exist_ok=True)
    cleaned_df.to_csv("data/transactions_cleaned.csv", index=False)
    print("Saved cleaned data to: data/transactions_cleaned.csv")

if __name__ == "__main__":
    main()
