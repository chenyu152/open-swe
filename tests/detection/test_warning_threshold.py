from src.detection.charset_detector import CharsetDetector
from src.detection.warning_level import WarningLevel


class TestWarningThreshold:
    def test_default_threshold_warning(self):
        detector = CharsetDetector()
        result = detector.detect("sample text", confidence=0.45)
        assert len(result.warnings) == 1
        assert result.warnings[0].level == WarningLevel.MEDIUM

    def test_custom_threshold(self):
        detector = CharsetDetector(threshold=0.5)
        result = detector.detect("sample text", confidence=0.6)
        assert len(result.warnings) == 0

    def test_per_module_threshold(self):
        config = {"utf8_detector": {"threshold": 0.8}}
        detector = CharsetDetector(module_config=config)

        class utf8_detector:
            def detect(self, text):
                return {"charset": "UTF-8", "confidence": 0.75}

        detector.register_module(utf8_detector())
        result = detector.detect("sample text", confidence=0.85)
        assert len(result.warnings) == 1
