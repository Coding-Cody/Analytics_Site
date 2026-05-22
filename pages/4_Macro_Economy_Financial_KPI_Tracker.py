from __future__ import annotations

import plotly.express as px
import streamlit as st

from utils.data import load_macro_kpi_data
from utils.ui import inject_global_styles, render_insight


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
for chunk_start in range(0, len(filtered_cards), 3):
    cols = st.columns(3)
    for col, (_, row) in zip(cols, filtered_cards.iloc[chunk_start : chunk_start + 3].iterrows()):
        col.metric(
            f"{row['region']} | {row['indicator']}",
            f"{row['value']:.2f}{row['unit'] if row['unit'].startswith('%') else ' ' + row['unit']}",
            row["period"],
        )
        col.caption(f"{row['status']} | {row['source']}")

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
    color_discrete_sequence=["#2563eb", "#0f766e", "#be185d", "#f97316"],
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
        <div class="section-band">
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
    st.write(
        """
        Sources referenced for this portfolio view include Statistics Canada, Bank of
        Canada, OECD statistical releases, and public indicator feeds. The current app
        keeps a lightweight static snapshot so it can run locally and deploy without
        API credentials. A production dashboard should add source-specific refresh jobs,
        metadata timestamps, and validation checks.
        """
    )
    st.dataframe(filtered_cards, width="stretch", hide_index=True)

