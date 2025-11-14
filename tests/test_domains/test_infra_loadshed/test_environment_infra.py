from tau2.domains.infra_loadshed.environment import get_environment, get_tasks
from tau2.domains.infra_loadshed.tools import InfraTools


def test_environment_returns_infra_tools():
    env = get_environment()
    assert isinstance(env.tools, InfraTools)
    assert env.domain_name == "infra_loadshed"


def test_tasks_include_quota_assertions():
    tasks = get_tasks()
    assert tasks
    assert any(
        a.func_name == "assert_quota_within_limits"
        for t in tasks
        if t.evaluation_criteria and t.evaluation_criteria.env_assertions
        for a in t.evaluation_criteria.env_assertions
    )
