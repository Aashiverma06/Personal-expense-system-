from app.models.transaction import Transaction

def test_transaction_crud(auth_client):
    """Test full transaction CRUD operations."""
    client, user = auth_client

    # 1. Add transaction
    res = client.post("/transactions/add", data={
        "type": "expense",
        "amount": "250.00",
        "category": "Food & Dining",
        "payment_method": "UPI",
        "date": "2026-10-08",
        "description": "Domino's pizza lunch"
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Transaction recorded successfully" in res.data

    # Query DB
    txs = Transaction.search(user.user_id)
    assert len(txs) == 1
    t_id = txs[0]["transaction_id"]
    assert txs[0]["amount"] == 250.00
    assert txs[0]["category"] == "Food & Dining"

    # 2. Edit transaction
    res_edit = client.post(f"/transactions/{t_id}/edit", data={
        "type": "expense",
        "amount": "300.00",
        "category": "Food & Dining",
        "payment_method": "Cash",
        "date": "2026-10-08",
        "description": "Domino's pizza lunch with coke"
    }, follow_redirects=True)
    assert res_edit.status_code == 200

    updated = Transaction.get_by_id(t_id, user.user_id)
    assert updated["amount"] == 300.00
    assert updated["payment_method"] == "Cash"

    # 3. Delete transaction
    res_del = client.post(f"/transactions/{t_id}/delete", follow_redirects=True)
    assert res_del.status_code == 200
    assert len(Transaction.search(user.user_id)) == 0

def test_transaction_export_csv(auth_client):
    """Test CSV export endpoint."""
    client, user = auth_client
    Transaction.create(
        user_id=user.user_id,
        t_type="income",
        amount=25000.0,
        category="Salary",
        description="Monthly salary",
        payment_method="Bank Transfer",
        date="2026-10-01"
    )

    res = client.get("/transactions/export/csv")
    assert res.status_code == 200
    assert b"Monthly salary" in res.data
    assert b"25000.00" in res.data
