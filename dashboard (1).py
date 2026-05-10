"""
QuickPay FinTech - Business Monitoring Dashboard
Task: Create visual dashboard for business monitoring
Run: python dashboard/dashboard.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os


def get_data():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists("data/transactions_cleaned.csv"):
        print("Generating synthetic data for dashboard...")
        import random
        from datetime import datetime, timedelta

        records = []
        for i in range(300):
            records.append({
                "transaction_id": f"TXN{4000 + i}",
                "merchant_id": f"M{random.randint(1, 8):03}",
                "amount": round(random.uniform(50, 8000), 2),
                "date": (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d"),
                "status": random.choices(
                    ["success", "failed", "pending", "refunded"],
                    weights=[70, 15, 10, 5]
                )[0],
                "currency": "INR"
            })
        pd.DataFrame(records).to_csv("data/transactions_cleaned.csv", index=False)

    df = pd.read_csv("data/transactions_cleaned.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


def build_dashboard(df):
    fig = plt.figure(figsize=(18, 12), facecolor="#0f1117")
    fig.suptitle("QuickPay FinTech — Business Monitoring Dashboard",
                 fontsize=20, fontweight="bold", color="white", y=0.98)

    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

    ACCENT = "#00e5a0"
    RED    = "#ff4d6d"
    YELLOW = "#ffd166"
    BLUE   = "#4cc9f0"
    BG     = "#1a1d2e"
    TEXT   = "#e0e0e0"

    def ax_style(ax, title):
        ax.set_facecolor(BG)
        ax.tick_params(colors=TEXT, labelsize=8)
        ax.set_title(title, color=TEXT, fontsize=10, fontweight="bold", pad=8)
        for spine in ax.spines.values():
            spine.set_edgecolor("#333355")

   
    kpis = [
        ("Total Revenue", f"₹{df[df['status']=='success']['amount'].sum():,.0f}", ACCENT),
        ("Transactions", str(len(df)), BLUE),
        ("Failed Txns", str((df['status']=='failed').sum()), RED),
    ]
    for i, (label, value, color) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, i])
        ax.set_facecolor(BG)
        for spine in ax.spines.values():
            spine.set_edgecolor(color)
            spine.set_linewidth(2)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.5, 0.65, value, ha="center", va="center",
                fontsize=26, fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.5, 0.25, label, ha="center", va="center",
                fontsize=11, color=TEXT, transform=ax.transAxes)

   
    ax1 = fig.add_subplot(gs[1, :2])
    ax_style(ax1, "Revenue by Merchant (Successful Txns)")
    rev = df[df["status"] == "success"].groupby("merchant_id")["amount"].sum().sort_values(ascending=False)
    bars = ax1.bar(rev.index, rev.values, color=ACCENT, edgecolor="#0f1117", linewidth=0.5)
    ax1.set_ylabel("Amount (₹)", color=TEXT, fontsize=8)
    ax1.set_xlabel("Merchant ID", color=TEXT, fontsize=8)
    ax1.yaxis.label.set_color(TEXT)

   
    ax2 = fig.add_subplot(gs[1, 2])
    ax_style(ax2, "Transaction Status Split")
    status_counts = df["status"].value_counts()
    colors_pie = [ACCENT, RED, YELLOW, BLUE]
    wedges, texts, autotexts = ax2.pie(
        status_counts.values, labels=status_counts.index,
        autopct="%1.1f%%", colors=colors_pie[:len(status_counts)],
        textprops={"color": TEXT, "fontsize": 8},
        wedgeprops={"width": 0.5}
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(7)

    
    ax3 = fig.add_subplot(gs[2, :2])
    ax_style(ax3, "Daily Transaction Volume Trend")
    daily = df.groupby("date")["amount"].sum()
    ax3.plot(daily.index, daily.values, color=BLUE, linewidth=1.5)
    ax3.fill_between(daily.index, daily.values, alpha=0.15, color=BLUE)
    ax3.set_ylabel("Volume (₹)", color=TEXT, fontsize=8)
    ax3.set_xlabel("Date", color=TEXT, fontsize=8)

    
    ax4 = fig.add_subplot(gs[2, 2])
    ax_style(ax4, "Failure Rate by Merchant (%)")
    failure_rate = (
        df.groupby("merchant_id")
        .apply(lambda x: 100 * (x["status"] == "failed").sum() / len(x))
        .sort_values(ascending=True)
    )
    ax4.barh(failure_rate.index, failure_rate.values, color=RED, edgecolor="#0f1117")
    ax4.set_xlabel("Failure Rate (%)", color=TEXT, fontsize=8)

    os.makedirs("dashboard", exist_ok=True)
    plt.savefig("dashboard/quickpay_dashboard.png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print("\nDashboard saved to: dashboard/quickpay_dashboard.png")
    plt.show()


def main():
    df = get_data()
    print(f"Building dashboard with {len(df)} transactions...")
    build_dashboard(df)


if __name__ == "__main__":
    main()
