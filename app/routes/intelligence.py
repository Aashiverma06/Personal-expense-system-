from flask import Blueprint, request, jsonify, g
from app.routes.auth import login_required
from app.services.categorizer import get_categorizer
from app.services.insights_engine import IntelligentInsightsEngine
from app.models.insight import Insight

intelligence_bp = Blueprint("intelligence", __name__, url_prefix="/api/intelligence")

@intelligence_bp.route("/categorize", methods=["POST"])
@login_required
def auto_categorize():
    """
    Real-time auto-categorization API endpoint.
    Invoked via AJAX as user types the expense description.
    """
    data = request.get_json(silent=True) or request.form
    description = data.get("description", "").strip()

    if not description:
        return jsonify({
            "success": False,
            "category": "Miscellaneous",
            "confidence": 0.0,
            "method": "none",
            "explanation": "No text provided"
        }), 400

    categorizer = get_categorizer()
    prediction = categorizer.predict_hybrid(description)

    return jsonify({
        "success": True,
        "category": prediction["category"],
        "confidence": prediction["confidence"],
        "method": prediction["method"],
        "explanation": prediction["explanation"],
        "alternatives": prediction.get("alternatives", [])
    })

@intelligence_bp.route("/insights", methods=["GET"])
@login_required
def get_insights():
    """Returns active intelligent insights for the current user."""
    insights = IntelligentInsightsEngine.generate_user_insights(g.user.user_id)
    return jsonify({
        "success": True,
        "insights": insights
    })

@intelligence_bp.route("/insights/<int:insight_id>/dismiss", methods=["POST"])
@login_required
def dismiss_insight(insight_id):
    """Marks an insight as dismissed."""
    success = Insight.dismiss(insight_id, g.user.user_id)
    return jsonify({"success": success})
