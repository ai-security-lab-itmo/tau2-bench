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
        tasks = json.load(fp)
    return [Task.model_validate(task) for task in tasks]
