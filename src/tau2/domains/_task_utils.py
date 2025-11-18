from pathlib import Path
from typing import Any


def _resolve_file_ref(value: Any, base_dir: Path) -> Any:
    """
    If value is a string starting with 'file:', load the referenced file from base_dir.
    Otherwise, return the value unchanged.
    """
    if isinstance(value, str) and value.startswith("file:"):
        rel = value.split("file:", 1)[1].strip()
        file_path = (base_dir / rel).resolve()
        with open(file_path, "r") as fp:
            return fp.read()
    return value


def resolve_task_file_refs(tasks: list[dict], tasks_json_path: Path) -> list[dict]:
    """
    Resolve file:filename references for:
      - user_scenario.instructions
      - user_prompt
      - agent_prompt
    The files are read relative to the directory containing tasks_json_path.
    """
    base_dir = tasks_json_path.parent
    resolved: list[dict] = []
    for t in tasks:
        t = dict(t)  # shallow copy
        # Top-level prompts
        if "user_prompt" in t:
            t["user_prompt"] = _resolve_file_ref(t.get("user_prompt"), base_dir)
        if "agent_prompt" in t:
            t["agent_prompt"] = _resolve_file_ref(t.get("agent_prompt"), base_dir)
        # User scenario instructions
        user_scenario = t.get("user_scenario")
        if isinstance(user_scenario, dict) and "instructions" in user_scenario:
            user_scenario = dict(user_scenario)
            user_scenario["instructions"] = _resolve_file_ref(
                user_scenario.get("instructions"), base_dir
            )
            t["user_scenario"] = user_scenario
        resolved.append(t)
    return resolved


