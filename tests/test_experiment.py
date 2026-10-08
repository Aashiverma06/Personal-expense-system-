from app.services.experiment_service import ResearchExperimentService

def test_research_experiment_benchmark():
    """Verify empirical research evaluation runner."""
    results = ResearchExperimentService.run_benchmark_experiment()

    assert "metrics_summary" in results
    assert "comparison_samples" in results
    assert len(results["metrics_summary"]) == 3
    assert len(results["comparison_samples"]) == 30

    # Ensure ML accuracy and Rule accuracy are calculated numbers
    rule_metric = next(m for m in results["metrics_summary"] if "Rule-Based" in m["method"])
    ml_metric = next(m for m in results["metrics_summary"] if "Machine Learning" in m["method"])

    assert isinstance(rule_metric["accuracy_pct"], (int, float))
    assert isinstance(ml_metric["accuracy_pct"], (int, float))
    assert rule_metric["accuracy_pct"] > 50.0
    assert ml_metric["accuracy_pct"] > 70.0

def test_live_prompt_test():
    """Verify live inference comparison on single prompt."""
    res = ResearchExperimentService.test_single_prompt("Ordered pizza from Domino's")
    assert res["rule_based"]["category"] == "Food & Dining"
    assert res["machine_learning"]["category"] == "Food & Dining"
    assert res["hybrid_recommendation"]["category"] == "Food & Dining"
