#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from codescope_ai.app.ingestion.code_chunker import CodeChunker
from codescope_ai.app.ingestion.source_file_reader import SourceFileReader


def test_chunk_python_file(test_config, sample_repo: Path) -> None:
    """Chunk Python file by AST symbols."""

    reader = SourceFileReader(test_config)
    chunker = CodeChunker(test_config)

    source_file = reader.read_file(
        str(sample_repo / "app" / "service.py"),
        str(sample_repo),
    )

    chunks = chunker.chunk_file(source_file)

    symbols = {
        chunk.symbol_name
        for chunk in chunks
    }

    assert "UserService" in symbols
    assert "load_users" in symbols

    symbol_types = {
        chunk.symbol_type
        for chunk in chunks
    }

    assert "class" in symbol_types
    assert "function" in symbol_types


def test_chunk_markdown_file(test_config, sample_repo: Path) -> None:
    """Chunk Markdown file by line windows."""

    reader = SourceFileReader(test_config)
    chunker = CodeChunker(test_config)

    source_file = reader.read_file(
        str(sample_repo / "README.md"),
        str(sample_repo),
    )

    chunks = chunker.chunk_file(source_file)

    assert chunks
    assert chunks[0].symbol_type == "file_section"
