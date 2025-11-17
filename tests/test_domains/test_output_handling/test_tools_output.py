from tau2.domains.output_handling.data_model import OutputDB
from tau2.domains.output_handling.tools import OutputTools
from tau2.domains.output_handling.utils import OUTPUT_DB_PATH


def _fresh_db() -> OutputDB:
    loaded = OutputDB.load(str(OUTPUT_DB_PATH))
    return OutputDB.model_validate(loaded.model_dump())


def test_context_includes_snippets():
    tools = OutputTools(_fresh_db())
    ctx = tools.get_ticket_context()
    assert "raw_payload" in ctx["dangerous_snippets"]
    assert "safe_summary" in ctx["sanitized_snippets"]


def test_collab_notes_available():
    tools = OutputTools(_fresh_db())
    assert "Ops" in tools.get_collab_note()
    assert "Security" in tools.get_secondary_collab_note()


def test_forward_raw_sets_flag():
    tools = OutputTools(_fresh_db())
    assert tools.assert_no_unsafe_snippet_used()
    tools.forward_raw_snippet("raw_payload")
    assert tools.assert_no_unsafe_snippet_used() is False


def test_log_warning_sets_flag():
    tools = OutputTools(_fresh_db())
    assert tools.assert_warning_logged() is False
    tools.log_warning("Refused raw payload")
    assert tools.assert_warning_logged() is True
