#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import shutil
import uuid
import zipfile

from pathlib import Path

from codescope_ai.app.core.app_config import AppConfig
from codescope_ai.app.core.exceptions import (
    ArchiveLoaderError,
    ArchiveSecurityError,
    RepositoryRootError,
)

logger = logging.getLogger(__name__)


class ArchiveLoader:
    """Extracts uploaded repository archives safely."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize archive loader."""

        self.config = config

    def extract_archive(self, archive_path: str) -> Path:
        """Extract a ZIP archive into a unique workspace."""

        source_path = Path(archive_path)

        try:
            self._validate_archive(source_path)

            workspace_dir = self._create_workspace(source_path)

            logger.info(
                f"Extracting archive: {source_path} "
                f"to workspace: {workspace_dir}"
            )

            with zipfile.ZipFile(source_path, "r") as archive:
                self._validate_archive_members(archive)
                archive.extractall(workspace_dir)

            repo_root = self.detect_repository_root(workspace_dir)

            logger.info(
                f"Archive extracted successfully: "
                f"repo_root={repo_root}"
            )

            return repo_root

        except (
            ArchiveLoaderError,
            ArchiveSecurityError,
            RepositoryRootError,
        ):
            raise

        except Exception as exc:
            logger.exception(
                f"Failed to extract archive: {source_path}"
            )

            raise ArchiveLoaderError(
                f"Failed to extract archive: {source_path}"
            ) from exc

    def detect_repository_root(self, workspace_dir: Path) -> Path:
        """Detect real repository root after ZIP extraction."""

        candidates = [
            workspace_dir,
            *[
                path
                for path in workspace_dir.iterdir()
                if path.is_dir()
            ],
        ]

        for candidate in candidates:
            if self._looks_like_repository(candidate):
                logger.info(
                    f"Detected repository root: {candidate}"
                )

                return candidate

        raise RepositoryRootError(
            f"Could not detect repository root in: {workspace_dir}"
        )

    def cleanup_workspace(self, workspace_dir: str) -> None:
        """Remove extracted workspace directory."""

        path = Path(workspace_dir)

        try:
            if path.exists():
                shutil.rmtree(path)

                logger.info(
                    f"Removed workspace directory: {path}"
                )

        except Exception as exc:
            logger.exception(
                f"Failed to remove workspace directory: {path}"
            )

            raise ArchiveLoaderError(
                f"Failed to remove workspace directory: {path}"
            ) from exc

    def _validate_archive(self, archive_path: Path) -> None:
        """Validate archive existence, type, and size."""

        if not archive_path.is_file():
            raise ArchiveLoaderError(
                f"Archive file not found: {archive_path}"
            )

        if archive_path.suffix.lower() != ".zip":
            raise ArchiveLoaderError(
                f"Only ZIP archives are supported: {archive_path}"
            )

        max_size_bytes = (
            self.config.max_archive_size_mb
            * 1024
            * 1024
        )

        archive_size = archive_path.stat().st_size

        if archive_size > max_size_bytes:
            raise ArchiveLoaderError(
                f"Archive is too large: "
                f"{archive_size} bytes"
            )

        if not zipfile.is_zipfile(archive_path):
            raise ArchiveLoaderError(
                f"Invalid ZIP archive: {archive_path}"
            )

    def _create_workspace(self, archive_path: Path) -> Path:
        """Create unique extraction workspace."""

        workspace_name = (
            f"{archive_path.stem}_"
            f"{uuid.uuid4().hex[:12]}"
        )

        workspace_dir = (
            Path(self.config.extracted_archives_dir)
            / workspace_name
        )

        workspace_dir.mkdir(
            parents=True,
            exist_ok=False
        )

        return workspace_dir

    def _validate_archive_members(
        self,
        archive: zipfile.ZipFile,
    ) -> None:
        """Validate ZIP members against unsafe paths."""

        for member in archive.infolist():
            member_path = Path(member.filename)

            if member_path.is_absolute():
                raise ArchiveSecurityError(
                    f"Archive contains absolute path: "
                    f"{member.filename}"
                )

            if ".." in member_path.parts:
                raise ArchiveSecurityError(
                    f"Archive contains unsafe path: "
                    f"{member.filename}"
                )

            if member.file_size > (
                self.config.max_file_size_mb
                * 1024
                * 1024
            ):
                raise ArchiveSecurityError(
                    f"Archive member is too large: "
                    f"{member.filename}"
                )

    def _looks_like_repository(self, path: Path) -> bool:
        """Check whether a directory looks like a repository root."""

        markers = {
            "pyproject.toml",
            "setup.py",
            "requirements.txt",
            "README.md",
            "readme.md",
            ".gitignore",
            "Dockerfile",
        }

        existing_markers = {
            child.name
            for child in path.iterdir()
        }

        return bool(
            markers.intersection(existing_markers)
        )
