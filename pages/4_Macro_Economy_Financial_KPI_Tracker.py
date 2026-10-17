from __future__ import annotations

import html
import importlib
from textwrap import dedent

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from utils import data as macro_data
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
            color: __LINK__;
            text-decoration: underline;
            text-underline-offset: 2px;
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
        .macro-lens-stats {
            display: flex;
            flex-wrap: wrap;
            gap: 1.6rem;
            margin: 0.8rem 0 0.3rem;
        }
        .macro-lens-stat {
            border-left: 3px solid var(--lens-accent);
            padding-left: 0.8rem;
            min-width: 9rem;
        }
        .macro-lens-stat span, .macro-lens-stat small {
            display: block;
            color: __MUTED__;
            font-size: 0.76rem;
        }
        .macro-lens-stat strong {
            display: block;
            color: __INK__;
            font-size: 1.9rem;
            line-height: 1.15;
            margin: 0.15rem 0;
        }
        .macro-source-note {
            color: __MUTED__;
            font-size: 0.78rem;
            line-height: 1.45;
            margin: 0.15rem 0 0.6rem;
        }
        .macro-source-note a { color: __LINK__; }
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
        }
    </style>
    """
    .replace("__DEEP__", THEME["deep"])
    .replace("__ACCENT__", THEME["accent"])
    .replace("__MUTED__", THEME["muted"])
    .replace("__INK__", THEME["ink"])
    .replace("__LINK__", THEME["status_text"])
    .replace("__LINE__", THEME["line"]),
    unsafe_allow_html=True,
)

cards, trends = macro_data.load_macro_kpi_data()
has_current_schema = {"released", "source_url"}.issubset(cards.columns) and (
    (cards["region"].eq("Canada") & cards["indicator"].eq("Real GDP per capita")).any()
)
if not hasattr(macro_data, "load_inflation_energy_data") or not has_current_schema:
    # Streamlit can retain an imported data module during a repository update.
    cards, trends = importlib.reload(macro_data).load_macro_kpi_data()
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
        <p>October 2025–September 2026 · independent scales</p>
    </div>
    """,
    unsafe_allow_html=True,
)

signal_specs = (
    ("CPI inflation", "Canada CPI inflation", MACRO_COLORS[0], 1, [1.5, 3.5], [2.0, 3.0]),
    ("Unemployment", "Canada unemployment", MACRO_COLORS[1], 1, [6.0, 7.2], [6.0, 6.5, 7.0]),
    ("Policy rate", "Bank of Canada policy rate", MACRO_COLORS[2], 2, [1.75, 2.75], [2.0, 2.5]),
)
signal_figure = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.13)
for row_number, (label, indicator, color, precision, y_range, y_ticks) in enumerate(signal_specs, start=1):
    observations = trends.loc[trends["indicator"].eq(indicator)].sort_values("period")
    dates = pd.to_datetime(observations["period"])
    latest = observations.iloc[-1]
    latest_period = pd.Period(latest["period"], freq="M").strftime("%b")
    signal_figure.add_trace(
        go.Scatter(
            x=dates,
            y=observations["value"],
            name=label,
            mode="lines+markers" if row_number < 3 else "lines",
            line={"color": color, "width": 3, "shape": "hv" if row_number == 3 else "linear"},
            marker={"color": color, "size": 7},
            hovertemplate=f"%{{x|%b %Y}}<br>{label}: %{{y:.{precision}f}}%<extra></extra>",
        ),
        row=row_number,
        col=1,
    )
    signal_figure.update_yaxes(
        range=y_range,
        tickvals=y_ticks,
        ticktext=[f"{value:g}%" for value in y_ticks],
        showgrid=True,
        gridcolor=THEME["grid"],
        zeroline=False,
        fixedrange=True,
        row=row_number,
        col=1,
    )
    axis_name = "yaxis" if row_number == 1 else f"yaxis{row_number}"
    label_y = signal_figure.layout[axis_name].domain[1] + 0.012
    signal_figure.add_annotation(
        x=0,
        y=label_y,
        xref="paper",
        yref="paper",
        text=f"<b>{label}</b>",
        showarrow=False,
        xanchor="left",
        yanchor="bottom",
        font={"color": color, "size": 13},
    )
    signal_figure.add_annotation(
        x=1,
        y=label_y,
        xref="paper",
        yref="paper",
        text=f"<b>{latest['value']:.{precision}f}%</b> · {latest_period}",
        showarrow=False,
        xanchor="right",
        yanchor="bottom",
        font={"color": THEME["ink"], "size": 12},
    )

signal_figure.update_layout(
    height=505,
    margin={"l": 58, "r": 30, "t": 40, "b": 45},
    paper_bgcolor=THEME["paper_bg"],
    plot_bgcolor=THEME["plot_bg"],
    showlegend=False,
    hovermode="x unified",
    font={"color": THEME["muted"]},
)
signal_figure.update_xaxes(showgrid=False, fixedrange=True, range=["2025-10-01", "2026-09-20"])
signal_figure.update_xaxes(tickformat="%b '%y", dtick="M2", showticklabels=True, row=3, col=1)
st.plotly_chart(signal_figure, width="stretch")
st.caption(
    "CPI ends in August; September CPI was not yet published at the 17 Oct 2026 snapshot. "
    "Unemployment and the policy-rate series run through September. Each lane uses its own percentage scale; "
    "the policy rate stayed at 2.25% throughout the period shown."
)

st.markdown(
    """
    <div class="macro-divider"></div>
    <div class="macro-section-head">
        <h2>Inflation and energy</h2>
        <p>Two release schedules, two different units</p>
    </div>
    <p class="macro-method">
        The CPI detail shows Canadian consumer-price changes. The oil series tracks a
        US-dollar crude benchmark and is market context, not a Canadian gasoline price
        or a CPI forecast.
    </p>
    """,
    unsafe_allow_html=True,
)

cpi_detail, wti = macro_data.load_inflation_energy_data()
cpi_lookup = cpi_detail.set_index("measure")
wti = wti.sort_values("week_end").copy()
wti["date"] = pd.to_datetime(wti["week_end"])
latest_wti = wti.iloc[-1]
previous_wti = wti.iloc[-2]
wti_change = latest_wti["value"] - previous_wti["value"]
wti_period = f"{latest_wti['date']:%b} {latest_wti['date'].day}, {latest_wti['date']:%Y}"

cpi_col, oil_col = st.columns([1, 1], gap="large")
with cpi_col:
    st.markdown("**Canadian CPI** · August 2026 · 12-month change")
    st.markdown(
        dedent(
            f"""
            <div class="macro-lens-stats">
                <div class="macro-lens-stat" style="--lens-accent: {MACRO_COLORS[0]}">
                    <span>ALL ITEMS</span><strong>{cpi_lookup.loc['All-items CPI', 'value']:.1f}%</strong>
                    <small>Headline inflation</small>
                </div>
                <div class="macro-lens-stat" style="--lens-accent: {MACRO_COLORS[1]}">
                    <span>EXCLUDING GASOLINE</span>
                    <strong>{cpi_lookup.loc['CPI excluding gasoline', 'value']:.1f}%</strong>
                    <small>Recalculated aggregate</small>
                </div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )
    component_names = ["Food purchased from stores", "Shelter", "Transportation", "Gasoline"]
    components = cpi_lookup.loc[component_names]
    component_figure = go.Figure(
        go.Bar(
            x=components["value"],
            y=["Groceries", "Shelter", "Transport", "Gasoline"],
            customdata=component_names,
            orientation="h",
            marker_color=[MACRO_COLORS[1], MACRO_COLORS[0], MACRO_COLORS[3], MACRO_COLORS[2]],
            text=[f"{value:.1f}%" for value in components["value"]],
            textposition="outside",
            hovertemplate="%{customdata}<br>%{x:.1f}% over 12 months<extra></extra>",
        )
    )
    component_figure.update_layout(
        height=270,
        margin={"l": 90, "r": 42, "t": 12, "b": 38},
        paper_bgcolor=THEME["paper_bg"],
        plot_bgcolor=THEME["plot_bg"],
        showlegend=False,
        xaxis={"range": [0, 26], "ticksuffix": "%", "dtick": 5, "showgrid": True},
        yaxis={"autorange": "reversed", "showgrid": False},
    )
    st.plotly_chart(component_figure, width="stretch")
    st.markdown(
        f'<p class="macro-source-note">Source: <a href="{html.escape(cpi_detail.iloc[0]["source_url"], quote=True)}" '
        'target="_blank" rel="noopener noreferrer">Statistics Canada, August CPI</a> (released 14 Sep 2026). '
        "Category rates are not contributions to headline CPI.</p>",
        unsafe_allow_html=True,
    )

with oil_col:
    st.markdown("**WTI crude oil** · Cushing spot · weekly average")
    st.markdown(
        dedent(
            f"""
            <div class="macro-lens-stats">
                <div class="macro-lens-stat" style="--lens-accent: {THEME['gold']}">
                    <span>WEEK ENDING {html.escape(wti_period.upper())}</span>
                    <strong>${latest_wti['value']:.2f}</strong>
                    <small>USD per barrel · {wti_change:+.2f} from prior week</small>
                </div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )
    oil_figure = go.Figure(
        go.Scatter(
            x=wti["date"],
            y=wti["value"],
            mode="lines+markers",
            line={"color": THEME["gold"], "width": 3},
            marker={"color": THEME["gold"], "size": 7},
            hovertemplate="Week ending %{x|%d %b %Y}<br>$%{y:.2f} per barrel<extra></extra>",
        )
    )
    oil_figure.update_layout(
        height=270,
        margin={"l": 52, "r": 22, "t": 12, "b": 38},
        paper_bgcolor=THEME["paper_bg"],
        plot_bgcolor=THEME["plot_bg"],
        showlegend=False,
        xaxis={"tickformat": "%b %d", "dtick": "M1", "showgrid": False},
        yaxis={"tickprefix": "$", "range": [wti["value"].min() - 5, wti["value"].max() + 5], "showgrid": True},
    )
    st.plotly_chart(oil_figure, width="stretch")
    st.markdown(
        f'<p class="macro-source-note">Source: <a href="{html.escape(latest_wti["source_url"], quote=True)}" '
        'target="_blank" rel="noopener noreferrer">US EIA weekly WTI spot series</a> (released 15 Oct 2026). '
        "US benchmark; not a Canadian pump price.</p>",
        unsafe_allow_html=True,
    )

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
        The CPI component view uses the August 2026 release. WTI is the US EIA weekly
        Cushing spot average, in US dollars per barrel, through the week ending
        9 October 2026; it is not a Canadian retail fuel-price measure.
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
