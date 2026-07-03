#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest
import yaml

from codescope_ai.app.core.app_config import load_yaml_config
from codescope_ai.app.core.exceptions import ConfigError


def test_load_yaml_config_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Load valid YAML configuration."""

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    config_path = tmp_path / "config.yml"

    config_path.write_text(
        yaml.dump(
            {
                "env": "test",
                "paths": {
                    "base_dir": str(tmp_path),
                    "input_data_dir": "${base_dir}/var/input_data",
                    "extracted_archives_dir": "${base_dir}/var/extracted",
                    "vector_db_dir": "${base_dir}/var/vector_db",
                    "embeddings_dir": "${base_dir}/var/embeddings",
                    "generated_docs_dir": "${base_dir}/var/docs",
                    "generated_answers_dir": "${base_dir}/var/answers",
                    "log_dir": "${base_dir}/var/log",
                },
                "ai": {
                    "embedding_model": "text-embedding-3-small",
                    "llm_model": "gpt-4o-mini",
                    "chunk_size": 20,
                    "chunk_overlap": 5,
                    "retrieval_top_k": 3,
                    "max_context_chars": 4000,
                },
                "vector_db": {
                    "collection_name": "test_collection",
                },
                "limits": {
                    "max_archive_size_mb": 10,
                    "max_file_size_mb": 2,
                    "request_timeout_seconds": 30,
                    "embedding_timeout_seconds": 30,
                },
                "ingestion": {
                    "supported_extensions": [".py", ".md"],
                    "ignored_directories": [".git", ".venv"],
                },
            }
        ),
        encoding="utf-8",
    )

    config = load_yaml_config(str(config_path))

    assert config.env == "test"
    assert config.embedding_model == "text-embedding-3-small"
    assert config.vector_collection == "test_collection"


def test_load_yaml_config_missing_file() -> None:
    """Raise ConfigError when YAML file is missing."""

    with pytest.raises(ConfigError):
        load_yaml_config("missing.yml")


def test_load_yaml_config_missing_required_key(tmp_path: Path) -> None:
    """Raise ConfigError when required keys are missing."""

    config_path = tmp_path / "config.yml"

    config_path.write_text(
        yaml.dump({"env": "test"}),
        encoding="utf-8",
    )

    with pytest.raises(ConfigError):
        load_yaml_config(str(config_path))
