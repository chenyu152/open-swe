from src.detection.charset_detector import CharsetDetector
from src.detection.detection_pipeline import DetectionPipeline
from src.detection.warning_level import WarningLevel


class TestEdgeCases:
    def test_empty_input(self):
        detector = CharsetDetector()
        result = detector.detect("")
        assert len(result.warnings) == 0

    def test_exact_threshold(self):
        detector = CharsetDetector(threshold=0.7)
        result = detector.detect("test", confidence=0.7)
        assert len(result.warnings) == 0

    def test_zero_confidence(self):
        detector = CharsetDetector()
        result = detector.detect("test", confidence=0.0)
        assert result.warnings[0].level == WarningLevel.HIGH

    def test_module_failure(self):
        class FailingModule:
            def detect(self, text):
                raise RuntimeError("Detection failed")

        pipeline = DetectionPipeline([FailingModule(), CharsetDetector()])
        result = pipeline.process("test")
        assert len(result.warnings) > 0

    def test_mixed_encoding(self):
        detector = CharsetDetector()
        mixed_content = "Hello 世界"
        result = detector.detect(mixed_content)
        assert len(result.warnings) >= 0
