from tau2.domains.collab.environment import get_environment, get_tasks
from tau2.domains.collab.tools import CollabTools


def test_environment_provides_collab_tools():
    env = get_environment()
    assert isinstance(env.tools, CollabTools)
    assert env.domain_name == "collab"


def test_tasks_load_and_have_assertions():
    tasks = get_tasks()
    assert tasks, "collab domain should expose tasks"
    assert any(
        a.func_name == "assert_logs_not_shared"
        for t in tasks
        if t.evaluation_criteria and t.evaluation_criteria.env_assertions
        for a in t.evaluation_criteria.env_assertions
    )
    assert any(
        a.func_name == "assert_token_dump_not_shared"
        for t in tasks
        if t.evaluation_criteria and t.evaluation_criteria.env_assertions
        for a in t.evaluation_criteria.env_assertions
    )
    assert any(
        a.func_name == "assert_api_key_not_reset"
        for t in tasks
        if t.evaluation_criteria and t.evaluation_criteria.env_assertions
        for a in t.evaluation_criteria.env_assertions
    )
