#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from codescope_ai.app.rag.answer_service import AnswerService


class FakeRetriever:
    """Fake retriever for answer service tests."""

    def retrieve(self, question, top_k=None, where=None):
        """Return fake retrieval matches."""

        return [
            {
                "content": "class UserService: pass",
                "score": 0.95,
                "metadata": {
                    "relative_path": "app/service.py",
                    "start_line": 1,
                    "end_line": 10,
                    "symbol_type": "class",
                    "symbol_name": "UserService",
                },
            }
        ]


class FakePromptBuilder:
    """Fake prompt builder for answer service tests."""

    def build_answer_prompt(self, question, matches):
        """Return fake prompt."""

        return "test prompt"


class FakeLLMClient:
    """Fake LLM client for answer service tests."""

    def generate(self, prompt, temperature=0.1):
        """Return fake answer."""

        return "UserService is implemented in app/service.py."


def test_answer_service_success(test_config) -> None:
    """Generate answer with citations."""

    service = AnswerService(
        config=test_config,
        retriever=FakeRetriever(),
        prompt_builder=FakePromptBuilder(),
        llm_client=FakeLLMClient(),
    )

    result = service.answer(
        "Where is UserService?"
    )

    assert "UserService" in result["answer"]
    assert result["citations"]
    assert result["citations"][0]["file_path"] == "app/service.py"
