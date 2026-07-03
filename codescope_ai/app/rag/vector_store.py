#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from dataclasses import asdict
from typing import Any

import chromadb

from chromadb.api.models.Collection import Collection

from codescope_ai.app.core.app_config import AppConfig
from codescope_ai.app.core.exceptions import (
    VectorStoreError,
)
from codescope_ai.app.ingestion.code_chunker import CodeChunk

logger = logging.getLogger(__name__)


class VectorStore:
    """Stores and searches embedded code chunks."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize persistent Chroma vector store."""

        self.config = config

        try:
            self.client = chromadb.PersistentClient(
                path=config.vector_db_dir
            )

            self.collection = self.client.get_or_create_collection(
                name=config.vector_collection,
                metadata={
                    "description": "CodeScope AI code chunks"
                },
            )

            logger.info(
                f"Vector store initialized: "
                f"path={config.vector_db_dir} "
                f"collection={config.vector_collection}"
            )

        except Exception as exc:
            logger.exception(
                "Failed to initialize vector store"
            )

            raise VectorStoreError(
                "Failed to initialize vector store"
            ) from exc

    def upsert_chunks(
        self,
        chunks: list[CodeChunk],
        embeddings: list[list[float]],
    ) -> None:
        """Store code chunks and embeddings."""

        if not chunks:
            logger.warning(
                "No chunks provided for vector upsert"
            )

            return

        if len(chunks) != len(embeddings):
            raise VectorStoreError(
                f"Chunks and embeddings count mismatch: "
                f"chunks={len(chunks)} "
                f"embeddings={len(embeddings)}"
            )

        try:
            ids = [
                chunk.chunk_id
                for chunk in chunks
            ]

            documents = [
                chunk.content
                for chunk in chunks
            ]

            metadatas = [
                self._build_metadata(chunk)
                for chunk in chunks
            ]

            logger.info(
                f"Upserting chunks into vector store: "
                f"count={len(chunks)}"
            )

            self.collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
            )

            logger.info(
                f"Vector upsert completed: "
                f"count={len(chunks)}"
            )

        except VectorStoreError:
            raise

        except Exception as exc:
            logger.exception(
                "Failed to upsert chunks into vector store"
            )

            raise VectorStoreError(
                "Failed to upsert chunks into vector store"
            ) from exc

    def search(
        self,
        query_embedding: list[float],
        top_k: int,
        where: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Search similar code chunks."""

        try:
            logger.info(
                f"Searching vector store: "
                f"top_k={top_k} "
                f"where={where}"
            )

            result = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where,
                include=[
                    "documents",
                    "metadatas",
                    "distances",
                ],
            )

            matches = self._normalize_search_result(result)

            logger.info(
                f"Vector search completed: "
                f"matches={len(matches)}"
            )

            return matches

        except Exception as exc:
            logger.exception(
                "Vector search failed"
            )

            raise VectorStoreError(
                "Vector search failed"
            ) from exc

    def count(self) -> int:
        """Return number of stored chunks."""

        try:
            return self.collection.count()

        except Exception as exc:
            logger.exception(
                "Failed to count vector store records"
            )

            raise VectorStoreError(
                "Failed to count vector store records"
            ) from exc

    def reset_collection(self) -> None:
        """Delete and recreate the vector collection."""

        try:
            logger.warning(
                f"Resetting vector collection: "
                f"{self.config.vector_collection}"
            )

            self.client.delete_collection(
                name=self.config.vector_collection
            )

            self.collection = self.client.get_or_create_collection(
                name=self.config.vector_collection,
                metadata={
                    "description": "CodeScope AI code chunks"
                },
            )

            logger.info(
                "Vector collection reset completed"
            )

        except Exception as exc:
            logger.exception(
                "Failed to reset vector collection"
            )

            raise VectorStoreError(
                "Failed to reset vector collection"
            ) from exc

    def _build_metadata(
        self,
        chunk: CodeChunk,
    ) -> dict[str, Any]:
        """Build Chroma-compatible chunk metadata."""

        metadata = asdict(chunk)

        metadata.pop(
            "content",
            None,
        )

        metadata["metadata"] = str(
            chunk.metadata
        )

        return metadata

    def _normalize_search_result(
        self,
        result: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Normalize Chroma query result."""

        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        ids = result.get("ids", [[]])[0]

        matches = []

        for index, document in enumerate(documents):
            matches.append(
                {
                    "chunk_id": ids[index],
                    "content": document,
                    "metadata": metadatas[index],
                    "distance": distances[index],
                    "score": self._distance_to_score(
                        distances[index]
                    ),
                }
            )

        return matches

    def _distance_to_score(
        self,
        distance: float,
    ) -> float:
        """Convert distance to approximate similarity score."""

        return 1.0 / (1.0 + float(distance))
