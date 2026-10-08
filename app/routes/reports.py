from flask import Blueprint, render_template, request, g
from datetime import datetime, timedelta
import pandas as pd
from app.routes.auth import login_required
from app.database import get_db
from app.services.analytics import FinancialAnalyticsService

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

@reports_bp.route("/")
@login_required
def index():
    """Comprehensive Financial Reports view."""
    now = datetime.now()
    report_type = request.args.get("type", "monthly")
    year = int(request.args.get("year", now.year))
    month = int(request.args.get("month", now.month))

    conn = get_db()
    # Fetch base transactions for selected time frame
    if report_type == "monthly":
        date_pattern = f"{year:04d}-{month:02d}-%"
        query = "SELECT * FROM transactions WHERE user_id = ? AND date LIKE ? ORDER BY date ASC"
        cursor = conn.cursor()
        cursor.execute(query, (g.user.user_id, date_pattern))
        records = [dict(r) for r in cursor.fetchall()]
        period_title = f"{datetime(year, month, 1).strftime('%B %Y')} Monthly Financial Report"
    elif report_type == "weekly":
        # Last 7 days
        start_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")
        query = "SELECT * FROM transactions WHERE user_id = ? AND date >= ? ORDER BY date ASC"
        cursor = conn.cursor()
        cursor.execute(query, (g.user.user_id, start_date))
        records = [dict(r) for r in cursor.fetchall()]
        period_title = f"Last 7 Days (Since {start_date}) Weekly Report"
    elif report_type == "daily":
        target_day = request.args.get("day", now.strftime("%Y-%m-%d"))
        query = "SELECT * FROM transactions WHERE user_id = ? AND date = ? ORDER BY transaction_id DESC"
        cursor = conn.cursor()
        cursor.execute(query, (g.user.user_id, target_day))
        records = [dict(r) for r in cursor.fetchall()]
        period_title = f"Daily Report for {target_day}"
    else:  # Yearly
        date_pattern = f"{year:04d}-%"
        query = "SELECT * FROM transactions WHERE user_id = ? AND date LIKE ? ORDER BY date ASC"
        cursor = conn.cursor()
        cursor.execute(query, (g.user.user_id, date_pattern))
        records = [dict(r) for r in cursor.fetchall()]
        period_title = f"Annual Financial Report for {year}"

    conn.close()

    # Calculate analytics with Pandas
    total_income = sum(r["amount"] for r in records if r["type"] == "income")
    total_expense = sum(r["amount"] for r in records if r["type"] == "expense")
    net_savings = total_income - total_expense
    savings_rate = round((net_savings / total_income * 100), 1) if total_income > 0 else 0.0

    # Category summaries
    cat_summary = {}
    for r in records:
        if r["type"] == "expense":
            cat = r["category"]
            cat_summary[cat] = cat_summary.get(cat, 0.0) + r["amount"]

    sorted_cats = sorted(
        [{"category": k, "amount": round(v, 2), "percentage": round((v / total_expense * 100), 1) if total_expense > 0 else 0}
         for k, v in cat_summary.items()],
        key=lambda x: x["amount"],
        reverse=True
    )

    # Highest single expense
    expenses_only = [r for r in records if r["type"] == "expense"]
    highest_expense = max(expenses_only, key=lambda x: x["amount"]) if expenses_only else None

    # Daily expense distribution
    daily_map = {}
    for r in records:
        if r["type"] == "expense":
            d = r["date"]
            daily_map[d] = daily_map.get(d, 0.0) + r["amount"]

    daily_labels = sorted(daily_map.keys())
    daily_values = [round(daily_map[d], 2) for d in daily_labels]
    avg_daily_spend = round(total_expense / len(daily_labels), 2) if daily_labels else 0.0

    return render_template(
        "reports.html",
        records=records,
        period_title=period_title,
        report_type=report_type,
        year=year,
        month=month,
        total_income=total_income,
        total_expense=total_expense,
        net_savings=net_savings,
        savings_rate=savings_rate,
        categories=sorted_cats,
        highest_expense=highest_expense,
        daily_labels=daily_labels,
        daily_values=daily_values,
        avg_daily_spend=avg_daily_spend,
        now=now
    )
