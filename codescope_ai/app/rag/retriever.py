#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from typing import Any

from codescope_ai.app.core.app_config import AppConfig
from codescope_ai.app.core.exceptions import (
    RetrievalError,
)
from codescope_ai.app.rag.embedding_client import EmbeddingClient
from codescope_ai.app.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


class Retriever:
    """Retrieves relevant code context for a user question."""

    def __init__(
        self,
        config: AppConfig,
        embedding_client: EmbeddingClient,
        vector_store: VectorStore,
    ) -> None:
        """Initialize retriever."""

        self.config = config
        self.embedding_client = embedding_client
        self.vector_store = vector_store

    def retrieve(
        self,
        question: str,
        top_k: int | None = None,
        where: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieve relevant chunks for a question."""

        if not question.strip():
            raise RetrievalError(
                "Question cannot be empty"
            )

        try:
            resolved_top_k = (
                top_k
                or self.config.retrieval_top_k
            )

            logger.info(
                f"Retrieving context: "
                f"top_k={resolved_top_k} "
                f"question_length={len(question)}"
            )

            query_embedding = self.embedding_client.embed_texts(
                [question]
            )[0]

            matches = self.vector_store.search(
                query_embedding=query_embedding,
                top_k=resolved_top_k,
                where=where,
            )

            logger.info(
                f"Context retrieved: "
                f"matches={len(matches)}"
            )

            self._log_matches(matches)

            return matches

        except RetrievalError:
            raise

        except Exception as exc:
            logger.exception(
                "Context retrieval failed"
            )

            raise RetrievalError(
                "Context retrieval failed"
            ) from exc

    def _log_matches(
        self,
        matches: list[dict[str, Any]],
    ) -> None:
        """Log retrieved chunk evidence."""

        for index, match in enumerate(
            matches,
            start=1,
        ):
            metadata = match.get(
                "metadata",
                {},
            )

            logger.info(
                f"Retrieved match #{index}: "
                f"path={metadata.get('relative_path')} "
                f"symbol={metadata.get('symbol_type')}."
                f"{metadata.get('symbol_name')} "
                f"lines={metadata.get('start_line')}-"
                f"{metadata.get('end_line')} "
                f"score={match.get('score')}"
            )
