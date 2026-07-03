#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from typing import Any

from codescope_ai.app.core.app_config import AppConfig
from codescope_ai.app.core.exceptions import (
    PromptBuildError,
)

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builds grounded prompts for codebase questions."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize prompt builder."""

        self.config = config

    def build_answer_prompt(
        self,
        question: str,
        matches: list[dict[str, Any]],
    ) -> str:
        """Build answer prompt with retrieved code context."""

        try:
            if not question.strip():
                raise PromptBuildError(
                    "Question cannot be empty"
                )

            context = self._build_context(matches)

            prompt = (
                "You are CodeScope AI, a senior code documentation assistant.\n"
                "Answer only from the provided repository context.\n"
                "If the context partially answers the question, explain what can be inferred and mention any uncertainty.\n"
                "If the context is completely unrelated, say that the repository context is insufficient.\n"
                "Use precise file citations with paths and line ranges.\n"
                "Do not invent files, APIs, classes, or behavior.\n\n"
                "Repository context:\n"
                f"{context}\n\n"
                "Question:\n"
                f"{question}\n\n"
                "Answer:"
            )

            logger.info(
                f"Answer prompt built: "
                f"question_length={len(question)} "
                f"context_length={len(context)}"
            )

            return prompt

        except PromptBuildError:
            raise

        except Exception as exc:
            logger.exception(
                "Failed to build answer prompt"
            )

            raise PromptBuildError(
                "Failed to build answer prompt"
            ) from exc

    def build_file_documentation_prompt(
        self,
        file_path: str,
        chunks: list[dict[str, Any]],
    ) -> str:
        """Build prompt for file-level documentation."""

        try:
            context = self._build_context(chunks)

            return (
                "You are CodeScope AI, a senior software documentation assistant.\n"
                "Generate concise technical documentation for the selected file.\n"
                "Explain purpose, key classes/functions, dependencies, errors, and operational behavior.\n"
                "Use only the provided context.\n\n"
                f"Target file: {file_path}\n\n"
                "File context:\n"
                f"{context}\n\n"
                "Documentation:"
            )

        except Exception as exc:
            logger.exception(
                f"Failed to build file documentation prompt: "
                f"{file_path}"
            )

            raise PromptBuildError(
                f"Failed to build file documentation prompt: "
                f"{file_path}"
            ) from exc

    def build_project_documentation_prompt(
        self,
        matches: list[dict[str, Any]],
    ) -> str:
        """Build prompt for project-level documentation."""

        try:
            context = self._build_context(matches)

            return (
                "You are CodeScope AI, a staff-level software documentation assistant.\n"
                "Generate a project overview from the provided repository context.\n"
                "Cover architecture, ingestion flow, RAG flow, configuration, observability, risks, and productionization.\n"
                "Use only the provided context and cite files with line ranges.\n\n"
                "Repository context:\n"
                f"{context}\n\n"
                "Project documentation:"
            )

        except Exception as exc:
            logger.exception(
                "Failed to build project documentation prompt"
            )

            raise PromptBuildError(
                "Failed to build project documentation prompt"
            ) from exc

    def _build_context(
        self,
        matches: list[dict[str, Any]],
    ) -> str:
        """Build bounded context block from retrieved matches."""

        context_parts = []
        current_size = 0

        for match in matches:
            metadata = match.get(
                "metadata",
                {},
            )

            content = match.get(
                "content",
                "",
            )

            block = (
                f"[Source: {metadata.get('relative_path')} "
                f"lines {metadata.get('start_line')}-"
                f"{metadata.get('end_line')} "
                f"symbol={metadata.get('symbol_type')}."
                f"{metadata.get('symbol_name')}]\n"
                f"{content}\n"
            )

            if (
                current_size + len(block)
                > self.config.max_context_chars
            ):
                logger.warning(
                    f"Context limit reached: "
                    f"max_context_chars={self.config.max_context_chars}"
                )

                break

            context_parts.append(block)
            current_size += len(block)

        if not context_parts:
            logger.warning(
                "Prompt context is empty"
            )

            return "No repository context was retrieved."

        return "\n---\n".join(context_parts)
