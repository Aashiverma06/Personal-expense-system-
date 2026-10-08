from datetime import datetime
from app.database import get_db
from app.services.analytics import FinancialAnalyticsService

class IntelligentInsightsEngine:
    """
    Decision-support and automated financial intelligence engine for PEIS.
    Analyzes historical records, budget allocations, and spending patterns to
    generate personalized recommendations, trend analyses, and budget alerts.
    """

    @classmethod
    def generate_user_insights(cls, user_id: int, year: int = None, month: int = None) -> list:
        """
        Synthesizes rule-based & statistical financial insights for a given user & month.
        """
        now = datetime.now()
        year = year or now.year
        month = month or now.month

        insights = []

        # 1. Fetch overview statistics
        overview = FinancialAnalyticsService.get_monthly_overview(user_id, year, month)
        categories = FinancialAnalyticsService.get_category_spending_breakdown(user_id, year, month)
        
        income = overview["income"]
        expense = overview["expense"]
        balance = overview["balance"]
        savings_rate = overview["savings_rate"]
        expense_growth = overview["expense_growth_rate"]

        # Insight Rule A: Month-over-Month Spending Trend
        if overview["prev_expense"] > 0:
            if expense_growth > 10.0:
                insights.append({
                    "type": "trend",
                    "title": "Spending Trend Alert",
                    "message": f"Your spending increased by {expense_growth}% compared to last month (₹{expense:,.2f} vs ₹{overview['prev_expense']:,.2f}).",
                    "severity": "warning",
                    "icon": "trending-up"
                })
            elif expense_growth < -5.0:
                insights.append({
                    "type": "trend",
                    "title": "Spending Reduction",
                    "message": f"Excellent discipline! Your expenses decreased by {abs(expense_growth)}% compared to last month.",
                    "severity": "success",
                    "icon": "trending-down"
                })

        # Insight Rule B: Savings Health Assessment (50/30/20 benchmark)
        if income > 0:
            if savings_rate >= 50.0:
                insights.append({
                    "type": "saving_tip",
                    "title": "Super Saver Milestone",
                    "message": f"You saved {savings_rate}% of your income this month! You are well ahead of the standard 20% savings target.",
                    "severity": "success",
                    "icon": "award"
                })
            elif savings_rate >= 20.0:
                insights.append({
                    "type": "saving_tip",
                    "title": "Healthy Savings Rate",
                    "message": f"You are currently saving {savings_rate}% of your total earnings (₹{balance:,.2f} retained).",
                    "severity": "info",
                    "icon": "check-circle"
                })
            elif savings_rate > 0:
                insights.append({
                    "type": "saving_tip",
                    "title": "Low Savings Rate",
                    "message": f"Your current savings rate is only {savings_rate}%. Financial experts recommend saving at least 20% of net income.",
                    "severity": "warning",
                    "icon": "alert-circle"
                })
            else:
                insights.append({
                    "type": "saving_tip",
                    "title": "Deficit Alert",
                    "message": f"You are in a deficit of ₹{abs(balance):,.2f} this month. Expenses exceed your earnings.",
                    "severity": "danger",
                    "icon": "alert-triangle"
                })

        # Insight Rule C: Category Dominance Analysis
        if categories:
            top_cat = categories[0]
            if top_cat["percentage"] >= 30.0:
                insights.append({
                    "type": "behavior",
                    "title": "Top Spending Category",
                    "message": f"{top_cat['category']} is your highest expense category, representing {top_cat['percentage']}% (₹{top_cat['amount']:,.2f}) of your total spending.",
                    "severity": "info",
                    "icon": "pie-chart"
                })

        # Insight Rule D: Budget Utilization & Warning Flags
        conn = get_db()
        budgets_cursor = conn.cursor()
        budgets_cursor.execute(
            "SELECT category, amount FROM budgets WHERE user_id = ? AND month = ? AND year = ?",
            (user_id, month, year)
        )
        user_budgets = {row["category"]: row["amount"] for row in budgets_cursor.fetchall()}
        conn.close()

        for cat_info in categories:
            cat_name = cat_info["category"]
            cat_spent = cat_info["amount"]

            if cat_name in user_budgets:
                b_limit = user_budgets[cat_name]
                utilization = (cat_spent / b_limit) * 100

                if utilization > 100.0:
                    exceeded_amt = cat_spent - b_limit
                    insights.append({
                        "type": "budget_warning",
                        "title": f"Budget Exceeded: {cat_name}",
                        "message": f"You exceeded your {cat_name} budget by ₹{exceeded_amt:,.2f} ({int(utilization)}% spent of ₹{b_limit:,.2f}).",
                        "severity": "danger",
                        "icon": "alert-octagon"
                    })
                elif utilization >= 80.0:
                    remaining_amt = b_limit - cat_spent
                    insights.append({
                        "type": "budget_warning",
                        "title": f"Budget Warning: {cat_name}",
                        "message": f"You have utilized {int(utilization)}% of your {cat_name} budget. Only ₹{remaining_amt:,.2f} remaining.",
                        "severity": "warning",
                        "icon": "alert-triangle"
                    })

        # Insight Rule E: Actionable Saving Recommendations
        # Find discretionary categories with high spend
        discretionary = ["Entertainment", "Shopping", "Food & Dining"]
        discretionary_spend = [c for c in categories if c["category"] in discretionary and c["amount"] > 1500]
        if discretionary_spend:
            target = discretionary_spend[0]
            suggested_cut = round(target["amount"] * 0.20, -1)  # 20% cut rounded
            potential_saving = suggested_cut
            new_savings_rate = round(((balance + potential_saving) / income * 100), 1) if income > 0 else 0.0

            insights.append({
                "type": "recommendation",
                "title": "Personalized Saving Recommendation",
                "message": f"Trimming your {target['category']} expenses by ₹{suggested_cut:,.0f}/month could elevate your savings to {new_savings_rate}%.",
                "severity": "info",
                "icon": "dollar-sign"
            })

        # Insight Rule F: Statistical Anomalies
        anomalies = FinancialAnalyticsService.detect_anomalies(user_id, year, month)
        for anom in anomalies[:2]:  # Limit top 2 anomalies
            insights.append({
                "type": "anomaly",
                "title": f"Unusual Spending in {anom['category']}",
                "message": anom["reason"],
                "severity": anom["severity"],
                "icon": "zap"
            })

        return insights

    @classmethod
    def sync_insights_to_db(cls, user_id: int):
        """
        Saves fresh insights into the database table for persistence.
        """
        insights = cls.generate_user_insights(user_id)
        conn = get_db()
        cursor = conn.cursor()

        # Clean old automated insights for this user
        cursor.execute("DELETE FROM insights WHERE user_id = ?", (user_id,))
        for ins in insights:
            cursor.execute(
                """INSERT INTO insights (user_id, type, title, message, severity)
                   VALUES (?, ?, ?, ?, ?)""",
                (user_id, ins["type"], ins["title"], ins["message"], ins["severity"])
            )
        conn.commit()
        conn.close()
        return insights
