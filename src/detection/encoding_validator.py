class EncodingValidator:
    def __init__(self, threshold: float = 0.7, name: str = "encoding_validator"):
        self.threshold = threshold
        self.name = name

    def detect(self, text: str) -> dict:
        if not text:
            return {"charset": "unknown", "confidence": 0.0}

        detected = "UTF-8"
        confidence = 0.85

        if text.startswith("\ufeff"):
            detected = "UTF-8-BOM"
            confidence = 0.9
        elif len(text) >= 2 and (text.startswith("\xff\xfe") or text.startswith("\xfe\xff")):
            detected = "UTF-16"
            confidence = 0.85
        elif any(ord(c) > 127 for c in text):
            confidence = 0.75

        return {"charset": detected, "confidence": confidence}
