#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import os
import sys

from pathlib import Path

from codescope_ai.app.core.exceptions import (
    LoggingSetupError
)


def is_interactive_shell() -> bool:
    """Detect interactive shell execution."""

    return bool(os.environ.get("TERM"))


def setup_logger(
    logfile: str,
    level: int = logging.INFO,
    stdout: bool = False,
    max_bytes: int = 20 * 1024 * 1024,
    backup_count: int = 10,
) -> logging.Logger:
    """Configure application root logger."""

    try:

        root_logger = logging.getLogger()

        if root_logger.handlers:
            root_logger.handlers.clear()

        formatter = logging.Formatter(
            fmt=(
                "%(asctime)s "
                "%(process)5d "
                "%(levelname)-5s "
                "%(name)s "
                "%(message)s"
            )
        )

        logging.addLevelName(logging.WARNING, "WARN")
        logging.addLevelName(logging.CRITICAL, "FATAL")

        log_path = Path(logfile)

        log_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_handler = logging.handlers.RotatingFileHandler(
            filename=logfile,
            mode="a",
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )

        file_handler.setFormatter(formatter)

        root_logger.addHandler(file_handler)

        if is_interactive_shell():
            stdout = True

        if stdout:

            stdout_handler = logging.StreamHandler(
                sys.stdout
            )

            stdout_handler.setFormatter(
                formatter
            )

            root_logger.addHandler(
                stdout_handler
            )

        root_logger.setLevel(level)

        logger = logging.getLogger(__name__)

        logger.info(
            "Logger initialized"
        )

        logger.info(
            f"Log file: {logfile}"
        )

        logger.info(
            f"Log level: {logging.getLevelName(level)}"
        )

        return root_logger

    except Exception as exc:

        raise LoggingSetupError(
            f"Failed to initialize logger: {exc}"
        ) from exc
