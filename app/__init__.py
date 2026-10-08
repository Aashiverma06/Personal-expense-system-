import os
from flask import Flask
from app.config import config
from app.database import init_db
from app.services.categorizer import get_categorizer

def create_app(config_name=None):
    """Flask application factory."""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["default"]))

    # Initialize SQLite database
    init_db(app.config["DATABASE_PATH"])

    # Ensure model is initialized
    with app.app_context():
        try:
            get_categorizer()
        except Exception as e:
            app.logger.warning(f"Categorizer initialization warning: {e}")

    # Register Jinja custom filters
    @app.template_filter("currency")
    def format_currency(value, symbol="₹"):
        try:
            val = float(value)
            return f"{symbol}{val:,.2f}"
        except (ValueError, TypeError):
            return f"{symbol}0.00"

    @app.template_filter("percent")
    def format_percent(value):
        try:
            val = float(value)
            return f"{val:.1f}%"
        except (ValueError, TypeError):
            return "0.0%"

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.transactions import transactions_bp
    from app.routes.budgets import budgets_bp
    from app.routes.intelligence import intelligence_bp
    from app.routes.reports import reports_bp
    from app.routes.experiment import experiment_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(budgets_bp)
    app.register_blueprint(intelligence_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(experiment_bp)

    return app
