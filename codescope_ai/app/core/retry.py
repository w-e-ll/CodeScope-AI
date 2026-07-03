#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time

from collections.abc import Callable
from functools import wraps
from typing import Any

from codescope_ai.app.core.exceptions import (
    RetryError
)

logger = logging.getLogger(__name__)


def retry(
    exceptions: tuple[type[Exception], ...],
    attempts: int = 3,
    delay_seconds: int = 2,
    backoff_multiplier: int = 2,
) -> Callable:
    """Retry failed operations with exponential backoff."""

    def decorator(function: Callable) -> Callable:

        @wraps(function)
        def wrapper(
            *args: Any,
            **kwargs: Any,
        ) -> Any:

            current_attempt = 1
            current_delay = delay_seconds

            while current_attempt <= attempts:

                try:

                    logger.info(
                        f"Executing operation: "
                        f"{function.__name__} "
                        f"(attempt {current_attempt}/{attempts})"
                    )

                    result = function(
                        *args,
                        **kwargs,
                    )

                    logger.info(
                        f"Operation succeeded: "
                        f"{function.__name__}"
                    )

                    return result

                except exceptions as exc:

                    logger.warning(
                        f"Retryable operation failed: "
                        f"{function.__name__} "
                        f"(attempt {current_attempt}/{attempts}) "
                        f"error={exc}"
                    )

                    if current_attempt >= attempts:

                        logger.exception(
                            f"Operation permanently failed: "
                            f"{function.__name__}"
                        )

                        raise RetryError(
                            f"Operation failed after "
                            f"{attempts} attempts: "
                            f"{function.__name__}"
                        ) from exc

                    logger.info(
                        f"Sleeping for "
                        f"{current_delay} seconds "
                        f"before retry"
                    )

                    time.sleep(
                        current_delay
                    )

                    current_delay *= backoff_multiplier
                    current_attempt += 1

                except Exception:

                    logger.exception(
                        f"Non-retryable error in "
                        f"{function.__name__}"
                    )

                    raise

        return wrapper

    return decorator
