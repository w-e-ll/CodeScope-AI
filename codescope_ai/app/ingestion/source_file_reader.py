#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import logging

from dataclasses import dataclass
from pathlib import Path

from codescope_ai.app.core.app_config import AppConfig
from codescope_ai.app.core.exceptions import (
    SourceFileReadError,
    UnsupportedFileError,
)

logger = logging.getLogger(__name__)


@dataclass
class SourceFile:
    """Represents a readable repository source file."""

    file_path: str
    relative_path: str
    file_name: str
    extension: str
    language: str
    content: str
    content_hash: str
    size_bytes: int
    line_count: int


class SourceFileReader:
    """Reads supported source files safely."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize source file reader."""

        self.config = config

    def read_file(self, file_path: str, repository_root: str) -> SourceFile:
        """Read a source file with metadata."""

        path = Path(file_path)
        root = Path(repository_root)

        try:
            self._validate_file(path)

            logger.info(
                f"Reading source file: {path}"
            )

            content = path.read_text(
                encoding="utf-8",
                errors="replace",
            )

            relative_path = (
                path.relative_to(root)
                .as_posix()
            )

            source_file = SourceFile(
                file_path=str(path),
                relative_path=relative_path,
                file_name=path.name,
                extension=path.suffix.lower(),
                language=self._detect_language(path),
                content=content,
                content_hash=self._hash_content(content),
                size_bytes=path.stat().st_size,
                line_count=len(content.splitlines()),
            )

            logger.info(
                f"Source file read successfully: "
                f"path={relative_path} "
                f"lines={source_file.line_count} "
                f"size={source_file.size_bytes}"
            )

            return source_file

        except (
            SourceFileReadError,
            UnsupportedFileError,
        ):
            raise

        except Exception as exc:
            logger.exception(
                f"Failed to read source file: {path}"
            )

            raise SourceFileReadError(
                f"Failed to read source file: {path}"
            ) from exc

    def read_files(self, file_paths: list[Path], repository_root: str) -> list[SourceFile]:
        """Read multiple source files."""

        source_files = []

        for file_path in file_paths:
            try:
                source_files.append(
                    self.read_file(
                        str(file_path),
                        repository_root,
                    )
                )

            except UnsupportedFileError as exc:
                logger.warning(
                    f"Skipping unsupported file: {file_path} "
                    f"reason={exc}"
                )

            except SourceFileReadError:
                logger.exception(
                    f"Skipping unreadable file: {file_path}"
                )

        logger.info(
            f"Source file reading completed: "
            f"read_files={len(source_files)}"
        )

        return source_files

    def _validate_file(self, file_path: Path) -> None:
        """Validate source file before reading."""

        if not file_path.is_file():
            raise SourceFileReadError(
                f"Source file not found: {file_path}"
            )

        max_size_bytes = (
            self.config.max_file_size_mb
            * 1024
            * 1024
        )

        size_bytes = file_path.stat().st_size

        if size_bytes > max_size_bytes:
            raise SourceFileReadError(
                f"Source file is too large: "
                f"{file_path} size={size_bytes}"
            )

        if not self._is_text_file(file_path):
            raise UnsupportedFileError(
                f"Binary or unsupported text file: {file_path}"
            )

    def _is_text_file(self, file_path: Path) -> bool:
        """Check whether file can be treated as text."""

        try:
            with open(
                file_path,
                "rb",
            ) as file:
                sample = file.read(4096)

            if b"\x00" in sample:
                return False

            return True

        except Exception as exc:
            raise SourceFileReadError(
                f"Failed to inspect source file: {file_path}"
            ) from exc

    def _detect_language(self, file_path: Path) -> str:
        """Detect language from file extension or name."""

        suffix = file_path.suffix.lower()
        name = file_path.name.lower()

        language_map = {
            ".py": "python",
            ".md": "markdown",
            ".txt": "text",
            ".yml": "yaml",
            ".yaml": "yaml",
            ".toml": "toml",
            ".json": "json",
            ".sql": "sql",
            ".ini": "ini",
            ".cfg": "config",
        }

        special_files = {
            "dockerfile": "dockerfile",
            "makefile": "makefile",
            "requirements.txt": "requirements",
            "manifest.in": "manifest",
            ".gitignore": "gitignore",
            ".env.example": "env",
            "version": "text",
        }

        if name in special_files:
            return special_files[name]

        return language_map.get(
            suffix,
            "text",
        )

    def _hash_content(self, content: str) -> str:
        """Create stable content hash."""

        return hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest()
