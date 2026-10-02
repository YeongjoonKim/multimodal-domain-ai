# Multimodal Domain AI

### Image → YOLO → Structured Evidence → Consultation

[![CI](https://github.com/YeongjoonKim/multimodal-domain-ai/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/YeongjoonKim/multimodal-domain-ai/actions/workflows/ci.yml)

## Actual Engineering Experience

상담에 첨부된 이미지를 병해·해충 YOLO 도구로 분석하고, 작물·병해충 표준명과
공식 등록정보 검색을 거쳐 상담 근거로 전달하는 파이프라인을 구현했습니다.
이미지 모델의 후보와 약제·사용기준을 설명하는 답변의 책임을 분리했습니다.

![Multimodal architecture](docs/architecture/01_multimodal_architecture.svg)

Image Input → Disease / Pest Inference → Taxonomy Mapping → Structured Knowledge
→ Evidence Context → LLM Consultation → SSE → Diagnosis Card / Answer.

## Actual YOLO Training

**Purpose** — 이미지 진단 모델의 학습 진행과 자원 상태를 확인합니다.

![Actual YOLO training progress supplied by the owner](docs/screenshots/yolo-training-progress.png)

**What this demonstrates** — 사용자가 제공한 실제 YOLO26-X 학습 진행 화면의 epoch, mAP, precision/recall,
loss 그래프, 로그와 4개 GPU 상태. 완료 결과가 아닌 epoch 75/100 시점의 기록입니다.
**Architecture relation** — Dataset → Detector Training → Model Selection.

## Actual Vision Execution

**Purpose** — 적용 중인 모델로 이미지 한 장을 추론하고 도메인 매핑 결과를 확인합니다.

![Actual CPU vision inference result](docs/screenshots/vision-cpu-result.png)

**What this demonstrates** — 실제 관리자 추론 테스트의 입력 이미지, 검출 후보·score,
모델 식별자, CPU 처리 시간과 공식 병해충 명칭 연결.
2026-10-02 실제 CPU 추론 결과입니다. 이 오이 노균병 라벨 샘플에서는 작물 '모름' 조건에서
정상·토마토 잎곰팡이병 후보가 나왔으므로 **라벨 불일치 관측 사례**로 보존했습니다.
**Architecture relation** — Image → Model as Tool → Candidate / Domain Mapping.

## Consultation Integration

| 단계 | 실제 구현 |
|---|---|
| Image input | 상담 API가 첨부 이미지를 decode하고 진단 도구 호출 |
| Vision execution | 병해·해충 모델을 비동기로 함께 호출, 성공한 분기 보존 |
| Candidate interpretation | 작물 필터·중복 제거·경쟁 후보/낮은 신뢰 처리 |
| Structured evidence | 작물·병해충 표준명으로 공식 등록정보 검색과 연결 |
| LLM context | 진단 근거를 검색 문맥에 넣어 기존 상담 생성·검증 경로 사용 |
| Result UI | 최종 SSE의 vision 데이터로 사진 진단 카드 표시 |

사진 진단 카드는 **이미지에서 본 후보와 신뢰 수준**을 표시합니다.
등록 약제·희석배수·사용시기·안전사용기준은 답변 본문의 공식 검색 근거에서 설명합니다.
[코드 연결 근거와 오류 처리](docs/actual-engineering.md).

## System Strengths

| Decision | 구현 효과 |
|---|---|
| Model as tool | Vision을 상담 전체와 분리해 교체·실패 처리 가능 |
| Taxonomy alignment | 모델 라벨을 도메인 검색에 사용하는 표준 개념으로 연결 |
| Evidence separation | 시각적 유사도와 공식 등록정보의 근거 범위를 분리 |
| Failure-aware execution | 서비스 오류, 빈 검출, 모호한 후보를 서로 다른 상태로 전달 |
| Domain response composition | 이미지 관찰 결과와 검색 근거를 상담 파이프라인에서 결합 |

QLoRA VLM 학습·서빙 경로와 현재 YOLO 기반 상담 진단 경로는 별개입니다.
학습 lifecycle은 [Fine-tuning Lab](https://github.com/YeongjoonKim/efficient-finetuning-lab)에서 다룹니다.

## Public Reference Implementation & Lightweight Demo

| 구분 | 범위 |
|---|---|
| Actual Engineering Experience | 실제 이미지·YOLO·도메인 DB·상담·결과 카드 통합 |
| Public Reference Implementation | 후보 계약·불확실성·근거 일치·오류 상태를 독립 코드로 재구성 |
| Public Lightweight Demo | 합성 detector metadata + 가상 지식 + 템플릿 응답 |

[실행 artifact](examples/execution.json) · [화면 갤러리](docs/screenshots.md)에서
candidate / ambiguous / service_error / knowledge_missing 분기를 확인할 수 있습니다.
20개 테스트는 finite score, 후보 중복, 근거 누락, 서비스 오류와 snapshot을 검증합니다.

## Reproduce

```sh
python3 -m src.vision_demo
python3 -m src.export_evidence
python3 -m src.render_evidence
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
```

## Scope & Limitations

현재 공개 실행 코드는 metadata 이후의 계약을 검토하는 경량 예제입니다.
실제 모델 가중치·운영 DB·회사 소스는 포함하지 않습니다.
높은 detector score는 확정 진단이나 교정된 정확도를 뜻하지 않으며 빈 검출은 건강함의 증거가 아닙니다.
이번 실제 화면 검증은 두 이미지의 CPU 기능 확인이며 상담 전체의 새 end-to-end 정확도 평가는 별도 과제입니다.
독립 holdout, OOD, calibration과 최종 권고의 근거 일치를 나누어 평가할 계획입니다.

[상세 근거](docs/actual-engineering.md) · [평가](docs/evaluation.md) ·
[검증 기록](docs/validation.md) · [공개 경계](PUBLICATION.md) ·
[License notice](LICENSE-NOTICE.md) · [Security](SECURITY.md).
