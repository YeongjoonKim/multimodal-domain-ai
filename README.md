# Multimodal Domain AI

## 01 Overview

A metadata-only reference pipeline links uncertain visual candidates to invented structured knowledge. **10 behavioral tests** cover validation, uncertainty and failure states. It demonstrates a safe tool boundary, not an image detector, a diagnostic service or measured model accuracy.

This repository is a sanitized and reconstructed technical showcase based on engineering experience from a private production AI platform.
It does not contain proprietary source code, private data, internal APIs, or production configuration.

본 저장소는 비공개 운영 AI 시스템의 설계·개발 경험을 기반으로 독립 재구성한 공개 기술 예제입니다. 회사 소스, 비공개 데이터, 내부 API 및 운영 설정은 포함하지 않습니다.

## 02 Problem

A high-confidence candidate without matching knowledge is not a justified recommendation. Service failure is different from no observation.

## 03 Architecture

![Reference architecture](docs/architecture/01_multimodal_architecture.svg)

[Editable Mermaid and diagram scope](docs/architecture/README.md).
Statuses are **IMPLEMENTED / PARTIAL / PROPOSED**; synthetic/mock describes the
dependency or data, not an additional implementation status.

## 04 Key Engineering Decisions

Treat candidates as uncertain evidence, not diagnoses. Validate scores, deduplicate entities, distinguish service failure from no observation and require matching knowledge.

[Design decisions](docs/design-decisions.md).

## 05 Implementation

IMPLEMENTED: finite-score validation, duplicate handling, low-score/ambiguity states, service-error separation and explicit not-a-diagnosis output. PARTIAL: synthetic detector metadata, fixture knowledge and template narration. PROPOSED: licensed image-model adapter, serving, calibrated uncertainty and evaluated LLM explanation.

Vision Pipeline: candidate metadata → uncertainty gate → structured knowledge → evidence → response. Model Serving is a future adapter, not a bundled server. Tool Integration uses typed candidates; API Design is an in-process function, not a published HTTP endpoint. Image uploads, authentication and pixel validation are not implemented.

## 06 Example

Synthetic pattern candidates pass through uncertainty and knowledge gates. Outputs always state that they are not diagnoses.

[Example instructions](examples/README.md).

## 07 Evaluation

10 behavioral tests plus five repository-quality checks run without models,
network or GPU. Counts are regression coverage, not model-quality scores.
[Evaluation](docs/evaluation.md) · [Local validation](docs/validation.md).

## 08 Failure / Limitations

No pixels, detector, YOLO model, LLM or model server is loaded. Teaching thresholds are not calibrated probabilities. Neither diagnostic accuracy nor pesticide safety is established.

[Failure boundaries](docs/limitations.md).

## 09 Reproducibility

Default sample: Python 3.10+ standard library; no package install, credentials or service
required. Run from the repository root. Synthetic inputs and explicit logic support
local comparison, not reproduction of a private platform.
[Maintenance](docs/maintenance.md).

## 10 Repository Structure

- `src/`: independently written sample modules.
- `examples/`: synthetic inputs or invocation guide.
- `tests/`: behavior and repository-quality regression tests.
- `docs/`: architecture, decisions, evaluation and limitations.
- `scripts/` and `.github/`: local checks and CI configuration.

## 11 Quick Start

```sh
python3 -m src.vision_demo
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
```

CI targets Python 3.10 and 3.12. Hosted runs are pending publication.

## 12 Research Relevance

Test calibrated multimodal grounding, out-of-distribution handling and human confirmation with independently licensed real images. No production images, weights or pesticide instructions are included.

MY CONTRIBUTION: author-confirmed engineering work. PLATFORM CONTEXT: private workflows
described conceptually. PUBLIC RECONSTRUCTION: this independent example.
FUTURE RESEARCH: unimplemented evaluation and integrations.

[Publication review](PUBLICATION.md) · [License notice](LICENSE-NOTICE.md) ·
[Security](SECURITY.md). No open-source license has been selected.
