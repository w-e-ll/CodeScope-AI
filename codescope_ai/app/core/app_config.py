#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from dotenv import load_dotenv

from codescope_ai.app.core.exceptions import (
    ConfigError
)

logger = logging.getLogger(__name__)

load_dotenv()


@dataclass
class AppConfig:
    """Application configuration model."""

    env: str
    base_dir: str
    input_data_dir: str
    extracted_archives_dir: str
    vector_db_dir: str
    embeddings_dir: str
    generated_docs_dir: str
    generated_answers_dir: str
    log_dir: str
    embedding_model: str
    llm_model: str
    chunk_size: int
    chunk_overlap: int
    retrieval_top_k: int
    max_context_chars: int
    vector_collection: str
    max_archive_size_mb: int
    max_file_size_mb: int
    request_timeout_seconds: int
    embedding_timeout_seconds: int
    supported_extensions: list[str]
    ignored_directories: list[str]


def expand_path(
    value: str,
    base_dir: str,
) -> str:
    """Expand base directory placeholders."""

    return value.replace(
        "${base_dir}",
        base_dir
    )


def validate_required_keys(
    config: dict[str, Any],
    required_keys: list[str],
) -> None:
    """Validate required configuration keys."""

    missing_keys = [
        key
        for key in required_keys
        if key not in config
    ]

    if missing_keys:

        raise ConfigError(
            f"Missing config keys: {missing_keys}"
        )


def validate_environment() -> None:
    """Validate required environment variables."""

    required_variables = [
        "OPENAI_API_KEY",
    ]

    missing_variables = [
        name
        for name in required_variables
        if not os.getenv(name)
    ]

    if missing_variables:
        raise ConfigError(
            f"Missing environment variables: {missing_variables}"
        )


def load_yaml_config(
    config_path: str,
) -> AppConfig:
    """Load application configuration from YAML."""

    logger.info(
        f"Loading config file: {config_path}"
    )

    path = Path(config_path)

    if not path.is_file():

        raise ConfigError(
            f"Config file not found: {config_path}"
        )

    try:

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            config = yaml.safe_load(file)

        validate_required_keys(
            config,
            [
                "env",
                "paths",
                "ai",
                "vector_db",
                "limits",
                "ingestion",
            ],
        )

        paths = config["paths"]
        ai = config["ai"]
        vector_db = config["vector_db"]
        limits = config["limits"]
        ingestion = config["ingestion"]

        base_dir = paths["base_dir"]

        app_config = AppConfig(
            env=config["env"],

            base_dir=base_dir,

            input_data_dir=expand_path(
                paths["input_data_dir"],
                base_dir,
            ),

            extracted_archives_dir=expand_path(
                paths["extracted_archives_dir"],
                base_dir,
            ),

            vector_db_dir=expand_path(
                paths["vector_db_dir"],
                base_dir,
            ),

            embeddings_dir=expand_path(
                paths["embeddings_dir"],
                base_dir,
            ),

            generated_docs_dir=expand_path(
                paths["generated_docs_dir"],
                base_dir,
            ),

            generated_answers_dir=expand_path(
                paths["generated_answers_dir"],
                base_dir,
            ),

            log_dir=expand_path(
                paths["log_dir"],
                base_dir,
            ),

            embedding_model=ai["embedding_model"],
            llm_model=ai["llm_model"],

            chunk_size=ai["chunk_size"],
            chunk_overlap=ai["chunk_overlap"],

            retrieval_top_k=ai["retrieval_top_k"],
            max_context_chars=ai["max_context_chars"],

            vector_collection=vector_db["collection_name"],

            max_archive_size_mb=limits["max_archive_size_mb"],
            max_file_size_mb=limits["max_file_size_mb"],

            request_timeout_seconds=limits[
                "request_timeout_seconds"
            ],

            embedding_timeout_seconds=limits[
                "embedding_timeout_seconds"
            ],

            supported_extensions=ingestion[
                "supported_extensions"
            ],

            ignored_directories=ingestion[
                "ignored_directories"
            ],
        )

        logger.info(
            "Configuration loaded successfully"
        )

        logger.info(
            f"Environment: {app_config.env}"
        )

        logger.info(
            f"Embedding model: "
            f"{app_config.embedding_model}"
        )

        logger.info(
            f"LLM model: "
            f"{app_config.llm_model}"
        )
        validate_environment()
        return app_config

    except ConfigError:

        raise

    except Exception as exc:

        logger.exception(
            "Failed to load configuration"
        )

        raise ConfigError(
            f"Failed to load config: {exc}"
        ) from exc
