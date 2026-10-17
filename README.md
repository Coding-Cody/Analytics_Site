# Data Science Career Website

An interactive Streamlit portfolio covering causal measurement, marketing science,
customer segmentation, retail analytics, and macro-financial monitoring.

## Quick Start

Install [uv](https://docs.astral.sh/uv/), clone the repository, and run:

```powershell
git clone https://github.com/Coding-Cody/Analytics_Site.git
cd Analytics_Site
uv sync --locked
uv run streamlit run app.py
```

The app will normally be available at [http://localhost:8501](http://localhost:8501).

## Conda Alternative

An Anaconda environment definition is retained for workflows that use Conda:

```powershell
conda env create -f environment.yml
conda activate career-site
streamlit run app.py
```

To synchronize an existing Conda environment after dependency changes:

```powershell
conda env update -f environment.yml --prune
```

## Run Locally

```powershell
streamlit run app.py
```

Using uv:

```powershell
uv run streamlit run app.py
```

## Project Structure

```text
.
|-- app.py
|-- pages/
|   |-- 1_Project_Gallery.py
|   |-- 2_Interactive_Dashboard.py
|   `-- 3_Model_Results.py
|-- utils/
|   `-- data.py
|-- .streamlit/
|   `-- config.toml
|-- AGENTS.md
|-- pyproject.toml
|-- uv.lock
|-- .python-version
|-- environment.yml
|-- requirements.txt
`-- README.md
```

`pyproject.toml` and `uv.lock` are the primary dependency definitions. The Conda
and requirements files are retained for compatible deployment environments.

## Development Checks

```powershell
uv run python -m compileall -q app.py pages utils
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## Deployment

Good first deployment options:

- Streamlit Community Cloud
- Render
- Hugging Face Spaces

For Streamlit Community Cloud, push this folder to GitHub and choose `app.py`
as the main file.
