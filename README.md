

**Role:** Data Analyst at QuickPay, a fintech company processing digital payments for merchants.

---



```
quickpay-fintech-case-study/
├── data/                        # Input and output data files (CSV, JSON)
├── scripts/
│   ├── clean_data.py            # Task 1: Data Cleaning
│   ├── reconciliation.py        # Task 3: Reconciliation Workflow
│   └── normalize_json.py        # Task 4: JSON Normalization
├── sql/
│   └── queries.sql              # Task 2: SQL Business Questions
├── dashboard/
│   └── dashboard.py             # Task 5: Business Monitoring Dashboard
└── README.md
```

---



```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/quickpay-fintech-case-study.git
cd quickpay-fintech-case-study

# Install dependencies
pip install pandas numpy matplotlib
```

---




Cleans raw transaction data: removes duplicates, handles nulls, fixes data types, standardizes status values, and removes invalid amounts.

```bash
python scripts/clean_data.py
```
**Output:** `data/transactions_cleaned.csv`

---


Answers business queries using SQL: merchant revenue, payment mismatches, daily volume, failure rates, refund analysis, and pending transactions.

**File:** `sql/queries.sql`

Run using any SQL client (SQLite, MySQL, PostgreSQL) after importing the cleaned CSV as a table.

---


Matches transactions against settlements, flags mismatches and missing settlements, calculates discrepancies.

```bash
python scripts/reconciliation.py
```
**Output:**
- `data/reconciliation_issues.csv` — flagged mismatches
- `data/reconciliation_full.csv` — complete reconciliation

---


Flattens nested API-style JSON (merchant + transactions) into a clean, analysis-ready flat CSV.

```bash
python scripts/normalize_json.py
```
**Output:** `data/normalized_transactions.csv`

---

Generates a multi-panel dashboard showing KPIs, revenue by merchant, status split, daily volume trend, and failure rates.

```bash
python dashboard/dashboard.py
```
**Output:** `dashboard/quickpay_dashboard.png`

---


|---|----------|------|
| 1 | Total revenue per merchant | `sql/queries.sql` — Q1 |
| 2 | Payment mismatches | `sql/queries.sql` — Q2, `reconciliation.py` |
| 3 | Daily transaction volume | `sql/queries.sql` — Q3 |
| 4 | Failed transaction rate | `sql/queries.sql` — Q4 |
| 5 | Monthly revenue trend | `sql/queries.sql` — Q6 |
| 6 | Refund analysis | `sql/queries.sql` — Q7 |

---



-

---

*Submitted as part of the QuickPay FinTech Operations Graded Assignment.*
