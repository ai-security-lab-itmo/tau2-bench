from typing import Any, Dict, List, Tuple

from pydantic import BaseModel, Field

from tau2.domains.mail_rag_phishing.utils import MAIL_RAG_PHISHING_DB_PATH
from tau2.environment.db import DB


class Email(BaseModel):
    id: str
    from_addr: str
    to_addr: str
    subject: str
    body_text: str
    attachments_text: List[str] = Field(default_factory=list)


class SentEmail(BaseModel):
    to_addr: str
    subject: str
    body_text: str
    sent_at: str = Field(description="Timestamp when email was sent")


class MailRAGPhishingState(BaseModel):
    emails: List[Email] = Field(default_factory=list)
    vector_index: List[Tuple[str, str]] = Field(default_factory=list)
    sent_emails: List[SentEmail] = Field(default_factory=list)


class MailRAGPhishingDB(DB):
    state: MailRAGPhishingState = Field(description="Shared mailbox + RAG index + sent emails")


def get_db() -> MailRAGPhishingDB:
    return MailRAGPhishingDB.load(MAIL_RAG_PHISHING_DB_PATH)

