import json
from typing import Optional

from tau2.data_model.tasks import Task
from tau2.domains.mktg_phishing.data_model import MktgDB
from tau2.domains.mktg_phishing.tools import MktgTools
from tau2.domains.mktg_phishing.utils import (
    MKTG_PHISHING_DB_PATH,
    MKTG_PHISHING_POLICY_PATH,
    MKTG_PHISHING_TASK_SET_PATH,
)
from tau2.environment.environment import Environment
from tau2.domains._task_utils import resolve_task_file_refs


def get_environment(db: Optional[MktgDB] = None, solo_mode: bool = False) -> Environment:
    if db is None:
        db = MktgDB.load(MKTG_PHISHING_DB_PATH)
    tools = MktgTools(db)
    with open(MKTG_PHISHING_POLICY_PATH, "r") as fp:
        policy = fp.read()
    env = Environment(
        domain_name="mktg_phishing",
        policy=policy,
        tools=tools,
    )
    if solo_mode:
        env.set_solo_mode(True)
    return env


def get_tasks() -> list[Task]:
    with open(MKTG_PHISHING_TASK_SET_PATH, "r") as fp:
        raw = json.load(fp)
    raw = resolve_task_file_refs(raw, MKTG_PHISHING_TASK_SET_PATH)
    return [Task.model_validate(task) for task in raw]


