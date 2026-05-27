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
card_cols = st.columns(5)
projects = [
    {
        "title": "Marketing Mix Modelling",
        "status": "Deep dive",
        "body": "Bayesian MMM concepts with hierarchical pooling, ad-stock carryover, Hill saturation, marginal returns, and planning.",
    },
    {
        "title": "Geo-based Incrementality Test",
        "status": "Case study",
        "body": "Matched-market and synthetic-control views for market-level lift, pre-period fit, DiD estimation, and causal validity.",
    },
    {
        "title": "Customer Segmentation",
        "status": "Case study",
        "body": "Premium menswear customer clustering with feature engineering, segment economics, affinity signals, and activation logic.",
    },
    {
        "title": "Third-party Data Dashboard",
        "status": "Next build",
        "body": "Reserved for a professional dashboard using external data, filters, KPI cards, and benchmark comparisons.",
    },
    {
        "title": "Macro & Financial KPI Tracker",
        "status": "Live section",
        "body": "Global and Canadian macro-financial indicators with KPI cards, trend charts, and monitoring context.",
    },
]

for col, project in zip(card_cols, projects):
    with col:
        render_project_card(project["title"], project["status"], project["body"])

