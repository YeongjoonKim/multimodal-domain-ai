# Vision Evidence Gallery

## Actual Engineering

- [YOLO 학습 진행](screenshots/yolo-training-progress.png): 사용자가 제공한 epoch 75/100 시점의 실제 학습·지표·GPU 화면.
- [CPU 추론 결과](screenshots/vision-cpu-result.png): 현재 활성 모델의 실제 입력·후보·처리 시간.
- [연결 근거와 관측 한계](actual-engineering.md): 상담 API → Vision → 근거 → SSE → 사용자 카드의 코드 대응.

첫 화면은 학습 진행 기록이며, 두 번째는 다른 active run의 추론 결과입니다.
오이 노균병 라벨과 다른 후보가 나온 관측을 진단 성공으로 바꾸지 않았습니다.
Purpose / What this demonstrates / Architecture relation은 README의 각 화면에 기재했습니다.

## Public Lightweight Demo

아래 두 화면은 독립 합성 예제를 실행해 생성한 문서입니다.
[JSON](../examples/execution.json), [HTML](../examples/execution.html), [renderer](../src/render_evidence.py)를 함께 제공합니다.

- [후보와 근거](screenshots/candidate.png): 가상 detector metadata와 지식의 연결.
- [불확실성](screenshots/boundary.png): 모호한 후보·도구 실패·지식 부재 분리.

[캡처 hash](screenshots/manifest.json)는 검토한 공개 이미지 파일을 식별합니다.
