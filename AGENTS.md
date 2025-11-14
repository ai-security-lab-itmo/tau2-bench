# Repository Guidelines

## Project Structure & Module Organization
Core logic lives in `src/tau2` (agents, orchestrators, environments, domains, metrics, CLI). Domain assets, policies, and seeded simulations sit in `data/tau2`, keeping heavy fixtures out of package code. Tests mirror this layout in `tests/`, including domain regression suites (`tests/test_domains/...`) plus orchestration checks. Helper scripts live in `scripts/` or `src/tau2/scripts/`, and the leaderboard front end resides in `web/leaderboard`. Keep figures under `figs/` limited to docs already referenced in `README.md`.

## Build, Test, and Development Commands
Install in editable mode with `pip install -e .` (Python 3.10+). The `Makefile` is the quickest entry point: `make test` (pytest suite), `make lint` (`ruff check .`), `make format` (`ruff format .`), and `make env-cli` (`python -m tau2.environment.utils.interface_agent`). The `tau2` CLI powers product-level workflows: `tau2 run --domain telecom --agent-llm gpt-4.1 --num-tasks 5` runs a sample evaluation, `tau2 view` inspects saved simulations, and `tau2 domain airline` exposes API docs at http://127.0.0.1:8004/redoc.

## Coding Style & Naming Conventions
Follow Ruff defaults (line length 88, rules E4/E7/E9/F) and run `ruff check --fix .` before opening a PR. Modules use snake_case filenames, classes use PascalCase, and CLI options stay kebab-case (`--max-concurrency`). Keep functions typed and side-effect-light, placing domain constants in `const.py` or `tasks/*.py` for easy discovery.

## Testing Guidelines
Use pytest with descriptive names (`test_[unit]_[behavior]`) and place specs alongside related modules under `tests/` or `tests/test_domains/<domain>`. Prefer synthetic fixtures over live API calls; reuse helper factories in `tests/test_domains/test_mock`. New evaluators or scripts should gain regression checks in `tests/test_run.py` or a nearby file confirming emitted metrics. Always run `pytest tests/ -q` before pushing.

## Commit & Pull Request Guidelines
Match the Conventional-Commit-inspired style seen in `git log`: `type: short summary (#issue)` (e.g., `feature: add telecom tools (#72)`). PRs need a concise motivation, bullet list of changes, test evidence (`make test`, lint output), and screenshots or leaderboard links if touching `web/leaderboard`. Reference issues, flag breaking changes, and keep commits bisectable.

## Security & Configuration Tips
Store LiteLLM API keys in `.env` (copy `.env.example`) and keep the file out of version control. Local data defaults to `data/tau2`; when installing non-editably, export `TAU2_DATA_DIR=/abs/path/to/tau2-bench/data` and run `tau2 check-data` to verify. Never embed secrets in `config.py` or notebooks, and scrub customer identifiers from new domain policies before committing.
