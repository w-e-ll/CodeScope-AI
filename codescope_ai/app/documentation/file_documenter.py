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

logger = logging.getLogger(__name__)


class FileDocumenter:
    """Generates documentation for a selected repository file."""

    def __init__(
        self,
        config: AppConfig,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient,
    ) -> None:
        """Initialize file documenter."""

        self.config = config
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def generate(
        self,
        file_path: str,
        chunks: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Generate file-level documentation."""

        if not file_path.strip():
            raise DocumentationGenerationError(
                "File path cannot be empty"
            )

        if not chunks:
            raise DocumentationGenerationError(
                f"No chunks provided for file: {file_path}"
            )

        try:
            logger.info(
                f"File documentation started: "
                f"file_path={file_path} "
                f"chunks={len(chunks)}"
            )

            prompt = self.prompt_builder.build_file_documentation_prompt(
                file_path=file_path,
                chunks=chunks,
            )

            documentation = self.llm_client.generate(
                prompt=prompt,
                temperature=0.1,
            )

            citations = self._build_citations(chunks)

            logger.info(
                f"File documentation completed: "
                f"file_path={file_path} "
                f"citations={len(citations)}"
            )

            return {
                "file_path": file_path,
                "documentation": documentation,
                "citations": citations,
            }

        except DocumentationGenerationError:
            raise

        except Exception as exc:
            logger.exception(
                f"File documentation failed: {file_path}"
            )

            raise DocumentationGenerationError(
                f"File documentation failed: {file_path}"
            ) from exc

    def _build_citations(
        self,
        chunks: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Build citations from file chunks."""

        citations = []
        seen = set()

        for chunk in chunks:
            metadata = chunk.get(
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
                }
            )

        return citations
