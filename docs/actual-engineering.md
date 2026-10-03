# Vision Execution & Consultation Evidence

2026-10-02 기준 이미지 입력에서 CPU 추론·도메인 검색·사용자 응답까지의 연결입니다.

| 단계 | 확인한 구현 |
|---|---|
| 상담 진입 | router_chat_stream의 image_b64 처리와 진단 호출 |
| 이미지 처리 | vision_diagnosis의 resize와 병해/해충 async gather |
| 후보 정리 | 작물 필터·중복 제거·상위 후보·ambiguity·OOD 상태 |
| 도메인 정렬 | 모델 label → crop / NCPMS 병해충 명칭 |
| 처방 검색 | 작물·병해충이 확보된 조건에서 공식 등록 DB 조회 |
| 근거 전달 | question_suffix와 evidence_text를 상담 검색·생성 문맥에 주입 |
| 최종 전달 | SSE에 vision 후보·model 정보 포함 |
| 사용자 UI | App → VisionDiagnosisCard, 약제 상세는 근거를 갖춘 답변 본문 |

## Actual Consultation UI

실제 상담 화면에는 사진 첨부·질문·증상 설명·기간별 대응·약제 정보가 표시됩니다.
[상담 캡처](consultation-evidence.md)는 관리자 추론 화면과 구별되는 사용자 경험의 근거입니다.
카드와 답변은 메시지별로 연결되므로, 앞선 턴의 카드와 다음 사진 질문의 본문을 같은 추론 결과로 합치지 않습니다.
작물·병해충에 따른 공식 등록정보 조회는 위 코드 경로로 연결돼 있으며,
캡처에 표시된 개별 약제·희석배수·사용 간격의 등록 행 대조는 별도 검증 항목입니다.

## Actual Inference UI

현재 관리자 UI의 CPU 추론 테스트를 격리된 검증 브라우저에서 실행했습니다.
모델 교체·학습·데이터 적재 없이 이미지 한 장을 처리하는 실제 추론 API를 사용했습니다.
후보·score·실행 시간은 해당 입력에 대한 결과이며 독립 holdout 평가와 구분합니다.
초기 현미경 이미지에서는 검출이 없었고, 이는 서비스 실패나 건강함 판정과 다른 상태입니다.
이어 같은 오이 노균병 라벨의 다른 이미지를 작물 '모름'으로 입력했을 때 정상·토마토 잎곰팡이병 후보가 나왔습니다.
공개 화면은 이 결과를 그대로 보존합니다. 라벨 불일치가 관찰되어 진단 성공 사례로 해석하지 않습니다.
이 검토는 두 입력을 사용한 기능 확인이며 독립 정확도 benchmark가 아닙니다.

## Actual YOLO Training

사용자가 제공하고 공개를 승인한 학습 진행 캡처를 별도 근거로 사용했습니다.
화면에는 disease-yolo26x-20261001-1445, disease_v3, 78 classes,
train 165,468, epoch 75/100의 지표·그래프·실행 로그·4개 GPU 자원이 표시됩니다.
이는 **진행 시점의 화면**이며 완료 checkpoint나 독립 test 성능으로 바꾸어 표현하지 않습니다.
해당 캡처의 학습 run과 현재 추론 화면의 active run은 다릅니다.

## Failure Boundaries

병해·해충 중 한 분기가 실패해도 성공한 후보를 보존합니다.
둘 다 실패하면 도구 오류로 전달하고 상담은 이미지 분석 실패를 알린 뒤 텍스트 경로로 이어갑니다.
경쟁 후보·낮은 신뢰·빈 검출을 확정 처방으로 승격하지 않도록 상태를 유지합니다.

## Separate Model Paths

현재 상담의 Vision 도구는 CPU YOLO 경로입니다.
Qwen QLoRA VLM 학습과 vLLM adapter serving은 별도의 모델 lifecycle이며
[Fine-tuning Lab](https://github.com/YeongjoonKim/efficient-finetuning-lab)에서 설명합니다.
상담 연결은 backend→SSE→frontend 코드로 확인했고, 이번 검토에서 새 사용자 대화를 저장하는 end-to-end 테스트는 실행하지 않았습니다.
