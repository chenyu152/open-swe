from src.detection.charset_detector import CharsetDetector
from src.detection.confidence_scorer import ConfidenceScorer
from src.detection.detection_pipeline import DetectionPipeline
from src.detection.encoding_validator import EncodingValidator


class TestPipelineIntegration:
    def test_warning_propagation(self):
        detector1 = CharsetDetector(threshold=0.8)
        validator = EncodingValidator(threshold=0.8)
        pipeline = DetectionPipeline([detector1, validator, ConfidenceScorer()])
        result = pipeline.process("sample text")
        assert len(result.warnings) > 0

    def test_non_blocking_warnings(self):
        pipeline = DetectionPipeline([CharsetDetector(threshold=0.9), EncodingValidator()])
        result = pipeline.process("sample text")
        assert result.detected_charset is not None
        assert len(result.warnings) > 0

    def test_warning_aggregation(self):
        detector1 = CharsetDetector(threshold=0.8)
        detector2 = EncodingValidator(threshold=0.8)
        result1 = detector1.detect("test", confidence=0.5)
        result2 = detector2.detect("test")
        combined = result1 + result2
        assert len(combined.warnings) >= 1
