"""
QuickPay FinTech - Payment Reconciliation Workflow
Task: Match transactions against settlements and flag mismatches
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_data():
    """Load transactions and settlements data."""
    os.makedirs("data", exist_ok=True)

    # Generate synthetic data if not present
    if not os.path.exists("data/transactions_cleaned.csv"):
        print("Generating synthetic transaction data...")
        records = []
        for i in range(100):
            records.append({
                "transaction_id": f"TXN{2000 + i}",
                "merchant_id": f"M{(i % 10) + 1:03}",
                "amount": round(100 + i * 10.5, 2),
                "date": f"2024-0{(i % 6) + 1}-{(i % 28) + 1:02d}",
                "status": "success" if i % 7 != 0 else "failed",
                "currency": "INR"
            })
        pd.DataFrame(records).to_csv("data/transactions_cleaned.csv", index=False)

    if not os.path.exists("data/settlements.csv"):
        print("Generating synthetic settlements data...")
        txn_df = pd.read_csv("data/transactions_cleaned.csv")
        settlements = []
        for _, row in txn_df.iterrows():
            # Introduce some mismatches intentionally
            settled_amount = row["amount"] if np.random.rand() > 0.15 else round(row["amount"] - np.random.uniform(1, 50), 2)
            settlements.append({
                "transaction_id": row["transaction_id"],
                "settled_amount": settled_amount,
                "settlement_date": row["date"],
                "settlement_status": "settled" if row["status"] == "success" else "not_settled"
            })
        pd.DataFrame(settlements).to_csv("data/settlements.csv", index=False)

    transactions = pd.read_csv("data/transactions_cleaned.csv")
    settlements = pd.read_csv("data/settlements.csv")
    print(f"Loaded {len(transactions)} transactions and {len(settlements)} settlements.")
    return transactions, settlements


def reconcile(transactions, settlements):
    """Merge and compare transactions vs settlements."""

    # Only reconcile successful transactions
    success_txns = transactions[transactions["status"] == "success"].copy()

    merged = success_txns.merge(settlements, on="transaction_id", how="left")

    # Flag types
    merged["is_missing_settlement"] = merged["settled_amount"].isna()
    merged["amount_mismatch"] = (
        ~merged["is_missing_settlement"] &
        (merged["amount"].round(2) != merged["settled_amount"].round(2))
    )
    merged["discrepancy"] = merged["amount"] - merged["settled_amount"].fillna(0)
    merged["reconciled"] = ~merged["is_missing_settlement"] & ~merged["amount_mismatch"]

    return merged


def generate_report(merged):
    """Print and save reconciliation report."""

    total = len(merged)
    reconciled = merged["reconciled"].sum()
    mismatches = merged["amount_mismatch"].sum()
    missing = merged["is_missing_settlement"].sum()

    print("\n========== RECONCILIATION REPORT ==========")
    print(f"Report Date       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Transactions: {total}")
    print(f"Reconciled        : {reconciled} ({100*reconciled/total:.1f}%)")
    print(f"Amount Mismatches : {mismatches}")
    print(f"Missing Settlement: {missing}")
    print(f"Total Discrepancy : ₹{merged['discrepancy'].sum():,.2f}")
    print("============================================\n")

    # Save mismatch report
    issues = merged[merged["amount_mismatch"] | merged["is_missing_settlement"]].copy()
    issues["issue_type"] = np.where(
        issues["is_missing_settlement"], "Missing Settlement",
        np.where(issues["amount_mismatch"], "Amount Mismatch", "OK")
    )

    os.makedirs("data", exist_ok=True)
    issues.to_csv("data/reconciliation_issues.csv", index=False)
    merged.to_csv("data/reconciliation_full.csv", index=False)

    print(f"Issues saved to: data/reconciliation_issues.csv")
    print(f"Full report saved to: data/reconciliation_full.csv")

    return issues


def main():
    transactions, settlements = load_data()
    merged = reconcile(transactions, settlements)
    issues = generate_report(merged)

    if len(issues) > 0:
        print(f"\nSample Issues:\n")
        print(issues[["transaction_id", "merchant_id", "amount", "settled_amount", "discrepancy", "issue_type"]].head(10).to_string(index=False))
    else:
        print("All transactions reconciled successfully!")


if __name__ == "__main__":
    main()
