from typing import Any

from src.detection.warning import Warning


class CharsetDetector:
    def __init__(
        self,
        threshold: float = 0.7,
        module_config: dict | None = None,
        name: str = "charset_detector",
    ):
        self.threshold = threshold
        self.module_config = module_config or {}
        self.name = name
        self._modules = []

    def _get_threshold(self, module_name: str | None = None) -> float:
        if module_name and module_name in self.module_config:
            return self.module_config[module_name].get("threshold", self.threshold)
        return self.threshold

    def detect(
        self, text: str, confidence: float | None = None, custom_message: str | None = None
    ) -> "DetectionResult":
        if not text:
            return DetectionResult(detected_charset="unknown", confidence=0.0, warnings=[])

        warnings = []
        detected_charset = "UTF-8"
        final_confidence = confidence if confidence is not None else 0.8

        for module in self._modules:
            try:
                mod_result = module.detect(text)
            except Exception as e:
                warnings.append(
                    Warning.from_confidence(
                        module=type(module).__name__,
                        confidence=0.0,
                        threshold=self._get_threshold(type(module).__name__),
                        message=f"Module {type(module).__name__} failed: {e}",
                    )
                )
                continue

            if isinstance(mod_result, dict):
                mod_name = type(module).__name__
                if mod_name in self.module_config:
                    mod_confidence = mod_result.get("confidence", 0.0)
                    mod_threshold = self._get_threshold(mod_name)
                    if mod_confidence < mod_threshold:
                        msg = custom_message.format(module=mod_name) if custom_message else ""
                        warnings.append(
                            Warning.from_confidence(
                                module=mod_name,
                                confidence=mod_confidence,
                                threshold=mod_threshold,
                                message=msg,
                            )
                        )
                continue

            mod_confidence = getattr(mod_result, "confidence", 0.0)
            mod_threshold = self._get_threshold(type(module).__name__)
            if mod_confidence < mod_threshold:
                msg = custom_message.format(module=type(module).__name__) if custom_message else ""
                warnings.append(
                    Warning.from_confidence(
                        module=type(module).__name__,
                        confidence=mod_confidence,
                        threshold=mod_threshold,
                        message=msg,
                    )
                )

        if final_confidence < self.threshold:
            msg = custom_message.format(module=self.name) if custom_message else ""
            w = Warning.from_confidence(
                module=self.name,
                confidence=final_confidence,
                threshold=self.threshold,
                message=msg,
            )
            warnings.append(w)

        return DetectionResult(
            detected_charset=detected_charset,
            confidence=final_confidence,
            warnings=warnings,
        )

    def register_module(self, module: Any) -> None:
        self._modules.append(module)


class DetectionResult:
    def __init__(
        self, detected_charset: str, confidence: float, warnings: list = None, extra: dict = None
    ):
        self.detected_charset = detected_charset
        self.confidence = confidence
        self.warnings = warnings or []
        self.extra = extra or {}

    def __add__(self, other: "DetectionResult") -> "DetectionResult":
        if isinstance(other, dict):
            return DetectionResult(
                detected_charset=other.get("charset", other.get("detected_charset", "unknown"))
                or self.detected_charset,
                confidence=max(self.confidence, other.get("confidence", 0.0)),
                warnings=list(self.warnings),
                extra={
                    **self.extra,
                    **{
                        k: v
                        for k, v in other.items()
                        if k not in ("charset", "detected_charset", "confidence", "warnings")
                    },
                },
            )
        return DetectionResult(
            detected_charset=other.detected_charset or self.detected_charset,
            confidence=max(self.confidence, other.confidence),
            warnings=self.warnings + other.warnings,
            extra={**self.extra, **other.extra},
        )
