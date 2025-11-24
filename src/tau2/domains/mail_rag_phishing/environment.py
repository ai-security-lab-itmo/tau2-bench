import json
from typing import Optional

from tau2.data_model.tasks import Task
from tau2.domains.mail_rag_phishing.data_model import MailRAGPhishingDB
from tau2.domains.mail_rag_phishing.tools import MailRAGPhishingTools
from tau2.domains.mail_rag_phishing.utils import (
    MAIL_RAG_PHISHING_DB_PATH,
    MAIL_RAG_PHISHING_POLICY_PATH,
    MAIL_RAG_PHISHING_TASK_SET_PATH,
    MAIL_RAG_PHISHING_DESCRIPTION_PATH,
)
from tau2.domains._task_utils import resolve_task_file_refs
from tau2.environment.environment import Environment


def get_environment(
    db: Optional[MailRAGPhishingDB] = None, solo_mode: bool = False
) -> Environment:
    if db is None:
        db = MailRAGPhishingDB.load(MAIL_RAG_PHISHING_DB_PATH)
    tools = MailRAGPhishingTools(db)
    with open(MAIL_RAG_PHISHING_POLICY_PATH, "r") as fp:
        policy = fp.read()
    env = Environment(
        domain_name="mail_rag_phishing",
        policy=policy,
        tools=tools,
    )
    if solo_mode:
        env.set_solo_mode(True)
    return env


def get_tasks() -> list[Task]:
    with open(MAIL_RAG_PHISHING_TASK_SET_PATH, "r") as fp:
        raw = json.load(fp)
    raw = resolve_task_file_refs(raw, MAIL_RAG_PHISHING_TASK_SET_PATH)
    return [Task.model_validate(task) for task in raw]

