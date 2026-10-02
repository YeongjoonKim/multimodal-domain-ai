# Evaluation

20개 테스트는 malformed/NaN/Infinity score, unknown entity, ambiguity, low score, service error, 저장된 실행 결과와 HTML 및 저장소 검사기를 검사합니다. detector mAP·진단 정확도·calibration은 미측정입니다.

운영 화면은 두 이미지의 CPU 기능 확인과 저장된 상담 UI를 보여줍니다.
이미지 진단부터 최종 권고까지 같은 요청을 재실행한 end-to-end 정확도 평가는 후속 과제입니다.
독립 Holdout/OOD/Calibration 평가와 Vision 후보·taxonomy·등록 근거·최종 답변의 일관성을 나누어 검증할 계획입니다.

후속 연구는 독립적인 task label과 baseline을 분리해야 합니다. 합성 회귀 통과율을 현장 성능으로 해석하지 않습니다.
