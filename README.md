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
