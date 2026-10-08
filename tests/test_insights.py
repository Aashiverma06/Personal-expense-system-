from app.models.transaction import Transaction
from app.services.insights_engine import IntelligentInsightsEngine
from app.services.analytics import FinancialAnalyticsService

def test_insights_generation(auth_client):
    """Test decision-support insights generation."""
    client, user = auth_client

    # Add Income and Expenses
    Transaction.create(
        user_id=user.user_id,
        t_type="income",
        amount=50000.0,
        category="Salary",
        description="Salary pay",
        payment_method="Bank Transfer",
        date="2026-10-01"
    )

    Transaction.create(
        user_id=user.user_id,
        t_type="expense",
        amount=15000.0,
        category="Food & Dining",
        description="Dining and party",
        payment_method="UPI",
        date="2026-10-05"
    )

    # Overview check
    overview = FinancialAnalyticsService.get_monthly_overview(user.user_id, 2026, 10)
    assert overview["income"] == 50000.0
    assert overview["expense"] == 15000.0
    assert overview["balance"] == 35000.0
    assert overview["savings_rate"] == 70.0

    # Insights check
    insights = IntelligentInsightsEngine.generate_user_insights(user.user_id, 2026, 10)
    assert len(insights) > 0
    # Should include super saver milestone and food top category
    titles = [i["title"] for i in insights]
    assert any("Saver" in t for t in titles)
    assert any("Top Spending" in t for t in titles)
