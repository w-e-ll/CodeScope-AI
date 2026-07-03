#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from codescope_ai.app.core.exceptions import PromptBuildError
from codescope_ai.app.rag.prompt_builder import PromptBuilder


def test_build_answer_prompt(test_config) -> None:
    """Build grounded answer prompt."""

    builder = PromptBuilder(test_config)

    prompt = builder.build_answer_prompt(
        question="Where is logging configured?",
        matches=[
            {
                "content": "logger = logging.getLogger(__name__)",
                "metadata": {
                    "relative_path": "app/service.py",
                    "start_line": 1,
                    "end_line": 3,
                    "symbol_type": "file_section",
                    "symbol_name": "lines_1_3",
                },
            }
        ],
    )

    assert "Where is logging configured?" in prompt
    assert "app/service.py" in prompt
    assert "Answer only from the provided repository context" in prompt


def test_build_answer_prompt_empty_question(test_config) -> None:
    """Reject empty answer prompt question."""

    builder = PromptBuilder(test_config)

    with pytest.raises(PromptBuildError):
        builder.build_answer_prompt(
            question="",
            matches=[],
        )
