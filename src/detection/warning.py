import time
from dataclasses import dataclass

from src.detection.warning_level import WarningLevel


@dataclass
class Warning:
    module: str
    confidence: float
    threshold: float
    level: WarningLevel
    message: str
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    @classmethod
    def from_confidence(
        cls, module: str, confidence: float, threshold: float, message: str = ""
    ) -> "Warning":
        if confidence <= 0:
            level = WarningLevel.HIGH
        elif confidence >= threshold:
            level = WarningLevel.LOW
        else:
            ratio = confidence / threshold
            if ratio < 0.4:
                level = WarningLevel.LOW
            elif ratio < 0.7:
                level = WarningLevel.MEDIUM
            else:
                level = WarningLevel.HIGH
        return cls(
            module=module,
            confidence=confidence,
            threshold=threshold,
            level=level,
            message=message
            or f"Low confidence detection (confidence={confidence:.2f}, threshold={threshold:.2f})",
        )
