from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from utils.data import MACRO_SNAPSHOT_CUTOFF, load_macro_kpi_data
from utils.theme import MACRO_COLORS, THEME
from utils.ui import inject_global_styles, render_insight, render_kpi_card


inject_global_styles()

st.markdown(
    """
    <section class="hero">
        <p class="eyebrow">Public macro-financial monitoring</p>
        <h1>Macro-economy and financial KPI tracker.</h1>
        <p class="hero-copy">
            A professional monitoring page for Canadian and global macro signals:
            inflation, labour market conditions, oil prices, and output. Each reading
            is tied to its published period and source, with monthly trends shown on
            separate scales so unlike units are not compared as if equivalent.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

cards, trends = load_macro_kpi_data()

with st.sidebar:
    st.header("Trend controls")
    selected_indicators = st.multiselect(
        "Monthly indicators",
        list(trends["indicator"].unique()),
        default=list(trends["indicator"].unique()),
    )

filtered_trends = trends[trends["indicator"].isin(selected_indicators)]

st.subheader("Executive KPI Snapshot")
st.caption(
    f"Static snapshot through {MACRO_SNAPSHOT_CUTOFF}. Reference periods vary by release schedule; "
    "September CPI is not included."
)
for chunk_start in range(0, len(cards), 3):
    cols = st.columns(3)
    for col, (_, row) in zip(cols, cards.iloc[chunk_start : chunk_start + 3].iterrows()):
        with col:
            value = f"${row['value']:.2f}" if row["unit"] == "USD/bbl" else f"{row['value']:.1f}%"
            render_kpi_card(
                f"{row['region']} | {row['indicator']}",
                value,
                f"{row['period']} | {row['basis']}",
            )

st.divider()

st.subheader("Monthly signals")
st.caption("Canada CPI and unemployment alongside the U.S. WTI oil benchmark. Each lane uses its own unit and scale.")

signal_specs = {
    "CPI inflation": ("CPI inflation", MACRO_COLORS[0], "%", ".1f"),
    "Unemployment rate": ("Unemployment rate", MACRO_COLORS[1], "%", ".1f"),
    "WTI crude oil": ("WTI crude oil", MACRO_COLORS[2], "USD/bbl", ".2f"),
}
visible_signals = [indicator for indicator in signal_specs if indicator in selected_indicators]
if visible_signals:
    trend_fig = make_subplots(
        rows=len(visible_signals),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.12 if len(visible_signals) > 1 else 0,
        subplot_titles=[signal_specs[indicator][0] for indicator in visible_signals],
    )
    for row_number, indicator in enumerate(visible_signals, start=1):
        series = filtered_trends[filtered_trends["indicator"] == indicator].sort_values("period")
        _, color, unit, precision = signal_specs[indicator]
        dates = pd.to_datetime(series["period"] + "-01")
        suffix = "%" if unit == "%" else " USD/bbl"
        trend_fig.add_trace(
            go.Scatter(
                x=dates,
                y=series["value"],
                mode="lines+markers",
                line={"color": color, "width": 2.5},
                marker={"color": color, "size": 6},
                hovertemplate=f"%{{x|%b %Y}}<br>%{{y:{precision}}}{suffix}<extra></extra>",
            ),
            row=row_number,
            col=1,
        )
        trend_fig.update_yaxes(
            title_text=unit,
            gridcolor=THEME["grid"],
            zeroline=False,
            row=row_number,
            col=1,
        )
    trend_fig.update_xaxes(tickformat="%b '%y", dtick="M2", showgrid=False, linecolor=THEME["line"])
    trend_fig.update_layout(
        height=190 * len(visible_signals) + 80,
        showlegend=False,
        hovermode="closest",
        margin={"l": 58, "r": 24, "t": 48, "b": 36},
        paper_bgcolor=THEME["soft_light"],
        plot_bgcolor=THEME["soft_light"],
        font={"color": THEME["ink"]},
    )
    trend_fig.update_annotations(font={"color": THEME["ink"], "size": 14})
    st.plotly_chart(trend_fig, width="stretch")
else:
    st.info("Select a monthly indicator in the sidebar to show its trend.")

render_insight(
    "Inflation signals household price pressure, unemployment describes labour slack, "
    "and oil prices add an energy-cost benchmark. The series have different units "
    "and release lags; their line heights are not directly comparable."
)

st.subheader("Release ledger")
st.dataframe(
    cards[["region", "indicator", "value", "unit", "period", "basis", "released", "source_url"]],
    column_config={"source_url": st.column_config.LinkColumn("Source")},
    width="stretch",
    hide_index=True,
)

with st.expander("Source and refresh notes"):
    st.markdown(
        f"""
        This is a static snapshot through **{MACRO_SNAPSHOT_CUTOFF}**, not a live feed.
        CPI is the 12-month all-items change; unemployment is seasonally adjusted;
        WTI is the unweighted monthly average of Cushing spot prices in U.S. dollars
        per barrel. GDP and GDP-per-capita cards show change from the previous quarter,
        not an annualized rate. Each series ends at its latest included reference period.

        Monthly history: [CPI](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810000402),
        [unemployment](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410028701),
        and [WTI oil](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RWTC&f=M).
        Release links and dates are in the ledger above. No external request runs when
        this page loads.
        """
    )
