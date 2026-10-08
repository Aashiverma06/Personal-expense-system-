import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app.database import get_db

class FinancialAnalyticsService:
    """
    Pandas-powered financial analytics and statistical intelligence engine for PEIS.
    """

    @staticmethod
    def _load_user_transactions_df(user_id: int) -> pd.DataFrame:
        """Loads all transactions for a user into a Pandas DataFrame."""
        conn = get_db()
        query = """
            SELECT transaction_id, user_id, type, amount, category, 
                   description, payment_method, date, is_auto_categorized, 
                   categorization_method, created_at
            FROM transactions 
            WHERE user_id = ?
            ORDER BY date DESC
        """
        df = pd.read_sql_query(query, conn, params=(user_id,))
        conn.close()

        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            df["year"] = df["date"].dt.year
            df["month"] = df["date"].dt.month
            df["day"] = df["date"].dt.day
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
        return df

    @classmethod
    def get_monthly_overview(cls, user_id: int, year: int, month: int) -> dict:
        """
        Computes comprehensive monthly financial metrics and month-over-month delta.
        """
        df = cls._load_user_transactions_df(user_id)
        if df.empty:
            return {
                "income": 0.0,
                "expense": 0.0,
                "balance": 0.0,
                "savings_rate": 0.0,
                "prev_income": 0.0,
                "prev_expense": 0.0,
                "expense_growth_rate": 0.0,
                "income_growth_rate": 0.0,
                "year": year,
                "month": month
            }

        # Current month slice
        curr_mask = (df["year"] == year) & (df["month"] == month)
        curr_df = df[curr_mask]

        income = float(curr_df[curr_df["type"] == "income"]["amount"].sum())
        expense = float(curr_df[curr_df["type"] == "expense"]["amount"].sum())
        balance = income - expense
        savings_rate = round((balance / income * 100), 1) if income > 0 else 0.0

        # Previous month
        if month == 1:
            prev_m, prev_y = 12, year - 1
        else:
            prev_m, prev_y = month - 1, year

        prev_mask = (df["year"] == prev_y) & (df["month"] == prev_m)
        prev_df = df[prev_mask]

        prev_income = float(prev_df[prev_df["type"] == "income"]["amount"].sum())
        prev_expense = float(prev_df[prev_df["type"] == "expense"]["amount"].sum())

        expense_growth_rate = 0.0
        if prev_expense > 0:
            expense_growth_rate = round(((expense - prev_expense) / prev_expense) * 100, 1)

        income_growth_rate = 0.0
        if prev_income > 0:
            income_growth_rate = round(((income - prev_income) / prev_income) * 100, 1)

        return {
            "income": round(income, 2),
            "expense": round(expense, 2),
            "balance": round(balance, 2),
            "savings_rate": savings_rate,
            "prev_income": round(prev_income, 2),
            "prev_expense": round(prev_expense, 2),
            "expense_growth_rate": expense_growth_rate,
            "income_growth_rate": income_growth_rate,
            "year": year,
            "month": month
        }

    @classmethod
    def get_category_spending_breakdown(cls, user_id: int, year: int, month: int) -> list:
        """
        Category-wise expense breakdown with totals, percentage share, and count.
        """
        df = cls._load_user_transactions_df(user_id)
        if df.empty:
            return []

        curr_mask = (df["year"] == year) & (df["month"] == month) & (df["type"] == "expense")
        expense_df = df[curr_mask]

        if expense_df.empty:
            return []

        total_expense = expense_df["amount"].sum()
        grouped = expense_df.groupby("category").agg(
            amount=("amount", "sum"),
            count=("transaction_id", "count")
        ).reset_index()

        grouped["percentage"] = (grouped["amount"] / total_expense * 100).round(1)
        grouped = grouped.sort_values(by="amount", ascending=False)

        return grouped.to_dict(orient="records")

    @classmethod
    def get_spending_trends(cls, user_id: int, num_months: int = 6) -> dict:
        """
        Returns multi-month income vs expense time series for trend charts.
        """
        df = cls._load_user_transactions_df(user_id)
        labels = []
        income_data = []
        expense_data = []

        now = datetime.now()
        # Generate target month periods chronologically
        periods = []
        for i in range(num_months - 1, -1, -1):
            target_date = now - timedelta(days=i * 30)
            periods.append((target_date.year, target_date.month))

        # Deduplicate while preserving order
        seen = set()
        dedup_periods = []
        for y, m in periods:
            if (y, m) not in seen:
                seen.add((y, m))
                dedup_periods.append((y, m))

        for y, m in dedup_periods:
            month_label = datetime(y, m, 1).strftime("%b %Y")
            labels.append(month_label)

            if df.empty:
                income_data.append(0.0)
                expense_data.append(0.0)
            else:
                m_slice = df[(df["year"] == y) & (df["month"] == m)]
                inc = float(m_slice[m_slice["type"] == "income"]["amount"].sum())
                exp = float(m_slice[m_slice["type"] == "expense"]["amount"].sum())
                income_data.append(round(inc, 2))
                expense_data.append(round(exp, 2))

        return {
            "labels": labels,
            "income": income_data,
            "expenses": expense_data
        }

    @classmethod
    def get_payment_method_distribution(cls, user_id: int, year: int, month: int) -> list:
        """
        Aggregates expense distribution by payment method (UPI, Card, Cash, etc.).
        """
        df = cls._load_user_transactions_df(user_id)
        if df.empty:
            return []

        curr_mask = (df["year"] == year) & (df["month"] == month) & (df["type"] == "expense")
        expense_df = df[curr_mask]

        if expense_df.empty:
            return []

        grouped = expense_df.groupby("payment_method").agg(
            amount=("amount", "sum"),
            count=("transaction_id", "count")
        ).reset_index().sort_values(by="amount", ascending=False)

        return grouped.to_dict(orient="records")

    @classmethod
    def detect_anomalies(cls, user_id: int, year: int, month: int, z_threshold: float = 2.0) -> list:
        """
        Statistical anomaly detection for transactions:
        Computes category-wise baseline statistics and flags unusually high expenses.
        """
        df = cls._load_user_transactions_df(user_id)
        if df.empty:
            return []

        expense_df = df[df["type"] == "expense"].copy()
        if len(expense_df) < 5:
            return []

        # Find historical baselines per category (excluding current month or across all history)
        anomalies = []
        curr_mask = (expense_df["year"] == year) & (expense_df["month"] == month)
        curr_expenses = expense_df[curr_mask]

        for _, row in curr_expenses.iterrows():
            cat = row["category"]
            cat_history = expense_df[expense_df["category"] == cat]["amount"]
            
            if len(cat_history) >= 3:
                mean = cat_history.mean()
                std = cat_history.std()
                amt = row["amount"]

                # Statistical flag condition
                is_anomaly = False
                reason = ""

                if std > 0 and (amt - mean) / std > z_threshold:
                    multiplier = round(amt / mean, 1)
                    is_anomaly = True
                    reason = f"Transaction amount of ₹{amt:,.2f} is {multiplier}x higher than your average {cat} expense (₹{mean:,.2f})."
                elif amt > (mean * 2.5) and amt > 1000:
                    multiplier = round(amt / mean, 1)
                    is_anomaly = True
                    reason = f"Unusual spike detected: ₹{amt:,.2f} is {multiplier}x above normal {cat} baseline."

                if is_anomaly:
                    anomalies.append({
                        "transaction_id": int(row["transaction_id"]),
                        "amount": float(amt),
                        "category": cat,
                        "description": row["description"] or "Unnamed transaction",
                        "date": row["date"].strftime("%Y-%m-%d"),
                        "reason": reason,
                        "severity": "warning" if amt < 5000 else "danger"
                    })

        return anomalies
