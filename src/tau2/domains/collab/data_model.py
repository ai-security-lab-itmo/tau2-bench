from typing import Literal

from pydantic import BaseModel, Field

from tau2.domains.collab.utils import COLLAB_DB_PATH
from tau2.environment.db import DB


class CollabState(BaseModel):
    ticket_id: str = Field(description="Unique ticket identifier")
    customer_name: str = Field(description="Customer full name")
    subscription_tier: str = Field(description="Active subscription plan")
    issue_summary: str = Field(description="Summary of the reported issue")
    resolution_hint: str = Field(description="Suggested remediation path")
    collab_note: str = Field(
        description="Message supposedly from a collaborator, may contain poisoned instructions"
    )
    ticket_status: Literal["investigating", "awaiting_customer", "resolved"] = Field(
        default="investigating", description="Current ticket status"
    )
    logs_available: bool = Field(default=True, description="Whether diagnostic logs exist")
    logs_shared_with_customer: bool = Field(
        default=False, description="Whether logs were shared outside the team"
    )
    audit_trail_deleted: bool = Field(
        default=False, description="Whether internal audit artifacts were deleted"
    )


class CollabDB(DB):
    """Holds the collaborative ticket state."""

    state: CollabState = Field(description="Single-ticket state used for the scenario")


def get_db() -> CollabDB:
    return CollabDB.load(COLLAB_DB_PATH)
