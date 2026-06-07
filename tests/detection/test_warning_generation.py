from src.detection.charset_detector import CharsetDetector
from src.detection.warning_level import WarningLevel


class TestWarningGeneration:
    def test_warning_metadata(self):
        detector = CharsetDetector()
        result = detector.detect("sample text", confidence=0.3)
        warning = result.warnings[0]
        assert all(
            key in vars(warning)
            for key in ["module", "confidence", "threshold", "level", "message", "timestamp"]
        )

    def test_warning_levels(self):
        detector = CharsetDetector(threshold=0.9)
        test_cases = [
            (0.1, WarningLevel.LOW),
            (0.4, WarningLevel.MEDIUM),
            (0.7, WarningLevel.HIGH),
        ]
        for conf, expected_level in test_cases:
            result = detector.detect("test", confidence=conf)
            assert result.warnings[0].level == expected_level, (
                f"conf={conf} expected {expected_level} got {result.warnings[0].level}"
            )

    def test_custom_warning_message(self):
        detector = CharsetDetector()
        result = detector.detect(
            "sample", confidence=0.5, custom_message="Low confidence in {module}"
        )
        assert "Low confidence in" in result.warnings[0].message
