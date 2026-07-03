#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from codescope_ai.app.core.exceptions import RetryError
from codescope_ai.app.core.retry import retry


def test_retry_eventual_success() -> None:
    """Retry until operation succeeds."""

    state = {
        "calls": 0,
    }

    @retry(
        exceptions=(ValueError,),
        attempts=3,
        delay_seconds=0,
    )
    def unstable_operation() -> str:
        state["calls"] += 1

        if state["calls"] < 2:
            raise ValueError("temporary")

        return "ok"

    assert unstable_operation() == "ok"
    assert state["calls"] == 2


def test_retry_exhausted() -> None:
    """Raise RetryError after exhausted attempts."""

    @retry(
        exceptions=(ValueError,),
        attempts=2,
        delay_seconds=0,
    )
    def broken_operation() -> None:
        raise ValueError("temporary")

    with pytest.raises(RetryError):
        broken_operation()
