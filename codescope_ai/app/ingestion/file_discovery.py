#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from pathlib import Path

from codescope_ai.app.core.app_config import AppConfig
from codescope_ai.app.core.exceptions import (
    FileDiscoveryError,
)

logger = logging.getLogger(__name__)


class FileDiscovery:
    """Discovers supported repository files."""

    def __init__(
        self,
        config: AppConfig,
    ) -> None:
        """Initialize file discovery service."""

        self.config = config

    def discover_files(
        self,
        repository_root: str,
    ) -> list[Path]:
        """Discover supported files recursively."""

        root_path = Path(repository_root)

        if not root_path.exists():

            raise FileDiscoveryError(
                f"Repository root does not exist: "
                f"{repository_root}"
            )

        logger.info(
            f"Starting file discovery: "
            f"{repository_root}"
        )

        discovered_files = []

        skipped_directories = 0
        skipped_files = 0

        try:

            for file_path in root_path.rglob("*"):

                if not file_path.is_file():
                    continue

                if self._should_skip_directory(file_path):

                    skipped_directories += 1

                    logger.debug(
                        f"Skipping file from ignored directory: "
                        f"{file_path}"
                    )

                    continue

                if not self._is_supported_file(file_path):

                    skipped_files += 1

                    logger.debug(
                        f"Skipping unsupported file: "
                        f"{file_path}"
                    )

                    continue

                discovered_files.append(file_path)

                logger.info(
                    f"Discovered file: {file_path}"
                )

            logger.info(
                f"File discovery completed: "
                f"supported_files={len(discovered_files)} "
                f"skipped_files={skipped_files} "
                f"skipped_directories={skipped_directories}"
            )

            return sorted(discovered_files)

        except Exception as exc:

            logger.exception(
                f"Failed during file discovery: "
                f"{repository_root}"
            )

            raise FileDiscoveryError(
                f"Failed to discover files: "
                f"{repository_root}"
            ) from exc

    def _is_supported_file(
        self,
        file_path: Path,
    ) -> bool:
        """Check whether a file is supported."""

        file_name = file_path.name.lower()

        special_files = {
            "dockerfile",
            "makefile",
            "requirements.txt",
            "pyproject.toml",
            "setup.py",
            "manifest.in",
            ".gitignore",
            ".env.example",
            "readme",
            "readme.md",
            "changelog",
            "changelog.md",
            "decisions",
            "decisions.md",
            "version",
        }

        if file_name in special_files:
            return True

        return (
            file_path.suffix.lower()
            in self.config.supported_extensions
        )

    def _should_skip_directory(
        self,
        file_path: Path,
    ) -> bool:
        """Check whether a file belongs to ignored directories."""

        ignored_directories = {
            directory.lower()
            for directory
            in self.config.ignored_directories
        }

        path_parts = {
            part.lower()
            for part
            in file_path.parts
        }

        return bool(
            ignored_directories.intersection(path_parts)
        )
