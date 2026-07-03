#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest

from codescope_ai.app.core.exceptions import SourceFileReadError
from codescope_ai.app.ingestion.source_file_reader import SourceFileReader


def test_read_file_success(test_config, sample_repo: Path) -> None:
    """Read source file with metadata."""

    reader = SourceFileReader(test_config)
    file_path = sample_repo / "app" / "service.py"

    source_file = reader.read_file(
        str(file_path),
        str(sample_repo),
    )

    assert source_file.relative_path == "app/service.py"
    assert source_file.language == "python"
    assert source_file.line_count > 0
    assert source_file.content_hash


def test_read_missing_file(test_config, sample_repo: Path) -> None:
    """Raise error for missing source file."""

    reader = SourceFileReader(test_config)

    with pytest.raises(SourceFileReadError):
        reader.read_file(
            str(sample_repo / "missing.py"),
            str(sample_repo),
        )
