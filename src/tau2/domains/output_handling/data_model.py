from pydantic import BaseModel, Field

from tau2.domains.output_handling.utils import OUTPUT_DB_PATH
from tau2.environment.db import DB


class OutputState(BaseModel):
    ticket_id: str = Field(description="Ticket identifier")
    customer_message: str = Field(description="Raw customer message or payload")
    sanitized_snippets: dict[str, str] = Field(
        default_factory=dict,
        description="Safe snippets indexed by id",
    )
    dangerous_snippets: dict[str, str] = Field(
        default_factory=dict,
        description="Raw snippets that contain scripts/SQL/etc.",
    )
    collab_note: str = Field(description="Instruction from collaborator")
    secondary_collab_note: str | None = Field(
        default=None, description="Security guidance to follow"
    )
    unsafe_snippet_used: bool = Field(
        default=False, description="Whether a dangerous snippet was sent"
    )
    warning_logged: bool = Field(
        default=False, description="Whether the agent logged a refusal"
    )


class OutputDB(DB):
    state: OutputState = Field(description="Output handling state")


def get_db() -> OutputDB:
    return OutputDB.load(OUTPUT_DB_PATH)
