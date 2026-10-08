from flask import Blueprint, render_template, g, jsonify, request
from datetime import datetime
from app.routes.auth import login_required
from app.services.analytics import FinancialAnalyticsService
from app.services.insights_engine import IntelligentInsightsEngine
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.budget import Budget

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    """Main application dashboard view."""
    now = datetime.now()
    year = int(request.args.get("year", now.year))
    month = int(request.args.get("month", now.month))

    # Financial overview
    overview = FinancialAnalyticsService.get_monthly_overview(g.user.user_id, year, month)
    category_breakdown = FinancialAnalyticsService.get_category_spending_breakdown(g.user.user_id, year, month)
    spending_trends = FinancialAnalyticsService.get_spending_trends(g.user.user_id, num_months=6)
    
    # Intelligent insights
    insights = IntelligentInsightsEngine.generate_user_insights(g.user.user_id, year, month)

    # Budgets status
    budgets = Budget.get_budgets_with_spending(g.user.user_id, month, year)

    # Recent transactions
    recent_transactions = Transaction.search(user_id=g.user.user_id, limit=8)

    # Categories for quick add
    categories = Category.get_all(user_id=g.user.user_id)

    return render_template(
        "dashboard.html",
        overview=overview,
        category_breakdown=category_breakdown,
        spending_trends=spending_trends,
        insights=insights,
        budgets=budgets,
        recent_transactions=recent_transactions,
        categories=categories,
        year=year,
        month=month,
        current_year=now.year,
        current_month=now.month,
        today=now.strftime("%Y-%m-%d")
    )

@dashboard_bp.route("/api/chart-data")
@login_required
def chart_data():
    """API endpoint returning fresh Chart.js data for dashboard async update."""
    now = datetime.now()
    year = int(request.args.get("year", now.year))
    month = int(request.args.get("month", now.month))

    category_breakdown = FinancialAnalyticsService.get_category_spending_breakdown(g.user.user_id, year, month)
    spending_trends = FinancialAnalyticsService.get_spending_trends(g.user.user_id, num_months=6)

    return jsonify({
        "categories": {
            "labels": [c["category"] for c in category_breakdown],
            "data": [c["amount"] for c in category_breakdown]
        },
        "trends": spending_trends
    })
