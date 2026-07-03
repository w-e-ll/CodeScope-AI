#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zipfile

from pathlib import Path

import pytest

from codescope_ai.app.core.exceptions import ArchiveLoaderError
from codescope_ai.app.ingestion.archive_loader import ArchiveLoader


def test_extract_archive_success(test_config, sample_zip: Path) -> None:
    """Extract valid repository archive."""

    loader = ArchiveLoader(test_config)

    repo_root = loader.extract_archive(str(sample_zip))

    assert repo_root.exists()
    assert (repo_root / "README.md").exists()
    assert (repo_root / "pyproject.toml").exists()


def test_extract_archive_missing_file(test_config) -> None:
    """Raise error for missing archive."""

    loader = ArchiveLoader(test_config)

    with pytest.raises(ArchiveLoaderError):
        loader.extract_archive("missing.zip")


def test_extract_archive_rejects_non_zip(test_config, tmp_path: Path) -> None:
    """Reject non-ZIP archives."""

    file_path = tmp_path / "repo.txt"
    file_path.write_text("not zip", encoding="utf-8")

    loader = ArchiveLoader(test_config)

    with pytest.raises(ArchiveLoaderError):
        loader.extract_archive(str(file_path))
