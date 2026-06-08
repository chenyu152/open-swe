from typing import Any

from src.detection.charset_detector import DetectionResult


class DetectionPipeline:
    def __init__(self, stages: list[Any]):
        self.stages = stages

    def process(self, text: str) -> DetectionResult:
        if not text:
            return DetectionResult(detected_charset="unknown", confidence=0.0, warnings=[])

        all_warnings = []
        final_charset = "unknown"
        final_confidence = 0.0

        for stage in self.stages:
            try:
                result = stage.detect(text)
            except Exception as e:
                all_warnings.append(
                    {
                        "module": type(stage).__name__,
                        "confidence": 0.0,
                        "threshold": getattr(stage, "threshold", 0.7),
                        "level": "HIGH",
                        "message": f"Stage {type(stage).__name__} failed: {e}",
                        "timestamp": "",
                    }
                )
                continue

            if isinstance(result, DetectionResult):
                all_warnings.extend(result.warnings)
                if result.detected_charset and result.detected_charset != "unknown":
                    final_charset = result.detected_charset
                final_confidence = max(final_confidence, result.confidence)
            elif isinstance(result, dict):
                detected = result.get("charset") or result.get("detected_charset")
                if detected and detected != "unknown":
                    final_charset = detected
                final_confidence = max(final_confidence, result.get("confidence", 0.0))

        return DetectionResult(
            detected_charset=final_charset,
            confidence=final_confidence,
            warnings=all_warnings,
        )
