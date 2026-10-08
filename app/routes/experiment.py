from flask import Blueprint, render_template, request, jsonify
from app.routes.auth import login_required
from app.services.experiment_service import ResearchExperimentService

experiment_bp = Blueprint("experiment", __name__, url_prefix="/experiment")

@experiment_bp.route("/")
@login_required
def index():
    """
    Research Experiment View:
    Presents empirical comparison of Manual vs Rule-Based vs Machine Learning categorization.
    """
    benchmark_results = ResearchExperimentService.run_benchmark_experiment()
    return render_template(
        "experiment.html",
        benchmark=benchmark_results
    )

@experiment_bp.route("/api/test-prompt", methods=["POST"])
@login_required
def test_prompt():
    """
    Live interactive test console for testing arbitrary expense descriptions
    against both Rule-Based and ML classifiers with millisecond execution timing.
    """
    data = request.get_json(silent=True) or request.form
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"success": False, "error": "Please provide an expense description to test."}), 400

    result = ResearchExperimentService.test_single_prompt(text)
    return jsonify({
        "success": True,
        "result": result
    })
