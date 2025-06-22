import pickle
import os
from typing import List, Dict, Any

class ToxicityPredictor:
    def __init__(self, model_path: str = "../model/toxic_detection.pkl"):
        self.model = None
        self.vectorizer = None
        self.load_model(model_path)

    def load_model(self, model_path: str):
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
        except Exception as e:
            raise Exception(f"Error loading model from '{model_path}': {str(e)}")

    def predict_toxicity(self, comments: List[str]) -> List[Dict[str, Any]]:
        if not comments:
            return []
        
        results = []
        
        for comment in comments:
            try:
                if self.vectorizer:
                    comment_vector = self.vectorizer.transform([comment])
                else:
                    comment_vector = [comment]
                
                prediction = self.model.predict(comment_vector)[0]
                probability = self.model.predict_proba(comment_vector)[0]
                
                confidence = max(probability)
                
                status = "toxic" if prediction == 1 else "non-toxic"
                
                results.append({"status": status, "confidence": round(confidence * 100, 2)})
            except Exception as e:
                results.append({"status": "error", "confidence": 0})
        
        return results
    
    def get_overall_statistics(self, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not predictions:
            return {"total_comments": 0, "toxic_count": 0, "non_toxic_count": 0,}
        
        total = len(predictions)
        toxic_count = sum(1 for p in predictions if p.get("status") == "toxic")
        non_toxic_count = sum(1 for p in predictions if p.get("status") == "non-toxic")
        
        return {"total_comments": total, "toxic_count": toxic_count, "non_toxic_count": non_toxic_count} 