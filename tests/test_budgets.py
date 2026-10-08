from app.models.budget import Budget
from app.models.transaction import Transaction

def test_budget_creation_and_tracking(auth_client):
    """Test setting budget and tracking spending against it."""
    client, user = auth_client

    # 1. Set budget
    res = client.post("/budgets/set", data={
        "category": "Food & Dining",
        "amount": "4000.00",
        "month": 10,
        "year": 2026
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Budget for &#39;Food &amp; Dining&#39; set to" in res.data or b"Budget for 'Food & Dining' set to" in res.data

    # Add expense of 3,200 (Safe status < 80%)
    Transaction.create(
        user_id=user.user_id,
        t_type="expense",
        amount=3200.0,
        category="Food & Dining",
        description="Dining out",
        payment_method="UPI",
        date="2026-10-05"
    )

    budgets = Budget.get_budgets_with_spending(user.user_id, 10, 2026)
    assert len(budgets) == 1
    assert budgets[0]["spent_amount"] == 3200.0
    assert budgets[0]["remaining_amount"] == 800.0
    assert budgets[0]["status"] == "warning"  # 80% is warning threshold

    # Exceed budget by adding another 1,000
    Transaction.create(
        user_id=user.user_id,
        t_type="expense",
        amount=1000.0,
        category="Food & Dining",
        description="Groceries",
        payment_method="UPI",
        date="2026-10-06"
    )

    budgets2 = Budget.get_budgets_with_spending(user.user_id, 10, 2026)
    assert budgets2[0]["spent_amount"] == 4200.0
    assert budgets2[0]["remaining_amount"] == -200.0
    assert budgets2[0]["status"] == "exceeded"
