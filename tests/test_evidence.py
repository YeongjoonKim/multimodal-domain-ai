"""공개 실행 snapshot이 실제 예제 계산과 일치하는지 검사한다."""
import json
from pathlib import Path
import unittest
from src.export_evidence import build
from src.render_evidence import render, pre


class EvidenceTests(unittest.TestCase):
    def test_rendered_evidence_matches(self):
        saved = (Path(__file__).parents[1] / "examples/execution.html").read_text()
        self.assertEqual(saved.strip(), render().strip())

    def test_html_escapes_content(self):
        self.assertNotIn("<script>", pre("<script>unsafe</script>"))

    def test_recorded_execution(self):
        saved = json.loads((Path(__file__).parents[1] / "examples/execution.json").read_text())
        self.assertEqual(saved, build())
