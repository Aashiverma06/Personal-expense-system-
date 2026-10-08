from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from datetime import datetime
from app.routes.auth import login_required
from app.models.budget import Budget
from app.models.category import Category

budgets_bp = Blueprint("budgets", __name__, url_prefix="/budgets")

@budgets_bp.route("/")
@login_required
def index():
    """List budgets with actual spending status."""
    now = datetime.now()
    month = int(request.args.get("month", now.month))
    year = int(request.args.get("year", now.year))

    budgets = Budget.get_budgets_with_spending(
        user_id=g.user.user_id,
        month=month,
        year=year
    )

    categories = Category.get_all(user_id=g.user.user_id, cat_type="expense")

    # Overall budget summary calculations
    total_budgeted = sum(b["budget_amount"] for b in budgets)
    total_spent = sum(b["spent_amount"] for b in budgets)
    overall_pct = round((total_spent / total_budgeted * 100), 1) if total_budgeted > 0 else 0.0

    exceeded_count = sum(1 for b in budgets if b["status"] == "exceeded")
    warning_count = sum(1 for b in budgets if b["status"] == "warning")

    return render_template(
        "budgets.html",
        budgets=budgets,
        categories=categories,
        month=month,
        year=year,
        current_month=now.month,
        current_year=now.year,
        summary={
            "total_budgeted": total_budgeted,
            "total_spent": total_spent,
            "overall_pct": overall_pct,
            "exceeded_count": exceeded_count,
            "warning_count": warning_count
        }
    )

@budgets_bp.route("/set", methods=["POST"])
@login_required
def set_budget():
    """Create or update a category budget."""
    category = request.form.get("category", "").strip()
    amount = request.form.get("amount", "0")
    month = int(request.form.get("month", datetime.now().month))
    year = int(request.form.get("year", datetime.now().year))

    try:
        amt = float(amount)
        if amt <= 0:
            flash("Budget amount must be greater than zero.", "danger")
            return redirect(url_for("budgets.index", month=month, year=year))
    except ValueError:
        flash("Invalid budget amount.", "danger")
        return redirect(url_for("budgets.index", month=month, year=year))

    if not category:
        flash("Please select a category.", "danger")
        return redirect(url_for("budgets.index", month=month, year=year))

    Budget.set_budget(
        user_id=g.user.user_id,
        category=category,
        amount=amt,
        month=month,
        year=year
    )

    flash(f"Budget for '{category}' set to ₹{amt:,.2f}.", "success")
    return redirect(url_for("budgets.index", month=month, year=year))

@budgets_bp.route("/<int:budget_id>/delete", methods=["POST"])
@login_required
def delete_budget(budget_id):
    """Delete a budget item."""
    month = request.form.get("month")
    year = request.form.get("year")
    success = Budget.delete_budget(budget_id, g.user.user_id)
    if success:
        flash("Budget target removed.", "info")
    else:
        flash("Budget could not be deleted.", "danger")

    return redirect(url_for("budgets.index", month=month, year=year))
