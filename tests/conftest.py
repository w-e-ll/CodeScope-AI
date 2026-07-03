#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import zipfile

from pathlib import Path

import pytest

from codescope_ai.app.core.app_config import AppConfig


@pytest.fixture
def test_config(tmp_path: Path) -> AppConfig:
    """Create test application config."""

    return AppConfig(
        env="test",
        base_dir=str(tmp_path),
        input_data_dir=str(tmp_path / "input_data"),
        extracted_archives_dir=str(tmp_path / "extracted_archives"),
        vector_db_dir=str(tmp_path / "vector_db"),
        embeddings_dir=str(tmp_path / "embeddings"),
        generated_docs_dir=str(tmp_path / "generated_docs"),
        generated_answers_dir=str(tmp_path / "generated_answers"),
        log_dir=str(tmp_path / "log"),
        embedding_model="text-embedding-3-small",
        llm_model="gpt-4o-mini",
        chunk_size=20,
        chunk_overlap=5,
        retrieval_top_k=3,
        max_context_chars=4000,
        vector_collection="test_codescope_chunks",
        max_archive_size_mb=10,
        max_file_size_mb=2,
        request_timeout_seconds=30,
        embedding_timeout_seconds=30,
        supported_extensions=[
            ".py",
            ".md",
            ".txt",
            ".yml",
            ".yaml",
            ".toml",
            ".json",
            ".sql",
            ".ini",
            ".cfg",
        ],
        ignored_directories=[
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            "node_modules",
            "dist",
            "build",
            ".idea",
            ".pytest_cache",
        ],
    )


@pytest.fixture
def sample_repo(tmp_path: Path) -> Path:
    """Create a sample repository."""

    repo = tmp_path / "sample_repo"
    repo.mkdir()

    (repo / "README.md").write_text(
        "# Sample Repo\n\nThis is a test repository.",
        encoding="utf-8",
    )

    (repo / "pyproject.toml").write_text(
        "[project]\nname = 'sample-repo'",
        encoding="utf-8",
    )

    app_dir = repo / "app"
    app_dir.mkdir()

    (app_dir / "service.py").write_text(
        "\n".join(
            [
                "import logging",
                "",
                "logger = logging.getLogger(__name__)",
                "",
                "class UserService:",
                "    \"\"\"Handles user operations.\"\"\"",
                "",
                "    def get_user(self, user_id: int) -> dict:",
                "        \"\"\"Return user by id.\"\"\"",
                "        return {'id': user_id}",
                "",
                "async def load_users() -> list:",
                "    \"\"\"Load users asynchronously.\"\"\"",
                "    return []",
            ]
        ),
        encoding="utf-8",
    )

    tests_dir = repo / "tests"
    tests_dir.mkdir()

    (tests_dir / "test_service.py").write_text(
        "def test_user():\n    assert True\n",
        encoding="utf-8",
    )

    ignored = repo / ".venv"
    ignored.mkdir()

    (ignored / "ignored.py").write_text(
        "print('ignore me')",
        encoding="utf-8",
    )

    return repo


@pytest.fixture
def sample_zip(tmp_path: Path, sample_repo: Path) -> Path:
    """Create a sample repository ZIP archive."""

    archive_path = tmp_path / "sample_repo.zip"

    with zipfile.ZipFile(archive_path, "w") as archive:
        for file_path in sample_repo.rglob("*"):
            if file_path.is_file():
                archive.write(
                    file_path,
                    file_path.relative_to(tmp_path),
                )

    return archive_path


@pytest.fixture(autouse=True)
def openai_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set OpenAI API key for config tests."""

    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-key",
    )
