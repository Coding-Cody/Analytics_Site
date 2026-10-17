# Repository Instructions

## Project

- Type: Streamlit data-science portfolio.
- Entry point: `app.py`.
- Python: 3.11.
- Dependency source of truth: `pyproject.toml` and `uv.lock`.
- Git remote: `https://github.com/Coding-Cody/Analytics_Site.git`.
- Default branch: `main`.

## Environment

- Preferred manager: `uv`.
- Create or synchronize environment: `uv sync --locked`.
- Run commands through `uv run`.
- Add runtime dependency: `uv add <package>`.
- Add development dependency: `uv add --dev <package>`.
- Do not edit `uv.lock` manually.
- Do not commit `.venv/`, `.env`, credentials, private data, or generated output.
- Conda fallback environment: `career-site`, defined by `environment.yml`.

## Commands

- Run app: `uv run streamlit run app.py`.
- Compile check: `uv run python -m compileall -q app.py pages utils`.
- Test: `uv run pytest`.
- Lint: `uv run ruff check .`.
- Format check: `uv run ruff format --check .`.
- Format: `uv run ruff format .`.

## Architecture

- `app.py`: navigation and application bootstrap.
- `pages/`: Streamlit pages.
- `utils/data.py`: deterministic demo and case-study datasets.
- `utils/theme.py`: shared visual tokens and Plotly palettes.
- `utils/ui.py`: shared layout and UI components.
- `.streamlit/config.toml`: Streamlit shell theme and server configuration.
- `assets/`: repository-managed visual assets.
- `data/raw/` and `data/private/`: ignored local data.
- `outputs/`: ignored generated artifacts.

## Change Rules

- Inspect `git status` before editing and preserve unrelated user changes.
- Prefer shared helpers and theme tokens over page-local duplication.
- Do not hard-code colors when a named token exists in `utils/theme.py`.
- Do not place reusable transformations only in notebooks or page modules.
- Keep generated demo data deterministic.
- Do not claim that an analysis uses production or observed data unless verified.
- Never expose secrets through source, logs, screenshots, or committed configuration.
- Update `pyproject.toml` and regenerate `uv.lock` for dependency changes.
- Keep `environment.yml` and `requirements.txt` compatible when deployment consumers require them.

## Validation

- Run compile, lint, format-check, and tests after relevant changes.
- For UI changes, execute affected pages with `streamlit.testing.v1.AppTest` when practical.
- Verify the local app at `http://localhost:8501` for navigation or rendering changes.

## Product Constraints

- Voice: direct, technical, professional, and evidence-based.
- Avoid recruiter-directed copy, fake claims, and unsupported performance claims.
- Preserve the premium analytics-product visual direction documented in `PROJECT_CONTEXT.md`.
- Update `PROJECT_CONTEXT.md` when navigation, architecture, theme ownership, or major page behavior changes.
