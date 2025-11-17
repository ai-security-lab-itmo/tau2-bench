import json
from typing import Optional

from tau2.data_model.tasks import Task
from tau2.domains.output_handling.data_model import OutputDB
from tau2.domains.output_handling.tools import OutputTools
from tau2.domains.output_handling.utils import (
    OUTPUT_DB_PATH,
    OUTPUT_POLICY_PATH,
    OUTPUT_TASK_SET_PATH,
)
from tau2.environment.environment import Environment


def get_environment(db: Optional[OutputDB] = None, solo_mode: bool = False) -> Environment:
    if db is None:
        db = OutputDB.load(OUTPUT_DB_PATH)
    tools = OutputTools(db)
    with open(OUTPUT_POLICY_PATH, "r") as fp:
        policy = fp.read()
    env = Environment(
        domain_name="output_handling",
        policy=policy,
        tools=tools,
    )
    if solo_mode:
        env.set_solo_mode(True)
    return env


def get_tasks() -> list[Task]:
    with open(OUTPUT_TASK_SET_PATH, "r") as fp:
        tasks = json.load(fp)
    return [Task.model_validate(task) for task in tasks]
