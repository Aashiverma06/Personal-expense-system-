import functools
from flask import Blueprint, request, redirect, url_for, flash, session, g, render_template
from app.models.user import User
from app.database import seed_demo_data

auth_bp = Blueprint("auth", __name__)

def login_required(view):
    """Decorator to protect routes requiring authentication."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

@auth_bp.before_app_request
def load_logged_in_user():
    """Load logged-in user into Flask's `g` global context before every request."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.get_by_id(user_id)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration view."""
    if g.user:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        currency = request.form.get("currency", "₹")

        error = None
        if not name or not email or not password:
            error = "All fields are required."
        elif len(password) < 6:
            error = "Password must be at least 6 characters long."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif User.get_by_email(email):
            error = f"An account with email '{email}' already exists."

        if error is None:
            user = User.create(name=name, email=email, password=password, currency=currency)
            if user:
                session.clear()
                session["user_id"] = user.user_id
                flash(f"Welcome to PEIS, {user.name}! Your account was created successfully.", "success")
                return redirect(url_for("dashboard.index"))
            else:
                error = "Failed to create account. Please try again."

        flash(error, "danger")

    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login view."""
    if g.user:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.authenticate(email, password)
        if user:
            session.clear()
            session["user_id"] = user.user_id
            flash(f"Welcome back, {user.name}!", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("dashboard.index"))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    """Logs out the active user."""
    session.clear()
    flash("You have been securely logged out.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User profile management view."""
    if request.method == "POST":
        action = request.form.get("action")
        if action == "update_info":
            name = request.form.get("name", "").strip()
            currency = request.form.get("currency", "₹")
            if name:
                g.user.update_profile(name=name, currency=currency)
                flash("Profile details updated successfully.", "success")
            else:
                flash("Name cannot be empty.", "danger")

        elif action == "change_password":
            current_pw = request.form.get("current_password", "")
            new_pw = request.form.get("new_password", "")
            confirm_pw = request.form.get("confirm_password", "")

            if not User.authenticate(g.user.email, current_pw):
                flash("Current password is incorrect.", "danger")
            elif len(new_pw) < 6:
                flash("New password must be at least 6 characters.", "danger")
            elif new_pw != confirm_pw:
                flash("New passwords do not match.", "danger")
            else:
                g.user.change_password(new_pw)
                flash("Password changed successfully.", "success")

    return render_template("auth/profile.html", user=g.user)

@auth_bp.route("/seed-demo-data", methods=["POST"])
@login_required
def load_demo():
    """Populate sample dataset to demonstrate intelligence features."""
    success = seed_demo_data(g.user.user_id)
    if success:
        flash("Loaded demo transactions and budgets! Explore your dashboard and intelligence insights.", "success")
    else:
        flash("You already have transactions in your account. Demo data was not added.", "info")
    return redirect(url_for("dashboard.index"))
