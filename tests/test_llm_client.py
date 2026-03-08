"""Tests for LLM client utilities (no actual API calls)."""

from src.summarization.llm_client import TokenUsage, strip_markdown_fences


class TestStripMarkdownFences:
    def test_json_fence(self):
        text = '```json\n{"key": "value"}\n```'
        assert strip_markdown_fences(text) == '{"key": "value"}'

    def test_plain_fence(self):
        text = '```\n{"key": "value"}\n```'
        assert strip_markdown_fences(text) == '{"key": "value"}'

    def test_no_fence(self):
        text = '{"key": "value"}'
        assert strip_markdown_fences(text) == '{"key": "value"}'

    def test_whitespace_around_fences(self):
        text = '  ```json\n{"key": "value"}\n```  '
        assert strip_markdown_fences(text) == '{"key": "value"}'


class TestTokenUsage:
    def test_initial_state(self):
        t = TokenUsage()
        assert t.total_tokens == 0
        assert t.call_count == 0
        assert t.total_cost == 0.0

    def test_report_format(self):
        t = TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150, call_count=2)
        report = t.report()
        assert "2 calls" in report
        assert "100" in report
        assert "150" in report

    def test_report_with_cost(self):
        t = TokenUsage(call_count=1, total_cost=0.005)
        report = t.report()
        assert "$0.005" in report
