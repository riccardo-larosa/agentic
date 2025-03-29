import pytest
from src.workflow import enable_debug_logging  # run_agent_workflow
import logging


def test_enable_debug_logging():
    """Test that debug logging is properly enabled."""
    enable_debug_logging()
    logger = logging.getLogger("src")
    assert logger.getEffectiveLevel() == logging.DEBUG


# def test_run_agent_workflow_empty_input():
#     """Test workflow execution with empty input."""
#     with pytest.raises(ValueError):
#         run_agent_workflow("")
