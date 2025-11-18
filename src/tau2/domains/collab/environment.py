import json
from typing import Optional

from tau2.data_model.tasks import Task
from tau2.domains.collab.data_model import CollabDB
from tau2.domains.collab.tools import CollabTools
from tau2.domains.collab.utils import (
    COLLAB_DB_PATH,
    COLLAB_POLICY_PATH,
    COLLAB_TASK_SET_PATH,
)
from tau2.environment.environment import Environment
from tau2.domains._task_utils import resolve_task_file_refs


def get_environment(db: Optional[CollabDB] = None, solo_mode: bool = False) -> Environment:
    if db is None:
        db = CollabDB.load(COLLAB_DB_PATH)
    tools = CollabTools(db)
    with open(COLLAB_POLICY_PATH, "r") as fp:
        policy = fp.read()
    env = Environment(
        domain_name="collab",
        policy=policy,
        tools=tools,
    )
    if solo_mode:
        env.set_solo_mode(True)
    return env


def get_tasks() -> list[Task]:
    with open(COLLAB_TASK_SET_PATH, "r") as fp:
        raw = json.load(fp)
    raw = resolve_task_file_refs(raw, COLLAB_TASK_SET_PATH)
    return [Task.model_validate(task) for task in raw]
