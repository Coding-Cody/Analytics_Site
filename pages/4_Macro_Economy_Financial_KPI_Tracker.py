from __future__ import annotations

import plotly.express as px
import streamlit as st

from utils.data import load_macro_kpi_data
from utils.theme import MACRO_COLORS
from utils.ui import inject_global_styles, render_insight, render_kpi_card


inject_global_styles()

st.markdown(
    """
    <section class="hero">
        <p class="eyebrow">Public macro-financial monitoring</p>
        <h1>Macro-economy and financial KPI tracker.</h1>
        <p class="hero-copy">
            A professional monitoring page for Canadian and global macro signals:
            inflation, labour market pressure, policy rates, growth, and financial
            context for business planning. The analytical framing emphasizes indicator
            normalization, signal direction, policy context, and KPI monitoring.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

cards, trends = load_macro_kpi_data()

with st.sidebar:
    st.header("KPI Controls")
    selected_regions = st.multiselect(
        "Regions",
        sorted(cards["region"].unique()),
        default=sorted(cards["region"].unique()),
    )
    selected_indicators = st.multiselect(
        "Trend indicators",
        sorted(trends["indicator"].unique()),
        default=sorted(trends["indicator"].unique()),
    )

filtered_cards = cards[cards["region"].isin(selected_regions)]
filtered_trends = trends[trends["indicator"].isin(selected_indicators)]

st.subheader("Executive KPI Snapshot")
st.caption(
    "Static snapshot checked 17 Oct 2026. Reference periods vary by release schedule; "
    "September CPI is not yet published."
)
for chunk_start in range(0, len(filtered_cards), 3):
    cols = st.columns(3)
    for col, (_, row) in zip(cols, filtered_cards.iloc[chunk_start : chunk_start + 3].iterrows()):
        with col:
            value = f"{row['value']:.2f}{row['unit'] if row['unit'].startswith('%') else ' ' + row['unit']}"
            render_kpi_card(
                f"{row['region']} | {row['indicator']}",
                value,
                f"{row['period']} | {row['status']}",
            )

st.divider()

st.markdown(
    """
    <div class="method-note">
        <strong>Analytical layer:</strong> a production macro tracker should normalize
        indicators with rolling z-scores, flag regime shifts, compare nominal rates with
        inflation to estimate real-rate pressure, and preserve source metadata for every
        refresh. This page structures the KPI view around growth, labour slack, inflation
        pressure, and financing cost.
    </div>
    """,
    unsafe_allow_html=True,
)

trend_fig = px.line(
    filtered_trends,
    x="period",
    y="value",
    color="indicator",
    markers=True,
    title="Macro-financial Trend Monitor",
    labels={"period": "Period", "value": "Value", "indicator": "Indicator"},
    color_discrete_sequence=MACRO_COLORS,
)
trend_fig.update_layout(hovermode="x unified")
st.plotly_chart(trend_fig, width="stretch")
render_insight(
    "This view keeps planning context close to business KPIs: inflation affects pricing and consumer pressure, unemployment affects demand and labour conditions, and policy rates influence financing and discount-rate assumptions."
)

left, right = st.columns([1, 1], gap="small")
with left:
    heatmap_df = filtered_cards.copy()
    heatmap_df["display_value"] = heatmap_df["value"]
    heatmap_fig = px.imshow(
        heatmap_df.pivot_table(
            index="indicator",
            columns="region",
            values="display_value",
            aggfunc="mean",
        ),
        text_auto=".2f",
        aspect="auto",
        title="KPI Heatmap by Region",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(heatmap_fig, width="stretch")

with right:
    st.markdown(
        """
        <div class="section-band paired-card">
            <h3>Monitoring logic</h3>
            <p>
                The tracker is organized around signals that matter for planning:
                demand temperature, household pressure, financing cost, and global
                growth context. Data science work behind this type of dashboard usually
                includes API ingestion, calendar alignment, missing-value rules, release
                date metadata, rolling normalization, anomaly flags, and lead/lag analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.expander("Source and refresh notes"):
    st.markdown(
        """
        This static snapshot was checked on **17 October 2026**. CPI is the 12-month
        all-items change; unemployment is the seasonally adjusted national rate; the
        policy rate is the Bank of Canada's month-end overnight target. GDP and GDP per capita
        cards show quarter-over-quarter real growth. The monthly chart covers Canada
        only, with each series ending at its latest published reference month.

        - [CPI, August 2026](https://www150.statcan.gc.ca/n1/daily-quotidien/260914/dq260914a-eng.htm)
        - [Labour Force Survey, September 2026](https://www150.statcan.gc.ca/n1/daily-quotidien/261009/dq261009a-eng.htm)
        - [Bank of Canada policy rate](https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rate/)
        - [Canadian GDP, Q2 2026](https://www150.statcan.gc.ca/n1/daily-quotidien/260828/dq260828a-eng.htm)
        - [OECD and G7 GDP per capita, Q1 2026](https://www.oecd.org/content/dam/oecd/en/data/insights/statistical-releases/2026/8/Growth-and-economic-well-being-oecd-08-2026.pdf)

        Monthly history: [CPI](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810000402)
        and [unemployment](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410028701).
        This app keeps a static snapshot so it can run without API credentials.
        """
    )
    st.dataframe(filtered_cards, width="stretch", hide_index=True)

