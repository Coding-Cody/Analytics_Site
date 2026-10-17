from __future__ import annotations

from pathlib import Path

import streamlit as st

from utils.ui import inject_global_styles, render_contact_card, render_focus_card, render_project_card


inject_global_styles()

st.markdown(
    """
    <section class="hero">
        <p class="eyebrow">Cody Xu | Data science and analytics portfolio</p>
        <h1>Interactive analytics work built for business decisions.</h1>
        <p class="hero-copy">
            Welcome. This portfolio is built as an interactive analytics app: causal
            measurement, marketing science, macro-financial monitoring, and decision
            dashboards in one place. Each section connects methods, assumptions,
            uncertainty, and business action.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

render_contact_card(Path(__file__).resolve().parents[1] / "Cody.JPG")

st.markdown(
    """
    <div class="section-band">
        <h3>Technical focus</h3>
        <p>
            The purpose of this app is to demonstrate applied data science work in
            a structured way: measurement design, model interpretation, dashboard
            logic, KPI monitoring, and the statistical assumptions behind each view.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Focus Areas")
focus_cols = st.columns(4)
focus_items = [
    ("target", "Marketing Analytics", "Channel impact, incrementality, ROI, and budget allocation."),
    ("map", "Geo Experimentation", "Matched-market design, synthetic controls, DiD, and lift inference."),
    ("curve", "MMM", "Bayesian hierarchy, ad-stock, Hill saturation, priors, and posteriors."),
    ("dashboard", "Dashboarding", "Executive-ready Streamlit and Plotly decision surfaces."),
    ("forecast", "Forecasting", "Trend, seasonality, decomposition, and scenario monitoring."),
    ("cluster", "Clustering", "Segmentation, similarity scoring, cohort discovery, profiling, and actionability checks."),
    ("database", "Programming", "Python, PySpark, SQL, analytical pipelines, feature shaping, and repeatable reporting."),
    ("mlops", "MLOps", "Model packaging, monitoring, reproducible pipelines, deployment readiness, and governance."),
]

for index, item in enumerate(focus_items):
    with focus_cols[index % 4]:
        render_focus_card(item[0], item[1], item[2])

st.divider()

st.subheader("Featured Sections")
projects = [
    {
        "title": "Marketing Mix Modelling",
        "status": "Deep dive",
        "body": "Bayesian measurement workspace for carryover, saturation, marginal returns, and budget planning decisions.",
        "icon": "analytics",
        "tags": ("Bayesian MMM", "ROI", "Planning"),
        "accent": "rgba(20, 184, 166, 0.28)",
    },
    {
        "title": "Geo-based Incrementality Test",
        "status": "Case study",
        "body": "Causal testing layer for matched markets, synthetic controls, lift reads, and pre-period validity checks.",
        "icon": "map",
        "tags": ("Causal lift", "Markets", "DiD"),
        "accent": "rgba(37, 99, 235, 0.24)",
    },
    {
        "title": "Customer Segmentation",
        "status": "Case study",
        "body": "Luxury customer intelligence with engineered features, segment economics, affinity signals, and activation logic.",
        "icon": "groups",
        "tags": ("Clustering", "LTV", "Activation"),
        "accent": "rgba(190, 24, 93, 0.20)",
    },
    {
        "title": "Sales Dashboard",
        "status": "Dashboard",
        "body": "Operating command surface for KPI diagnostics, margin pressure, product drill-downs, and sales performance.",
        "icon": "dashboard",
        "tags": ("KPI Ops", "Margin", "Drill-down"),
        "accent": "rgba(208, 138, 29, 0.24)",
    },
    {
        "title": "Macro & Financial KPI Tracker",
        "status": "Live section",
        "body": "Monitoring suite for global and Canadian indicators, financial signals, trend charts, and decision context.",
        "icon": "monitoring",
        "tags": ("Macro", "Markets", "Trends"),
        "accent": "rgba(124, 58, 237, 0.20)",
    },
]

top_featured_cols = st.columns(3)
for index, project in enumerate(projects[:3]):
    with top_featured_cols[index]:
        render_project_card(
            project["title"],
            project["status"],
            project["body"],
            icon=project["icon"],
            index=index + 1,
            tags=project["tags"],
            accent=project["accent"],
        )

bottom_featured_cols = st.columns(2)
for offset, project in enumerate(projects[3:]):
    index = offset + 3
    with bottom_featured_cols[offset]:
        render_project_card(
            project["title"],
            project["status"],
            project["body"],
            icon=project["icon"],
            index=index + 1,
            tags=project["tags"],
            accent=project["accent"],
        )

