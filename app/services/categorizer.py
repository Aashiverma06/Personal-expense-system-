import re
import os
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

from app.config import Config
from app.data.default_dataset import RULE_KEYWORDS, TRAINING_DATA

class IntelligentCategorizer:
    """
    Intelligent expense categorization service supporting:
    1. Keyword & Pattern-based Rule Matching
    2. Machine Learning Text Classification (TF-IDF + Naive Bayes / Logistic Regression)
    3. Hybrid confidence ranking and explainability
    """

    def __init__(self, model_path=None):
        self.model_path = model_path or Config.MODEL_PATH
        self.rule_dict = RULE_KEYWORDS
        self.ml_pipeline = None
        self._load_or_train_model()

    def _normalize_text(self, text: str) -> str:
        """Sanitize and clean description strings."""
        if not text:
            return ""
        # Lowercase and remove punctuation except apostrophes
        text = text.lower().strip()
        text = re.sub(r"[^a-z0-9\s']", " ", text)
        return " ".join(text.split())

    def predict_rule_based(self, text: str) -> dict:
        """
        Keyword and rule-based categorization.
        Returns matched category, confidence, and matched keywords.
        """
        clean_text = self._normalize_text(text)
        tokens = set(clean_text.split())

        best_category = None
        max_matches = 0
        matched_words = []

        for category, keywords in self.rule_dict.items():
            current_matches = []
            for kw in keywords:
                # check both exact phrase substring and token overlap
                if " " in kw:
                    if kw in clean_text:
                        current_matches.append(kw)
                else:
                    if kw in tokens or kw in clean_text:
                        current_matches.append(kw)

            if len(current_matches) > max_matches:
                max_matches = len(current_matches)
                best_category = category
                matched_words = current_matches

        if best_category and max_matches > 0:
            # Rule confidence scales with number of keyword matches
            confidence = min(0.70 + (max_matches * 0.15), 0.98)
            return {
                "category": best_category,
                "confidence": round(confidence, 2),
                "method": "rule",
                "explanation": f"Matched keyword(s): {', '.join(matched_words[:3])}",
                "matched_keywords": matched_words
            }

        return {
            "category": "Miscellaneous",
            "confidence": 0.20,
            "method": "rule",
            "explanation": "No keyword pattern matched",
            "matched_keywords": []
        }

    def _load_or_train_model(self):
        """Loads serialized ML pipeline from disk, or trains on default dataset."""
        if os.path.exists(self.model_path):
            try:
                self.ml_pipeline = joblib.load(self.model_path)
                return
            except Exception:
                pass

        # Train new model
        self.train_ml_model()

    def train_ml_model(self, extra_data=None):
        """
        Trains TF-IDF + Logistic Regression / Naive Bayes pipeline
        on default training dataset plus any user-provided transaction data.
        """
        corpus = list(TRAINING_DATA)
        if extra_data:
            corpus.extend(extra_data)

        X = [self._normalize_text(text) for text, _ in corpus]
        y = [cat for _, cat in corpus]

        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=1,
                sublinear_tf=True
            )),
            ("clf", LogisticRegression(
                C=1.5,
                max_iter=1000,
                class_weight="balanced"
            ))
        ])

        pipeline.fit(X, y)
        self.ml_pipeline = pipeline

        # Save model
        try:
            model_dir = os.path.dirname(self.model_path)
            if model_dir and not os.path.exists(model_dir):
                os.makedirs(model_dir, exist_ok=True)
            joblib.dump(pipeline, self.model_path)
        except Exception:
            pass

        return pipeline

    def predict_ml(self, text: str) -> dict:
        """
        Predicts category using trained ML model and returns top probabilities.
        """
        if not self.ml_pipeline:
            self._load_or_train_model()

        clean_text = self._normalize_text(text)
        if not clean_text:
            return {
                "category": "Miscellaneous",
                "confidence": 0.2,
                "method": "ml",
                "explanation": "Empty text provided",
                "alternatives": []
            }

        classes = self.ml_pipeline.classes_
        probabilities = self.ml_pipeline.predict_proba([clean_text])[0]

        # Sort classes by probability descending
        scored = sorted(zip(classes, probabilities), key=lambda x: x[1], reverse=True)
        top_cat, top_prob = scored[0]

        alternatives = [
            {"category": cat, "confidence": round(float(prob), 3)}
            for cat, prob in scored[1:4]
        ]

        return {
            "category": top_cat,
            "confidence": round(float(top_prob), 2),
            "method": "ml",
            "explanation": f"ML model confidence: {int(top_prob * 100)}% based on text features",
            "alternatives": alternatives
        }

    def predict_hybrid(self, text: str) -> dict:
        """
        Hybrid Intelligence Engine:
        Evaluates both Rule-based and Machine Learning predictions.
        Combines confidence scores to deliver the most accurate recommendation.
        """
        if not text or not text.strip():
            return {
                "category": "Miscellaneous",
                "confidence": 0.1,
                "method": "default",
                "explanation": "Enter a description for intelligent auto-categorization",
                "alternatives": []
            }

        rule_res = self.predict_rule_based(text)
        ml_res = self.predict_ml(text)

        # Decision Logic:
        # 1. If rule matched with high confidence (> 0.8), accept rule
        if rule_res["confidence"] >= 0.80:
            return {
                "category": rule_res["category"],
                "confidence": rule_res["confidence"],
                "method": "rule",
                "explanation": rule_res["explanation"],
                "alternatives": ml_res.get("alternatives", [])
            }

        # 2. If both agree, boost confidence
        if rule_res["category"] == ml_res["category"] and rule_res["category"] != "Miscellaneous":
            boosted = min(0.99, max(rule_res["confidence"], ml_res["confidence"]) + 0.10)
            return {
                "category": rule_res["category"],
                "confidence": round(boosted, 2),
                "method": "hybrid (rule + ml)",
                "explanation": f"Validated by both keyword match ({rule_res['explanation']}) and ML classifier ({int(ml_res['confidence']*100)}%)",
                "alternatives": ml_res.get("alternatives", [])
            }

        # 3. If ML has strong confidence (> 0.60), prefer ML
        if ml_res["confidence"] >= 0.60:
            return {
                "category": ml_res["category"],
                "confidence": ml_res["confidence"],
                "method": "ml",
                "explanation": ml_res["explanation"],
                "alternatives": ml_res.get("alternatives", [])
            }

        # 4. Fallback to rule if it found any keyword, else ML
        if rule_res["category"] != "Miscellaneous":
            return rule_res
        
        return ml_res

# Global singleton categorizer instance
_categorizer_instance = None

def get_categorizer():
    global _categorizer_instance
    if _categorizer_instance is None:
        _categorizer_instance = IntelligentCategorizer()
    return _categorizer_instance
