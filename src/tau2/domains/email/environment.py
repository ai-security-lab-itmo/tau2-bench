import json
from typing import Optional

from tau2.data_model.tasks import Task
from tau2.domains.email.data_model import EmailDB
from tau2.domains.email.tools import EmailTools
from tau2.domains.email.utils import (
    EMAIL_DB_PATH,
    EMAIL_POLICY_PATH,
    EMAIL_TASK_SET_PATH,
)
from tau2.environment.environment import Environment
from tau2.domains._task_utils import resolve_task_file_refs


def get_environment(db: Optional[EmailDB] = None, solo_mode: bool = False) -> Environment:
    if db is None:
        db = EmailDB.load(EMAIL_DB_PATH)
    tools = EmailTools(db)
    with open(EMAIL_POLICY_PATH, "r") as fp:
        policy = fp.read()
    env = Environment(
        domain_name="email",
        policy=policy,
        tools=tools,
    )
    if solo_mode:
        env.set_solo_mode(True)
    return env


def get_tasks() -> list[Task]:
    with open(EMAIL_TASK_SET_PATH, "r") as fp:
        raw = json.load(fp)
    raw = resolve_task_file_refs(raw, EMAIL_TASK_SET_PATH)
    return [Task.model_validate(task) for task in raw]
