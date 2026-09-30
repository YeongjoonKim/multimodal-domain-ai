"""실제 이미지 추론 대신 합성 관측 metadata를 이용해 근거 연결 경계를 실행한다."""

from dataclasses import dataclass, asdict
import json
import math


@dataclass(frozen=True)
class Candidate:
    entity: str
    score: float
    source: str = "synthetic_detector"


KNOWLEDGE = {
    "pattern-a": {"evidence_id": "synthetic-guide-a", "statement": "Inspect the fictional sample under consistent lighting."},
    "pattern-b": {"evidence_id": "synthetic-guide-b", "statement": "Compare a second fictional sample before interpreting."},
}


def validate_candidate(candidate):
    return (isinstance(candidate, Candidate)
            and type(candidate.score) in (int, float)
            and math.isfinite(candidate.score) and 0 <= candidate.score <= 1
            and candidate.source == "synthetic_detector"
            and isinstance(candidate.entity, str))


def interpret(candidates, *, service_status="ok", threshold=0.6, margin=0.15):
    if service_status not in {"ok", "error"}:
        raise ValueError("invalid_service_status")
    if (type(threshold) not in (int, float) or not 0 <= threshold <= 1
            or type(margin) not in (int, float) or not 0 <= margin <= 1):
        raise ValueError("invalid_policy")
    base = {"disclosure": "Reconstructed Public Demo",
            "vision_model": "mock_metadata_only", "narration": "template_not_llm",
            "diagnosis": False, "evidence": [], "claims": []}
    if service_status == "error":
        return dict(base, status="service_error", message="Inference unavailable; not a negative finding.")
    if not isinstance(candidates, list) or any(not validate_candidate(c) for c in candidates):
        raise ValueError("invalid_candidate")
    if not candidates:
        return dict(base, status="no_observation", message="No candidate; not proof of a healthy specimen.")
    # 같은 엔티티의 중복 관측은 더 높은 점수 하나만 사용한다.
    unique = {}
    for candidate in candidates:
        if candidate.entity not in unique or candidate.score > unique[candidate.entity].score:
            unique[candidate.entity] = candidate
    ranked = sorted(unique.values(), key=lambda c: (-c.score, c.entity))
    if ranked[0].score < threshold:
        return dict(base, status="low_confidence", message="Request another observation.")
    if len(ranked) > 1 and ranked[0].score - ranked[1].score < margin:
        return dict(base, status="ambiguous", message="Multiple candidates require review.",
                    candidates=[asdict(c) for c in ranked])
    top = ranked[0]
    evidence = KNOWLEDGE.get(top.entity)
    if evidence is None:
        return dict(base, status="knowledge_missing", message="No matching reference; no invented recommendation.")
    return dict(base, status="supported_candidate", candidate=asdict(top),
                evidence=[evidence["evidence_id"]],
                claims=[{"text": evidence["statement"], "evidence_id": evidence["evidence_id"]}],
                message="A fictional candidate with supporting sample knowledge, not a confirmed diagnosis.")


if __name__ == "__main__":
    for scenario in [[], [Candidate("pattern-a", 0.88)],
                     [Candidate("pattern-a", 0.8), Candidate("pattern-b", 0.76)]]:
        print(json.dumps(interpret(scenario), indent=2))
