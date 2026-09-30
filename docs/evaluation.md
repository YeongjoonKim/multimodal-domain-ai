# Evaluation

10 behavioral tests exercise the sample contracts. Five repository-quality tests
exercise the scanner, not model performance. Run `python3 -m unittest discover -s tests -v`.

No pixels, detector, YOLO model, LLM or model server is loaded. Teaching thresholds are not calibrated probabilities. Neither diagnostic accuracy nor pesticide safety is established.

Future evaluation needs independently labeled tasks and separated baselines.
A synthetic regression pass rate is not a real-world quality score.
