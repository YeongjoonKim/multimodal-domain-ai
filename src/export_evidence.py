"""픽셀 추론을 가장하지 않고 실제 metadata 해석 결과를 내보낸다."""
import json
from .vision_demo import Candidate, interpret


def build():
    return {"scope": "executed_synthetic_metadata_only_no_pixels_or_detector",
            "supported": interpret([Candidate("pattern-a", 0.88)]),
            "ambiguous": interpret([Candidate("pattern-a", 0.8), Candidate("pattern-b", 0.76)]),
            "service_error": interpret([], service_status="error"),
            "knowledge_missing": interpret([Candidate("unknown-pattern", 0.95)])}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
