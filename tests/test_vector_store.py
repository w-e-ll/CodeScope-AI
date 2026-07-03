#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from codescope_ai.app.ingestion.code_chunker import CodeChunk
from codescope_ai.app.rag.vector_store import VectorStore


def test_vector_store_upsert_and_count(test_config) -> None:
    """Upsert chunks into vector store and count records."""

    store = VectorStore(test_config)
    store.reset_collection()

    chunk = CodeChunk(
        chunk_id="chunk-1",
        relative_path="app/service.py",
        file_name="service.py",
        language="python",
        symbol_type="class",
        symbol_name="UserService",
        start_line=1,
        end_line=10,
        content="class UserService: pass",
        content_hash="hash",
        metadata={
            "docstring": None,
        },
    )

    store.upsert_chunks(
        chunks=[chunk],
        embeddings=[[0.1, 0.2, 0.3]],
    )

    assert store.count() == 1


def test_vector_store_mismatch_error(test_config) -> None:
    """Reject chunk and embedding count mismatch."""

    store = VectorStore(test_config)

    with pytest.raises(Exception):
        store.upsert_chunks(
            chunks=[
                CodeChunk(
                    chunk_id="chunk-1",
                    relative_path="app/service.py",
                    file_name="service.py",
                    language="python",
                    symbol_type="class",
                    symbol_name="UserService",
                    start_line=1,
                    end_line=10,
                    content="class UserService: pass",
                    content_hash="hash",
                    metadata={},
                )
            ],
            embeddings=[],
        )
