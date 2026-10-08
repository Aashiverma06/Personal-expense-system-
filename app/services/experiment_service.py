import time
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from app.data.default_dataset import BENCHMARK_TEST_DATA
from app.services.categorizer import get_categorizer

class ResearchExperimentService:
    """
    Scientific experimentation engine for comparing:
    - Manual Categorization (simulated baseline with user cognitive overhead)
    - Keyword/Rule-Based Categorization
    - Machine Learning Categorization (TF-IDF + Logistic Regression)
    """

    @classmethod
    def run_benchmark_experiment(cls) -> dict:
        """
        Runs rigorous empirical evaluation on the held-out benchmark test dataset.
        Computes Accuracy, Macro F1, Average Latency, and individual prediction logs.
        """
        categorizer = get_categorizer()
        test_samples = BENCHMARK_TEST_DATA

        descriptions = [item[0] for item in test_samples]
        y_true = [item[1] for item in test_samples]

        # 1. Evaluate Rule-Based Model
        rule_preds = []
        rule_latencies = []
        rule_details = []

        for desc, true_cat in zip(descriptions, y_true):
            t0 = time.perf_counter()
            res = categorizer.predict_rule_based(desc)
            t1 = time.perf_counter()
            
            rule_preds.append(res["category"])
            rule_latencies.append((t1 - t0) * 1000)  # ms
            rule_details.append({
                "description": desc,
                "ground_truth": true_cat,
                "predicted": res["category"],
                "confidence": res["confidence"],
                "is_correct": (res["category"] == true_cat),
                "matched_keywords": res.get("matched_keywords", [])
            })

        rule_acc = accuracy_score(y_true, rule_preds)
        rule_p, rule_r, rule_f1, _ = precision_recall_fscore_support(
            y_true, rule_preds, average="macro", zero_division=0
        )
        avg_rule_latency = sum(rule_latencies) / len(rule_latencies)

        # 2. Evaluate ML Model
        ml_preds = []
        ml_latencies = []
        ml_details = []

        for desc, true_cat in zip(descriptions, y_true):
            t0 = time.perf_counter()
            res = categorizer.predict_ml(desc)
            t1 = time.perf_counter()

            ml_preds.append(res["category"])
            ml_latencies.append((t1 - t0) * 1000)
            ml_details.append({
                "description": desc,
                "ground_truth": true_cat,
                "predicted": res["category"],
                "confidence": res["confidence"],
                "is_correct": (res["category"] == true_cat)
            })

        ml_acc = accuracy_score(y_true, ml_preds)
        ml_p, ml_r, ml_f1, _ = precision_recall_fscore_support(
            y_true, ml_preds, average="macro", zero_division=0
        )
        avg_ml_latency = sum(ml_latencies) / len(ml_latencies)

        # Combine into detailed sample-by-sample comparison
        comparison_table = []
        for i in range(len(descriptions)):
            comparison_table.append({
                "id": i + 1,
                "description": descriptions[i],
                "ground_truth": y_true[i],
                "rule_pred": rule_preds[i],
                "rule_correct": (rule_preds[i] == y_true[i]),
                "ml_pred": ml_preds[i],
                "ml_correct": (ml_preds[i] == y_true[i]),
                "ml_confidence": ml_details[i]["confidence"]
            })

        # Unique labels in dataset for summary
        unique_labels = sorted(list(set(y_true)))

        return {
            "dataset_info": {
                "total_test_samples": len(test_samples),
                "num_classes": len(unique_labels),
                "classes": unique_labels
            },
            "metrics_summary": [
                {
                    "method": "Manual Categorization",
                    "accuracy_pct": "Variable (User dependent)",
                    "f1_score": "N/A",
                    "avg_latency_ms": "~3,000 - 5,000 ms (Human)",
                    "scalability": "Poor (Manual effort)",
                    "notes": "Prone to typos, inconsistency, and fatigue"
                },
                {
                    "method": "Rule-Based Keyword Matching",
                    "accuracy_pct": round(rule_acc * 100, 2),
                    "f1_score": round(rule_f1, 3),
                    "avg_latency_ms": round(avg_rule_latency, 3),
                    "scalability": "Moderate (Requires maintaining dictionary)",
                    "notes": "Fails on unseen phrases, misspellings, or novel phrasing"
                },
                {
                    "method": "Machine Learning (TF-IDF + Logistic Reg)",
                    "accuracy_pct": round(ml_acc * 100, 2),
                    "f1_score": round(ml_f1, 3),
                    "avg_latency_ms": round(avg_ml_latency, 3),
                    "scalability": "High (Generalizes from text features)",
                    "notes": "Handles unseen variations, learns probabilistic associations"
                }
            ],
            "comparison_samples": comparison_table
        }

    @classmethod
    def test_single_prompt(cls, text: str) -> dict:
        """
        Runs live comparison on user-submitted text prompt.
        """
        categorizer = get_categorizer()

        t0 = time.perf_counter()
        rule_res = categorizer.predict_rule_based(text)
        t1 = time.perf_counter()
        ml_res = categorizer.predict_ml(text)
        t2 = time.perf_counter()
        hybrid_res = categorizer.predict_hybrid(text)

        return {
            "input_text": text,
            "rule_based": {
                "category": rule_res["category"],
                "confidence": rule_res["confidence"],
                "explanation": rule_res["explanation"],
                "latency_ms": round((t1 - t0) * 1000, 2)
            },
            "machine_learning": {
                "category": ml_res["category"],
                "confidence": ml_res["confidence"],
                "explanation": ml_res["explanation"],
                "alternatives": ml_res.get("alternatives", []),
                "latency_ms": round((t2 - t1) * 1000, 2)
            },
            "hybrid_recommendation": {
                "category": hybrid_res["category"],
                "confidence": hybrid_res["confidence"],
                "method": hybrid_res["method"],
                "explanation": hybrid_res["explanation"]
            }
        }
