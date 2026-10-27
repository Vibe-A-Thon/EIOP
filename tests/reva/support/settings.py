"""Settings override context manager for REVA tests."""

from contextlib import contextmanager
from typing import Any
from collections.abc import Generator

from reva.config import RevaSettings, clear_settings_cache, get_settings, set_settings


@contextmanager
def override_settings(**kwargs: Any) -> Generator[RevaSettings, None, None]:
    """Temporarily override RevaSettings fields."""
    current = get_settings()
    data = current.model_dump()
    data.update(kwargs)
    new_settings = RevaSettings(**data)
    set_settings(new_settings)
    try:
        yield new_settings
    finally:
        clear_settings_cache()
