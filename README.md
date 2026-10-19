# Data Science Career Website

This is a Streamlit starter project for a personal career website with project
summaries, interactive dashboards, and saved model-result visualizations.

## Create the Anaconda Environment

```powershell
conda env create -f environment.yml
conda activate career-site
```

If you already created the environment and later change dependencies:

```powershell
conda env update -f environment.yml --prune
```

## Run Locally

```powershell
streamlit run app.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

## Update the Macro Snapshot

The macro page uses a static, source-linked snapshot and makes no network requests
at runtime. In `utils/data.py`, add each new `YYYY-MM` value to the relevant
`monthly_signals` observations in `load_macro_kpi_data()`. The newest observation
automatically updates its KPI card. Update that signal's `source_url` and
`released` fields, the quarterly cards when new releases arrive, and
`MACRO_SNAPSHOT_CUTOFF`. Keep the source page and reference period together.

Run `python -m unittest discover -s tests` to check the data contract before
deploying. The working Streamlit Cloud configuration uses `environment.yml`;
this page does not require `pyproject.toml` or `uv.lock`.

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
|-- environment.yml
|-- requirements.txt
`-- README.md
```

## Deploy Later

Good first deployment options:

- Streamlit Community Cloud
- Render
- Hugging Face Spaces

For Streamlit Community Cloud, push this folder to GitHub and choose `app.py`
as the main file.
