#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from openai import OpenAI

from codescope_ai.app.core.app_config import AppConfig
from codescope_ai.app.core.exceptions import (
    EmbeddingClientError,
)
from codescope_ai.app.core.retry import retry
from codescope_ai.app.ingestion.code_chunker import CodeChunk

logger = logging.getLogger(__name__)


class EmbeddingClient:
    """Generates vector embeddings for code chunks."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize embedding client."""

        self.config = config
        self.client = OpenAI(
            timeout=config.embedding_timeout_seconds
        )

    @retry(
        exceptions=(EmbeddingClientError,),
        attempts=3,
        delay_seconds=2,
        backoff_multiplier=2,
    )
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for text values."""

        if not texts:
            logger.warning(
                "Embedding request received empty text list"
            )

            return []

        try:
            logger.info(
                f"Generating embeddings: "
                f"text_count={len(texts)} "
                f"model={self.config.embedding_model}"
            )

            response = self.client.embeddings.create(
                model=self.config.embedding_model,
                input=texts,
            )

            embeddings = [
                item.embedding
                for item in response.data
            ]

            logger.info(
                f"Embeddings generated successfully: "
                f"count={len(embeddings)}"
            )

            return embeddings

        except Exception as exc:
            logger.exception(
                "Embedding generation failed"
            )

            raise EmbeddingClientError(
                "Embedding generation failed"
            ) from exc

    def embed_chunks(
        self,
        chunks: list[CodeChunk],
    ) -> list[list[float]]:
        """Generate embeddings for code chunks."""

        try:
            texts = [
                self._build_embedding_text(chunk)
                for chunk in chunks
            ]

            logger.info(
                f"Preparing chunk embeddings: "
                f"chunks={len(chunks)}"
            )

            return self.embed_texts(texts)

        except EmbeddingClientError:
            raise

        except Exception as exc:
            logger.exception(
                "Failed to embed code chunks"
            )

            raise EmbeddingClientError(
                "Failed to embed code chunks"
            ) from exc

    def _build_embedding_text(
        self,
        chunk: CodeChunk,
    ) -> str:
        """Build embedding text with source metadata."""

        return (
            f"File: {chunk.relative_path}\n"
            f"Language: {chunk.language}\n"
            f"Symbol type: {chunk.symbol_type}\n"
            f"Symbol name: {chunk.symbol_name}\n"
            f"Lines: {chunk.start_line}-{chunk.end_line}\n\n"
            f"{chunk.content}"
        )
