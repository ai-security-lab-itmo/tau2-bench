from tau2.domains.output_handling.environment import get_environment, get_tasks
from tau2.domains.output_handling.tools import OutputTools


def test_environment_returns_output_tools():
    env = get_environment()
    assert isinstance(env.tools, OutputTools)
    assert env.domain_name == "output_handling"


def test_tasks_have_assertions():
    tasks = get_tasks()
    assert tasks
    assert any(
        a.func_name == "assert_no_unsafe_snippet_used"
        for t in tasks
        if t.evaluation_criteria and t.evaluation_criteria.env_assertions
        for a in t.evaluation_criteria.env_assertions
    )
