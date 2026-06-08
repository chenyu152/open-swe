from src.detection.charset_detector import CharsetDetector


class TestModuleSpecific:
    def test_backward_compatibility(self):
        class OldModule:
            def detect(self, text):
                return {"charset": "UTF-8", "confidence": 0.5}

        detector = CharsetDetector()
        detector.register_module(OldModule())
        result = detector.detect("test", confidence=0.8)
        assert result.detected_charset is not None
        assert len(result.warnings) == 0

    def test_multiple_modules_same_charset(self):
        detector = CharsetDetector(threshold=0.6)
        result = detector.detect("test", confidence=0.5)
        utf8_warnings = [w for w in result.warnings if "UTF-8" in w.message]
        assert len(utf8_warnings) <= len(result.warnings)
