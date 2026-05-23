# Career Website Project Context

Use this file as the handoff prompt for future work on this Streamlit portfolio.

## Project Context

Working folder:

```text
C:\aaa - Data and files\A - Vibe coding\Career website
```

Existing conda environment:

```text
career-site
```

Useful direct paths:

```text
Python:
C:\Users\ziyan\anaconda3\envs\career-site\python.exe

Streamlit:
C:\Users\ziyan\anaconda3\envs\career-site\Scripts\streamlit.exe
```

Run app:

```powershell
conda activate career-site
streamlit run app.py
```

If `conda` is not on PATH, use the direct env Python/Streamlit paths above.

## Current App Structure

Framework: Streamlit

Entry point:

```text
app.py
```

Navigation uses Streamlit top navigation:

```python
st.navigation(pages, position="top")
```

Current tabs/pages:

1. App Introduction
2. Marketing Mix Modelling
3. Geo-based Incrementality Test
4. Third-party Data Dashboard
5. Macro-economy & Financial KPI Tracker

MMM intentionally comes before Geo.

## Main Files

```text
app.py
pages/0_App_Introduction.py
pages/1_Geo_Based_Incrementality_Test.py
pages/2_Marketing_Mix_Modelling_Google_Meridian.py
pages/3_Third_Party_Data_Dashboard.py
pages/4_Macro_Economy_Financial_KPI_Tracker.py
utils/data.py
utils/theme.py
utils/ui.py
.streamlit/config.toml
```

## Style Direction

Overall style should be:

- Professional but cool
- Premium dashboard / analytics product feel
- Bold but not loud
- Dark editorial hero sections
- Warm off-white page background
- Muted teal / emerald as the primary accent
- Muted gold and violet as secondary accents
- Soft premium cards with shadows
- Top horizontal navigation, not sidebar-first
- Equal-height cards in rows
- Comfortable spacing between chunks
- Charts should be readable and not overly saturated

Theme is in `.streamlit/config.toml`:

```toml
[theme]
base = "light"
primaryColor = "#14b8a6"
backgroundColor = "#f4efe3"
secondaryBackgroundColor = "#fffaf0"
textColor = "#141a16"
font = "sans serif"
```

Most app-level colors and chart palettes are centralized in:

```text
utils/theme.py
```

Use this file first when changing the visual theme. It defines:

- `THEME` for CSS and Plotly tokens
- `PLOTLY_COLORWAY`
- `CHANNEL_COLORS`
- `MMM_KPI_COLORS`
- `GEO_COLORS`
- `MACRO_COLORS`

Streamlit still requires a few static theme values in `.streamlit/config.toml`, so update that file only for the Streamlit shell theme. Page code should import named colors from `utils/theme.py` instead of hard-coding hex values.

Most reusable layout and component styling is centralized in:

```text
utils/ui.py
```

## Tone Rules

Use Cody's voice as a technical demonstration, not a third-person sales pitch.

Good tone:

```text
Welcome. This portfolio is built as an interactive analytics app: causal measurement, marketing science, macro-financial monitoring, and decision dashboards in one place.
```

Avoid:

```text
This app is designed for recruiters, hiring managers...
```

Tone should be:

- Direct
- Technical
- Professional
- Confident but not braggy
- No fake claims
- No "AI portfolio" sounding language
- No awkward recruiter/hiring-manager framing
- Cody is demonstrating applied work

## Design Components

Reusable UI helpers in `utils/ui.py`:

- `inject_global_styles()`
- `render_project_card()`
- `render_focus_card()`
- `render_insight()`
- `render_kpi_card()`

Important layout rules already applied:

- Multi-card rows use equal heights.
- Focus Areas use pictogram-style SVG icons, not letters.
- KPI rows use custom KPI cards, not default `st.metric`, where formatting matters.
- Paired explanation cards use `paired-card`.
- App intro contact/profile card sits near the top under the hero and uses `Cody.JPG` as a circular cropped image.

## MMM Page

File:

```text
pages/2_Marketing_Mix_Modelling_Google_Meridian.py
```

Current content includes:

- Bayesian hierarchical MMM framing
- Google Meridian workflow
- Ad-stock
- Hill saturation
- `alpha`
- `ec50`
- Contribution
- ROI
- Marginal return
- Budget scenario

Current charts:

- Media Spend Over Time by Channel
- KPI and Estimated Media Contribution Over Time
- Channel Contribution
- ROI / Effectiveness Comparison
- Ad-stocked Media Pressure
- Saturation Curves
- Marginal Return by Spend Level
- Budget Planning Scenario

Color rule:

- Channel-based charts use `CHANNEL_COLORS` from `utils/theme.py`.
- Keep **KPI and Estimated Media Contribution Over Time** on `MMM_KPI_COLORS` from `utils/theme.py`, which intentionally uses a special KPI/contribution treatment.

## Geo Page

File:

```text
pages/1_Geo_Based_Incrementality_Test.py
```

Includes:

- Matched-market test
- Synthetic control
- Test and control FSA/city market chips
- Difference-in-differences
- ATT framing
- Pre-period fit
- t-statistic
- Synthetic control RMSE
- Treatment effect interpretation

Market matching setup uses chip-style labels, not plain text.

## Macro KPI Page

File:

```text
pages/4_Macro_Economy_Financial_KPI_Tracker.py
```

Includes:

- Canada/global macro-financial KPI cards
- Trend monitor
- KPI heatmap
- Source/refresh notes
- Analytical framing around z-scores, policy context, real-rate pressure, metadata, API ingestion

## Data

Demo/internal case-study data is generated in:

```text
utils/data.py
```

Important: the UI should avoid visible "demo only" or "simulated data" language unless specifically requested.

## QA Pattern

Use:

```powershell
& 'C:\Users\ziyan\anaconda3\envs\career-site\python.exe' -m compileall app.py pages utils
```

Render checks:

```python
from streamlit.testing.v1 import AppTest

files = [
    "app.py",
    "pages/0_App_Introduction.py",
    "pages/1_Geo_Based_Incrementality_Test.py",
    "pages/2_Marketing_Mix_Modelling_Google_Meridian.py",
    "pages/3_Third_Party_Data_Dashboard.py",
    "pages/4_Macro_Economy_Financial_KPI_Tracker.py",
]

for f in files:
    at = AppTest.from_file(f, default_timeout=20).run()
    assert not at.exception, (f, at.exception)
```

Also check local server:

```powershell
Invoke-WebRequest -Uri 'http://localhost:8501' -UseBasicParsing
```

## Known Environment Notes

- `conda` was not always recognized on PowerShell PATH.
- Direct env paths work.
- `git` was previously not recognized on PATH.
- GitHub connector is connected as `Coding-Cody`, but local Git setup may still need Git for Windows / VS Code Git.
