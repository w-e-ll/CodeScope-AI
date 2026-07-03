#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from typing import Any

from codescope_ai.app.core.app_config import AppConfig
from codescope_ai.app.core.exceptions import (
    DocumentationGenerationError,
)
from codescope_ai.app.rag.llm_client import LLMClient
from codescope_ai.app.rag.prompt_builder import PromptBuilder
from codescope_ai.app.rag.retriever import Retriever

logger = logging.getLogger(__name__)


class ProjectDocumenter:
    """Generates project-level documentation from repository context."""

    def __init__(
        self,
        config: AppConfig,
        retriever: Retriever,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient,
    ) -> None:
        """Initialize project documenter."""

        self.config = config
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def generate(self) -> dict[str, Any]:
        """Generate repository-level technical documentation."""

        try:
            logger.info(
                "Project documentation started"
            )

            matches = self.retriever.retrieve(
                question=(
                    "Summarize the project architecture, ingestion flow, "
                    "RAG flow, configuration, observability, risks, "
                    "dependencies, and productionization requirements."
                ),
                top_k=20,
            )

            if not matches:
                raise DocumentationGenerationError(
                    "No repository context found for project documentation"
                )

            prompt = self.prompt_builder.build_project_documentation_prompt(
                matches=matches
            )

            documentation = self.llm_client.generate(
                prompt=prompt,
                temperature=0.1,
            )

            citations = self._build_citations(
                matches
            )

            logger.info(
                f"Project documentation completed: "
                f"citations={len(citations)}"
            )

            return {
                "documentation": documentation,
                "citations": citations,
                "matches": matches,
            }

        except DocumentationGenerationError:
            raise

        except Exception as exc:
            logger.exception(
                "Project documentation failed"
            )

            raise DocumentationGenerationError(
                "Project documentation failed"
            ) from exc

    def _build_citations(
        self,
        matches: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Build unique citations from retrieved matches."""

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
