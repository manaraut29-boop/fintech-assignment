"""
QuickPay FinTech - JSON API Data Normalization
Task: Flatten and normalize nested API-style JSON transaction data
"""

import pandas as pd
import json
import os

SAMPLE_JSON = [
    {
        "merchant_id": "M001",
        "merchant_name": "Sharma Electronics",
        "address": {"city": "Mumbai", "state": "Maharashtra", "pin": "400001"},
        "transactions": [
            {"transaction_id": "TXN3001", "amount": 1500.00, "date": "2024-03-01", "status": "success", "payment_method": "UPI"},
            {"transaction_id": "TXN3002", "amount": 200.50, "date": "2024-03-02", "status": "failed", "payment_method": "card"}
        ]
    },
    {
        "merchant_id": "M002",
        "merchant_name": "Patel Grocers",
        "address": {"city": "Ahmedabad", "state": "Gujarat", "pin": "380001"},
        "transactions": [
            {"transaction_id": "TXN3003", "amount": 500.00, "date": "2024-03-01", "status": "success", "payment_method": "netbanking"},
            {"transaction_id": "TXN3004", "amount": 750.00, "date": "2024-03-03", "status": "pending", "payment_method": "UPI"}
        ]
    },
    {
        "merchant_id": "M003",
        "merchant_name": "Delhi Fashion Hub",
        "address": {"city": "New Delhi", "state": "Delhi", "pin": "110001"},
        "transactions": [
            {"transaction_id": "TXN3005", "amount": 3200.00, "date": "2024-03-04", "status": "success", "payment_method": "card"},
            {"transaction_id": "TXN3006", "amount": 180.00, "date": "2024-03-05", "status": "refunded", "payment_method": "UPI"}
        ]
    }
]


def load_json(filepath=None):
    """Load JSON from file or use sample data."""
    if filepath and os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
        print(f"Loaded JSON from: {filepath}")
    else:
        print("Using built-in sample JSON data.")
        data = SAMPLE_JSON
    return data


def normalize_json(data):
    """Flatten nested merchant + transaction JSON into a flat DataFrame."""

    df = pd.json_normalize(
        data,
        record_path=["transactions"],
        meta=[
            "merchant_id",
            "merchant_name",
            ["address", "city"],
            ["address", "state"],
            ["address", "pin"]
        ]
    )

    # Rename nested columns
    df.rename(columns={
        "address.city": "city",
        "address.state": "state",
        "address.pin": "pin_code"
    }, inplace=True)

    # Convert types
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Reorder columns
    cols = ["transaction_id", "merchant_id", "merchant_name", "city", "state",
            "pin_code", "amount", "date", "status", "payment_method"]
    df = df[[c for c in cols if c in df.columns]]

    print(f"\nNormalized {len(df)} transaction records from {len(data)} merchants.")
    return df


def analyze_normalized(df):
    """Quick analysis on normalized data."""
    print("\n--- Normalized Data Summary ---")
    print(f"Total records     : {len(df)}")
    print(f"Unique merchants  : {df['merchant_id'].nunique()}")
    print(f"Date range        : {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Total amount      : ₹{df['amount'].sum():,.2f}")
    print(f"Payment methods   : {df['payment_method'].unique().tolist()}")
    print(f"\nSample data:\n")
    print(df.to_string(index=False))


def main():
    os.makedirs("data", exist_ok=True)

    # Save sample JSON first
    with open("data/api_data.json", "w") as f:
        json.dump(SAMPLE_JSON, f, indent=2)
    print("Saved sample JSON to: data/api_data.json")

    data = load_json("data/api_data.json")
    df = normalize_json(data)
    analyze_normalized(df)

    df.to_csv("data/normalized_transactions.csv", index=False)
    print("\nSaved normalized data to: data/normalized_transactions.csv")


if __name__ == "__main__":
    main()
