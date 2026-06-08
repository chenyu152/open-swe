class ConfidenceScorer:
    def __init__(self, threshold: float = 0.7, name: str = "confidence_scorer"):
        self.threshold = threshold
        self.name = name

    def score(self, text: str, base_confidence: float = 0.0) -> dict:
        if not text:
            return {"charset": "unknown", "confidence": 0.0}

        length_factor = min(1.0, len(text) / 100)
        confidence = base_confidence * (0.5 + 0.5 * length_factor)
        return {"charset": "UTF-8", "confidence": round(confidence, 4)}
