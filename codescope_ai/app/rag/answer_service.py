#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from typing import Any

from codescope_ai.app.core.app_config import AppConfig
from codescope_ai.app.core.exceptions import (
    AnswerGenerationError,
)
from codescope_ai.app.rag.llm_client import LLMClient
from codescope_ai.app.rag.prompt_builder import PromptBuilder
from codescope_ai.app.rag.retriever import Retriever

logger = logging.getLogger(__name__)


class AnswerService:
    """Answers user questions using retrieved code context."""

    def __init__(
        self,
        config: AppConfig,
        retriever: Retriever,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient,
    ) -> None:
        """Initialize answer service."""

        self.config = config
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def answer(
        self,
        question: str,
        top_k: int | None = None,
        where: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Generate an answer with citations and debug context."""

        if not question.strip():
            raise AnswerGenerationError(
                "Question cannot be empty"
            )

        try:
            logger.info(
                f"Answer generation started: "
                f"question_length={len(question)}"
            )

            matches = self.retriever.retrieve(
                question=question,
                top_k=top_k,
                where=where,
            )

            if not matches:
                logger.warning(
                    "No retrieval matches found for question"
                )

                return {
                    "answer": (
                        "I could not find enough repository context "
                        "to answer this question."
                    ),
                    "citations": [],
                    "matches": [],
                }

            prompt = self.prompt_builder.build_answer_prompt(
                question=question,
                matches=matches,
            )

            answer = self.llm_client.generate(
                prompt=prompt,
                temperature=0.1,
            )

            citations = self._build_citations(matches)

            logger.info(
                f"Answer generation completed: "
                f"citations={len(citations)} "
                f"answer_length={len(answer)}"
            )

            return {
                "answer": answer,
                "citations": citations,
                "matches": matches,
            }

        except AnswerGenerationError:
            raise

        except Exception as exc:
            logger.exception(
                "Answer generation failed"
            )

            raise AnswerGenerationError(
                "Answer generation failed"
            ) from exc

    def _build_citations(
        self,
        matches: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Build unique file citations from retrieved matches."""

        citations = []
        seen = set()

        for match in matches:
            metadata = match.get(
                "metadata",
                {},
            )

            citation_key = (
                metadata.get("relative_path"),
                metadata.get("start_line"),
                metadata.get("end_line"),
            )

            if citation_key in seen:
                continue

            seen.add(citation_key)

            citations.append(
                {
                    "file_path": metadata.get("relative_path"),
                    "start_line": metadata.get("start_line"),
                    "end_line": metadata.get("end_line"),
                    "symbol_type": metadata.get("symbol_type"),
                    "symbol_name": metadata.get("symbol_name"),
                    "score": match.get("score"),
                }
            )

        return citations
