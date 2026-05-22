from __future__ import annotations

import streamlit as st

from utils.ui import inject_global_styles, render_project_card, render_stat_card, render_welcome_card


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

top_cols = st.columns([1.15, 0.85], gap="large")
with top_cols[0]:
    st.markdown(
        """
        <div class="section-band">
            <h3>Portfolio positioning</h3>
            <p>
                This app is designed for recruiters, hiring managers, and business
                partners who want to see how analytical work translates into decisions:
                where to invest, what changed, which markets to compare, and how to
                monitor performance with enough statistical discipline.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with top_cols[1]:
    st.markdown(
        """
        <div class="contact-card">
            <a href="https://www.linkedin.com/in/codyxu94/" target="_blank">LinkedIn: codyxu94</a>
            <a href="https://github.com/Coding-Cody" target="_blank">GitHub: Coding-Cody</a>
            <a href="mailto:codyxu94@gmail.com">codyxu94@gmail.com</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Focus Areas")
focus_cols = st.columns(4)
focus_items = [
    ("Marketing Analytics", "Channel impact, incrementality, ROI, and budget allocation."),
    ("Geo Experimentation", "Matched-market design, synthetic controls, DiD, and lift inference."),
    ("MMM", "Bayesian hierarchy, ad-stock, Hill saturation, priors, and posteriors."),
    ("Dashboarding", "Executive-ready Streamlit and Plotly decision surfaces."),
    ("Forecasting", "Trend, seasonality, decomposition, and scenario monitoring."),
    ("Experimentation", "Power, uncertainty, lift, confidence intervals, and validity checks."),
    ("Python + SQL", "Pipelines, analytical marts, feature shaping, and repeatable reporting."),
    ("Financial KPIs", "Macro signals, rate context, z-scores, and KPI monitoring."),
]

for index, item in enumerate(focus_items):
    with focus_cols[index % 4]:
        render_stat_card(item[0], item[1])

st.divider()

st.subheader("Section Guide")
welcome_cols = st.columns(5)
welcome_sections = [
    (
        "Home",
        "App Introduction",
        "A guided overview of Cody's analytics portfolio, focus areas, contact links, and project roadmap.",
    ),
    (
        "Map",
        "Geo Incrementality",
        "Market-level causal measurement using matched markets, synthetic controls, DiD, and uncertainty checks.",
    ),
    (
        "MMM",
        "Marketing Mix Modelling",
        "Bayesian MMM concepts including ad-stock, Hill saturation, response curves, ROI, and contribution.",
    ),
    (
        "BI",
        "Third-party Dashboard",
        "A reserved dashboard area for external data, benchmarks, filters, and professional reporting.",
    ),
    (
        "KPI",
        "Macro KPI Tracker",
        "Canadian and global macro-financial indicators for planning context and executive monitoring.",
    ),
]

for col, section in zip(welcome_cols, welcome_sections):
    with col:
        render_welcome_card(section[0], section[1], section[2])

st.divider()

st.subheader("Featured Sections")
card_cols = st.columns(4)
projects = [
    {
        "title": "Geo-based Incrementality Test",
        "status": "Case study",
        "body": "Matched-market and synthetic-control views for market-level lift, pre-period fit, DiD estimation, and causal validity.",
    },
    {
        "title": "Marketing Mix Modelling",
        "status": "Deep dive",
        "body": "Bayesian MMM concepts with hierarchical pooling, ad-stock carryover, Hill saturation, marginal returns, and planning.",
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
