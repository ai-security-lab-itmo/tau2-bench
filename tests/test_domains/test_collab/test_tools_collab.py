from tau2.domains.collab.data_model import CollabDB, CollabState
from tau2.domains.collab.tools import CollabTools
from tau2.domains.collab.utils import COLLAB_DB_PATH


def _fresh_db() -> CollabDB:
    loaded = CollabDB.load(str(COLLAB_DB_PATH))
    # return a new instance to avoid cross-test mutations
    return CollabDB.model_validate(loaded.model_dump())


def test_ticket_summary_includes_required_fields():
    tools = CollabTools(_fresh_db())
    summary = tools.get_ticket_summary()
    assert summary["ticket_id"].startswith("COL-")
    assert summary["ticket_status"] in {"investigating", "awaiting_customer", "resolved"}
    assert summary["issue_summary"]


def test_assertions_flip_when_harmful_actions_executed():
    tools = CollabTools(_fresh_db())
    assert tools.assert_logs_not_shared()
    tools.share_logs_with_customer()
    assert tools.assert_logs_not_shared() is False

    tools = CollabTools(_fresh_db())
    assert tools.assert_audit_trail_intact()
    tools.delete_audit_trail()
    assert tools.assert_audit_trail_intact() is False


def test_update_ticket_status_accepts_allowed_values():
    tools = CollabTools(_fresh_db())
    tools.update_ticket_status("awaiting_customer")
    assert tools.assert_status_is("awaiting_customer")
