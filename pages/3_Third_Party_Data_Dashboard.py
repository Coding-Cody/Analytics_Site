from __future__ import annotations

import streamlit as st

from utils.ui import inject_global_styles


inject_global_styles()

st.markdown(
    """
    <section class="hero">
        <p class="eyebrow">Planned portfolio section</p>
        <h1>Third-party data professional dashboard - coming next.</h1>
        <p class="hero-copy">
            This page is reserved for a dashboard using external data sources, benchmark
            comparisons, and executive-ready reporting interactions. The planned design
            will emphasize source validation, metric definitions, segmentation, and
            reproducible KPI calculations.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="small")

with left:
    st.markdown(
        """
        <div class="placeholder-panel paired-card">
            <h3>Planned dashboard space</h3>
            <p>
                The future build can include source selectors, market filters, KPI cards,
                benchmark comparisons, and Plotly charts for a polished third-party data
                story. The data science layer can include schema checks, outlier handling,
                rolling baselines, peer-group normalization, and confidence bands.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="section-band paired-card">
            <h3>Design intent</h3>
            <p>
                A quiet professional dashboard with dense but readable information,
                not a marketing landing page. The target structure is an analytical
                workspace: filters on top, KPI diagnostics in the middle, and drill-down
                charts below.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

