#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from codescope_ai.app.ingestion.file_discovery import FileDiscovery


def test_discover_files(test_config, sample_repo) -> None:
    """Discover supported repository files."""

    discovery = FileDiscovery(test_config)

    files = discovery.discover_files(str(sample_repo))

    relative_paths = {
        path.relative_to(sample_repo).as_posix()
        for path in files
    }

    assert "README.md" in relative_paths
    assert "pyproject.toml" in relative_paths
    assert "app/service.py" in relative_paths
    assert ".venv/ignored.py" not in relative_paths
