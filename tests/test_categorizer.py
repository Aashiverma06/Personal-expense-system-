from app.services.categorizer import get_categorizer

def test_rule_based_categorizer():
    """Verify keyword mapping rules."""
    cat = get_categorizer()

    # Food
    res = cat.predict_rule_based("Ordered pizza from Domino's")
    assert res["category"] == "Food & Dining"
    assert res["confidence"] >= 0.70

    # Transport
    res = cat.predict_rule_based("Uber ride to college campus")
    assert res["category"] == "Transportation"

    # Education
    res = cat.predict_rule_based("Enrolled in python course on Udemy")
    assert res["category"] == "Education"

    # Entertainment
    res = cat.predict_rule_based("Movie tickets at PVR cinemas")
    assert res["category"] == "Entertainment"

def test_ml_categorizer():
    """Verify machine learning model predictions."""
    cat = get_categorizer()

    # Complex phrasing
    res = cat.predict_ml("Supermarket grocery bill organic milk bread")
    assert res["category"] == "Food & Dining"
    assert res["confidence"] > 0.15
    assert "alternatives" in res

def test_hybrid_engine():
    """Verify hybrid decision logic."""
    cat = get_categorizer()
    res = cat.predict_hybrid("Starbucks cold brew coffee")
    assert res["category"] == "Food & Dining"
    assert res["confidence"] > 0.75
