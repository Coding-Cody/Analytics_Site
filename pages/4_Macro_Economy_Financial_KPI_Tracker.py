from __future__ import annotations

import html
from textwrap import dedent

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.data import load_macro_kpi_data
from utils.theme import MACRO_COLORS, THEME
from utils.ui import inject_global_styles


inject_global_styles()
st.markdown(
    """
    <style>
        .macro-masthead {
            display: flex;
            justify-content: space-between;
            gap: 2rem;
            align-items: end;
            padding: 1.2rem 1.5rem;
            background: __DEEP__;
            color: #ffffff;
            border-radius: 6px;
            margin-bottom: 0.45rem;
        }
        .macro-eyebrow {
            margin: 0 0 0.55rem;
            color: __ACCENT__;
            font-size: 0.76rem;
            font-weight: 750;
            text-transform: uppercase;
        }
        .macro-masthead h1 {
            color: #ffffff;
            font-size: 2.1rem;
            line-height: 1.08;
            margin: 0 0 0.4rem;
        }
        .macro-masthead p {
            margin: 0;
            color: #d7e2dc;
            line-height: 1.5;
            max-width: 40rem;
        }
        .macro-asof {
            border-left: 1px solid #52645a;
            padding-left: 1.2rem;
            flex: 0 0 11rem;
        }
        .macro-asof span, .macro-asof small {
            display: block;
            color: #bad0c4;
            font-size: 0.72rem;
        }
        .macro-asof strong {
            display: block;
            color: #ffffff;
            font-size: 1.1rem;
            margin: 0.3rem 0;
        }
        .macro-section-head {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 1rem;
            margin: 0.3rem 0 0.8rem;
        }
        .macro-section-head h2 {
            margin: 0;
            padding: 0;
            border: 0;
            font-size: 1.35rem;
            line-height: 1.2;
        }
        .macro-section-head p {
            margin: 0;
            color: __MUTED__;
            font-size: 0.86rem;
        }
        .macro-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.7rem;
            margin-bottom: 0.6rem;
        }
        .macro-metric {
            min-height: 175px;
            display: flex;
            flex-direction: column;
            padding: 1rem 1.05rem 0.85rem;
            border: 1px solid __LINE__;
            border-top: 3px solid var(--metric-accent);
            border-radius: 6px;
            background: #ffffff;
            box-sizing: border-box;
        }
        .macro-metric-label {
            min-height: 2.4rem;
            color: __INK__;
            font-size: 0.9rem;
            font-weight: 720;
            line-height: 1.25;
        }
        .macro-metric-value {
            color: __INK__;
            font-size: 2.2rem;
            font-weight: 760;
            line-height: 1.05;
            margin: 0.25rem 0;
        }
        .macro-metric-basis {
            color: __MUTED__;
            font-size: 0.79rem;
            line-height: 1.3;
        }
        .macro-metric-foot {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            gap: 0.35rem;
            margin-top: auto;
            padding-top: 0.75rem;
            border-top: 1px solid #e8ece8;
            font-size: 0.77rem;
        }
        .macro-metric-foot strong {
            color: __INK__;
        }
        .macro-metric-foot a, .macro-source-link {
            color: #0b6f76;
            text-decoration: underline;
            text-underline-offset: 2px;
        }
        .macro-reading {
            border-left: 3px solid var(--series-accent);
            padding: 0.3rem 0 0.3rem 1.1rem;
            margin-top: 1.5rem;
        }
        .macro-reading-label {
            color: __MUTED__;
            font-size: 0.76rem;
            text-transform: uppercase;
            font-weight: 750;
        }
        .macro-reading strong {
            display: block;
            color: __INK__;
            font-size: 2rem;
            margin: 0.2rem 0;
        }
        .macro-reading p {
            color: __MUTED__;
            font-size: 0.86rem;
            margin: 0.3rem 0;
            line-height: 1.45;
        }
        .macro-reading .macro-period {
            color: __INK__;
            font-weight: 700;
        }
        .macro-divider {
            border-top: 1px solid __LINE__;
            margin: 1.8rem 0 1.35rem;
        }
        .macro-method {
            color: __MUTED__;
            font-size: 0.85rem;
            line-height: 1.5;
            margin: 0 0 0.8rem;
        }
        div[data-testid="stPlotlyChart"] {
            background: #ffffff;
            box-shadow: none;
            border-color: __LINE__;
        }
        @media (max-width: 1000px) {
            .macro-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
        @media (max-width: 620px) {
            .macro-masthead { display: block; padding: 1.3rem; }
            .macro-masthead h1 { font-size: 1.85rem; }
            .macro-asof {
                border-left: 0;
                border-top: 1px solid #52645a;
                padding: 0.75rem 0 0;
                margin-top: 1rem;
            }
            .macro-grid { grid-template-columns: 1fr; }
            .macro-section-head { display: block; }
            .macro-section-head p { margin-top: 0.35rem; }
            .macro-metric { min-height: 165px; }
            .macro-reading { margin: 0.6rem 0 1.2rem; }
        }
    </style>
    """
    .replace("__DEEP__", THEME["deep"])
    .replace("__ACCENT__", THEME["accent"])
    .replace("__MUTED__", THEME["muted"])
    .replace("__INK__", THEME["ink"])
    .replace("__LINE__", THEME["line"]),
    unsafe_allow_html=True,
)

cards, trends = load_macro_kpi_data()
card_lookup = cards.set_index(["region", "indicator"])

st.markdown(
    """
    <header class="macro-masthead">
        <div>
            <div class="macro-eyebrow">Public data / Canada</div>
            <h1>Macro monitor</h1>
            <p>Inflation, labour, policy and output, with each reading tied to its
            published period and official release.</p>
        </div>
        <div class="macro-asof">
            <span>SNAPSHOT VERIFIED</span>
            <strong>17 Oct 2026</strong>
            <small>Static public data</small>
        </div>
    </header>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="macro-section-head">
        <h2>Canada at a glance</h2>
        <p>Latest available reading for each indicator</p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_specs = (
    ("CPI inflation", "12-month change in all-items prices", MACRO_COLORS[0], 1),
    ("Unemployment rate", "Seasonally adjusted labour-force rate", MACRO_COLORS[1], 1),
    ("Policy rate", "Bank of Canada overnight target", MACRO_COLORS[2], 2),
    ("Real GDP growth", "Change from the previous quarter", MACRO_COLORS[3], 1),
)
metric_markup = []
for indicator, basis, accent, decimals in metric_specs:
    row = card_lookup.loc[("Canada", indicator)]
    metric_markup.append(
        dedent(
            f"""
        <article class="macro-metric" style="--metric-accent: {html.escape(accent, quote=True)}">
            <div class="macro-metric-label">{html.escape(indicator)}</div>
            <div class="macro-metric-value">{row['value']:.{decimals}f}%</div>
            <div class="macro-metric-basis">{html.escape(basis)}</div>
            <div class="macro-metric-foot">
                <strong>{html.escape(row['period'])}</strong>
                <a href="{html.escape(row['source_url'], quote=True)}" target="_blank" rel="noopener noreferrer">
                    Official release
                </a>
            </div>
        </article>
        """
        ).strip()
    )
st.markdown(f'<div class="macro-grid">{"".join(metric_markup)}</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="macro-section-head">
        <h2>Monthly signals</h2>
        <p>October 2025–September 2026</p>
    </div>
    """,
    unsafe_allow_html=True,
)

series_specs = {
    "Inflation": ("Canada CPI inflation", MACRO_COLORS[0], "12-month CPI change"),
    "Unemployment": ("Canada unemployment", MACRO_COLORS[1], "Seasonally adjusted rate"),
    "Policy rate": ("Bank of Canada policy rate", MACRO_COLORS[2], "Month-end overnight target"),
}
selected_series = st.radio("Monthly indicator", list(series_specs), horizontal=True, label_visibility="collapsed")
series_name, series_color, series_basis = series_specs[selected_series]
series_data = trends.loc[trends["indicator"].eq(series_name)].sort_values("period").copy()
series_data["date"] = pd.to_datetime(series_data["period"])
latest = series_data.iloc[-1]
previous = series_data.iloc[-2]
latest_period = pd.Period(latest["period"], freq="M").strftime("%b %Y")
previous_period = pd.Period(previous["period"], freq="M").strftime("%b %Y")
change = latest["value"] - previous["value"]
change_text = "No change" if abs(change) < 0.005 else f"{change:+.1f} percentage points"
precision = 2 if selected_series == "Policy rate" else 1

left, right = st.columns([2.4, 1], gap="large")
with left:
    figure = go.Figure(
        go.Scatter(
            x=series_data["date"],
            y=series_data["value"],
            mode="lines+markers",
            line={"color": series_color, "width": 3},
            marker={"color": series_color, "size": 7},
            hovertemplate=f"%{{x|%b %Y}}<br>%{{y:.{precision}f}}%<extra></extra>",
        )
    )
    figure.update_layout(
        height=350,
        margin={"l": 48, "r": 24, "t": 30, "b": 40},
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        showlegend=False,
        xaxis={"tickformat": "%b '%y", "dtick": "M2", "showgrid": False},
        yaxis={"ticksuffix": "%", "rangemode": "tozero" if selected_series == "Inflation" else "normal"},
    )
    st.plotly_chart(figure, width="stretch")
with right:
    st.markdown(
        f"""
        <div class="macro-reading" style="--series-accent: {html.escape(series_color, quote=True)}">
            <div class="macro-reading-label">Latest reading</div>
            <strong>{latest['value']:.{precision}f}%</strong>
            <p class="macro-period">{html.escape(latest_period)}</p>
            <p>{html.escape(series_basis)}</p>
            <p>{html.escape(change_text)} from {html.escape(previous_period)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if selected_series == "Inflation":
        st.caption("September CPI had not been released when this snapshot was checked.")

st.markdown(
    """
    <div class="macro-divider"></div>
    <div class="macro-section-head">
        <h2>GDP per person</h2>
        <p>Real growth from the previous quarter · Q1 2026</p>
    </div>
    <p class="macro-method">
        Canada, OECD and G7 use the same OECD measure and reference quarter.
        The Canada GDP card above reports total output for Q2 2026; these rows
        report output per person for Q1 2026.
    </p>
    """,
    unsafe_allow_html=True,
)

comparison = cards.loc[cards["indicator"].eq("Real GDP per capita")].set_index("region").loc[["Canada", "OECD", "G7"]]
comparison_figure = go.Figure(
    go.Bar(
        x=comparison["value"],
        y=comparison.index,
        orientation="h",
        marker_color=[MACRO_COLORS[0], MACRO_COLORS[1], MACRO_COLORS[2]],
        text=[f"+{value:.1f}%" for value in comparison["value"]],
        textposition="outside",
        hovertemplate="%{y}<br>%{x:.1f}% from prior quarter<extra></extra>",
    )
)
comparison_figure.update_layout(
    height=230,
    margin={"l": 76, "r": 70, "t": 18, "b": 38},
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    showlegend=False,
    xaxis={"range": [0, 0.5], "ticksuffix": "%", "dtick": 0.1, "showgrid": True},
    yaxis={"autorange": "reversed", "showgrid": False},
)
st.plotly_chart(comparison_figure, width="stretch")

with st.expander("Definitions, releases and data table"):
    st.markdown(
        """
        **Quarter-over-quarter** means growth from one quarter to the next; the GDP
        figures here are not annualized. **Year-over-year CPI** compares a month with
        the same month one year earlier. Reference periods differ because agencies
        publish on different schedules. This page is a static snapshot, verified on
        17 October 2026.

        Monthly history: [Statistics Canada CPI](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810000402),
        [Labour Force Survey](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410028701),
        and [Bank of Canada policy rate](https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rate/).
        """
    )
    source_table = cards[["region", "indicator", "value", "period", "released", "source_url"]].copy()
    source_table.columns = ["Region", "Indicator", "Value (%)", "Reference period", "Published", "Official release"]
    st.dataframe(
        source_table,
        column_config={"Official release": st.column_config.LinkColumn("Official release", display_text="Open source")},
        width="stretch",
        hide_index=True,
    )
