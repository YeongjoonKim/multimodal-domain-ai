# Vision model lifecycle

관리자에서 데이터셋·온톨로지·학습 run·체크포인트·활성 모델을 연결해 관리합니다.
학습 작업은 별도 호스트 큐가 처리하고, 추론은 독립 CPU 서비스가 담당합니다.

`Dataset / taxonomy → GPU training → checkpoint → export → active selection → CPU inference`

![활성 병해·해충 모델과 체크포인트 변환·적용](screenshots/vision-model-deployment.png)

2026-10-03 읽기 전용으로 촬영한 실제 UI입니다. 실행자 표시는 비식별 처리했습니다.
아래 checkpoint 목록과 위의 활성 모델은 서로 다른 run을 표시할 수 있습니다.
학습 후보를 선택한 것만으로 추론 모델이 교체되지는 않습니다.

| 책임 | 구현 |
|---|---|
| 학습 요청 | 인증된 관리자 API가 작업 종류·인자를 받아 전용 큐에 기록 |
| 호스트 실행 | 허용 작업으로 학습·중지·변환·활성화 처리, 로그·결과 보존 |
| 자원 조정 | 학습과 언어모델의 GPU 사용 전환, 학습 중 언어모델 재개 거부 |
| Export | checkpoint별 ONNX / OpenVINO 변환 상태 표시 |
| Activation | task별 활성 run·checkpoint·형식과 이전 적용 이력 관리 |
| Inference | CPU 서비스가 활성 모델을 읽어 후보·score·모델 식별자 반환 |
| Consultation | 후보 정리·표준명·등록정보 검색을 답변과 SSE 카드에 연결 |

화면 상단은 촬영 시점의 활성 병해·해충 모델을, 하단은 disease_v3 run의 checkpoint와 변환·적용 기능을 보여줍니다.
README의 75/100 학습 이미지는 해당 시점의 지표 기록이며, 배포 화면은 2026-10-03 촬영 기록입니다.
이 구분은 run 상태와 배포 상태를 함께 추적하는 사례입니다.

이 촬영에서는 학습·변환·활성화·설정 저장을 실행하지 않았습니다.
서비스·배치의 [서명 실행기](https://github.com/YeongjoonKim/reliable-domain-agent-harness/blob/main/docs/execution-control.md)와
Vision의 전용 작업 큐는 별도 경로이며 같은 서명 프로토콜을 사용한다고 설명하지 않습니다.
