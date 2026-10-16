"""Importing the logging submodule must not shadow the stdlib logger factory."""

import logging

import pytest


@pytest.mark.req("NFR-OPS-001")
def test_configure_logging_after_child_module_import():
    import eoip.observability.logging  # noqa: F401
    from eoip import observability

    logger = logging.getLogger("eoip")
    old_handlers, old_level, old_propagate = list(logger.handlers), logger.level, logger.propagate
    try:
        observability.configure_json_logging()
        count = len(logger.handlers)
        observability.configure_json_logging()
        assert len(logger.handlers) == count
        assert any(isinstance(h.formatter, observability.JsonLogFormatter) for h in logger.handlers)
    finally:
        logger.handlers = old_handlers
        logger.setLevel(old_level)
        logger.propagate = old_propagate
