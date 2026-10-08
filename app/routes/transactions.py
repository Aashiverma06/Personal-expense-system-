from flask import Blueprint, render_template, request, redirect, url_for, flash, g, Response, jsonify
from datetime import datetime
from app.routes.auth import login_required
from app.models.transaction import Transaction
from app.models.category import Category
from app.services.categorizer import get_categorizer

transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")

@transactions_bp.route("/")
@login_required
def index():
    """Transaction history view with advanced filtering and pagination."""
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    t_type = request.args.get("type", "all")
    category = request.args.get("category", "all")
    payment_method = request.args.get("payment_method", "all")
    search_query = request.args.get("q", "").strip()

    transactions = Transaction.search(
        user_id=g.user.user_id,
        start_date=start_date if start_date else None,
        end_date=end_date if end_date else None,
        t_type=t_type,
        category=category,
        payment_method=payment_method,
        query=search_query if search_query else None
    )

    categories = Category.get_all(user_id=g.user.user_id)
    payment_methods = ["UPI", "Cash", "Credit Card", "Debit Card", "Bank Transfer", "Other"]

    # Compute quick filtered totals
    total_in = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_out = sum(t["amount"] for t in transactions if t["type"] == "expense")
    net_diff = total_in - total_out

    return render_template(
        "transactions.html",
        transactions=transactions,
        categories=categories,
        payment_methods=payment_methods,
        filters={
            "start_date": start_date,
            "end_date": end_date,
            "type": t_type,
            "category": category,
            "payment_method": payment_method,
            "q": search_query
        },
        summary={
            "total_income": total_in,
            "total_expense": total_out,
            "net": net_diff
        },
        today=datetime.now().strftime("%Y-%m-%d")
    )

@transactions_bp.route("/add", methods=["POST"])
@login_required
def add():
    """Add a new transaction with automatic categorization metadata."""
    t_type = request.form.get("type", "expense")
    amount = request.form.get("amount", "0")
    category = request.form.get("category", "").strip()
    payment_method = request.form.get("payment_method", "UPI")
    date = request.form.get("date", datetime.now().strftime("%Y-%m-%d"))
    description = request.form.get("description", "").strip()
    cat_method = request.form.get("categorization_method", "manual")
    is_auto = 1 if cat_method in ["rule", "ml", "hybrid (rule + ml)"] else 0

    try:
        amt = float(amount)
        if amt <= 0:
            flash("Amount must be greater than zero.", "danger")
            return redirect(url_for("transactions.index"))
    except ValueError:
        flash("Invalid amount entered.", "danger")
        return redirect(url_for("transactions.index"))

    if not category:
        # Fallback auto-categorize if user left category blank
        cat_res = get_categorizer().predict_hybrid(description)
        category = cat_res["category"]
        cat_method = cat_res["method"]
        is_auto = 1

    Transaction.create(
        user_id=g.user.user_id,
        t_type=t_type,
        amount=amt,
        category=category,
        description=description,
        payment_method=payment_method,
        date=date,
        is_auto_categorized=is_auto,
        categorization_method=cat_method
    )

    flash("Transaction recorded successfully!", "success")
    return redirect(request.referrer or url_for("transactions.index"))

@transactions_bp.route("/<int:transaction_id>/edit", methods=["POST"])
@login_required
def edit(transaction_id):
    """Update an existing transaction."""
    t_type = request.form.get("type")
    amount = request.form.get("amount")
    category = request.form.get("category")
    payment_method = request.form.get("payment_method")
    date = request.form.get("date")
    description = request.form.get("description")

    try:
        amt = float(amount) if amount else None
    except ValueError:
        flash("Invalid amount.", "danger")
        return redirect(url_for("transactions.index"))

    success = Transaction.update(
        transaction_id=transaction_id,
        user_id=g.user.user_id,
        t_type=t_type,
        amount=amt,
        category=category,
        description=description,
        payment_method=payment_method,
        date=date
    )

    if success:
        flash("Transaction updated.", "success")
    else:
        flash("Could not update transaction.", "danger")

    return redirect(url_for("transactions.index"))

@transactions_bp.route("/<int:transaction_id>/delete", methods=["POST"])
@login_required
def delete(transaction_id):
    """Delete a transaction."""
    success = Transaction.delete(transaction_id=transaction_id, user_id=g.user.user_id)
    if success:
        flash("Transaction deleted.", "info")
    else:
        flash("Transaction not found or could not be deleted.", "danger")
    return redirect(url_for("transactions.index"))

@transactions_bp.route("/export/csv")
@login_required
def export():
    """Export transactions as downloadable CSV."""
    transactions = Transaction.search(user_id=g.user.user_id)
    csv_data = Transaction.export_csv(transactions)

    filename = f"peis_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )
