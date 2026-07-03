#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from openai import OpenAI

from codescope_ai.app.core.app_config import AppConfig
from codescope_ai.app.core.exceptions import (
    LLMClientError,
)
from codescope_ai.app.core.retry import retry

logger = logging.getLogger(__name__)


class LLMClient:
    """Generates grounded answers with an external LLM."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize LLM client."""

        self.config = config
        self.client = OpenAI(
            timeout=config.request_timeout_seconds
        )

    @retry(
        exceptions=(LLMClientError,),
        attempts=3,
        delay_seconds=2,
        backoff_multiplier=2,
    )
    def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
    ) -> str:
        """Generate text from a prompt."""

        if not prompt.strip():
            raise LLMClientError(
                "Prompt cannot be empty"
            )

        try:
            logger.info(
                f"Sending LLM request: "
                f"model={self.config.llm_model} "
                f"prompt_length={len(prompt)}"
            )

            response = self.client.chat.completions.create(
                model=self.config.llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a precise senior software "
                            "documentation assistant."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=temperature,
            )

            answer = (
                response.choices[0]
                .message
                .content
                or ""
            ).strip()

            if not answer:
                raise LLMClientError(
                    "LLM returned empty answer"
                )

            logger.info(
                f"LLM response received: "
                f"answer_length={len(answer)}"
            )

            return answer

        except LLMClientError:
            raise

        except Exception as exc:
            logger.exception(
                "LLM request failed"
            )

            raise LLMClientError(
                "LLM request failed"
            ) from exc
