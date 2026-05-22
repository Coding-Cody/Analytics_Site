from __future__ import annotations

import plotly.express as px
import streamlit as st

from utils.data import CHANNELS, load_mmm_case_data, load_response_curve_data, summarize_channels
from utils.ui import inject_global_styles, render_insight, render_kpi_card


inject_global_styles()

st.markdown(
    """
    <section class="hero">
        <p class="eyebrow">Marketing science | Google Meridian workflow</p>
        <h1>Marketing Mix Modelling with ad-stock, saturation, and response curves.</h1>
        <p class="hero-copy">
            A deeper MMM case-study page that presents Bayesian hierarchical modeling
            concepts, Meridian-style media transformations, ad-stock memory, Hill-function
            saturation, contribution decomposition, posterior uncertainty, and planning
            decisions in an executive-ready format.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

df = load_mmm_case_data()
curve_df = load_response_curve_data()
all_channels = list(CHANNELS.keys())

with st.sidebar:
    st.header("MMM Controls")
    selected_channels = st.multiselect(
        "Channels",
        all_channels,
        default=all_channels,
    )
    min_date = df["week"].min().date()
    max_date = df["week"].max().date()
    date_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    budget_change = st.slider(
        "Budget scenario",
        min_value=-30,
        max_value=30,
        value=10,
        step=5,
        help="Applies a planning scenario to selected-channel spend using current response assumptions.",
    )

if not selected_channels:
    st.info("Select at least one channel to view the MMM case study.")
    st.stop()

start_date, end_date = date_range if len(date_range) == 2 else (min_date, max_date)
filtered = df[
    (df["channel"].isin(selected_channels))
    & (df["week"].dt.date >= start_date)
    & (df["week"].dt.date <= end_date)
].copy()
filtered_curves = curve_df[curve_df["channel"].isin(selected_channels)]

summary = summarize_channels(filtered)
weekly_kpi = (
    filtered.groupby("week", as_index=False)
    .agg(
        spend=("spend", "sum"),
        adstocked_spend=("adstocked_spend", "sum"),
        contribution=("contribution", "sum"),
        kpi_sales=("kpi_sales", "first"),
    )
    .sort_values("week")
)

st.subheader("Business Problem")
left, right = st.columns(2, gap="small")
with left:
    st.markdown(
        """
        <div class="section-band paired-card">
            <h3>Decision context</h3>
            <p>
                The core planning question is how much incremental outcome each channel
                contributes after accounting for baseline demand, carryover effects,
                diminishing returns, seasonality, and different roles across the funnel.
                A strong MMM read separates spend volume from true response quality and
                makes uncertainty explicit before budget recommendations are made.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        """
        <div class="section-band paired-card">
            <h3>How Meridian fits</h3>
            <p>
                Google Meridian supports Bayesian MMM workflows with media transformations,
                prior-informed modeling, contribution decomposition, uncertainty, and
                optimization. A typical model uses hierarchical priors to partially pool
                channel effects, improves stability across sparse channels, and returns
                posterior distributions rather than single-point estimates.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

metric_cols = st.columns(4)
with metric_cols[0]:
    render_kpi_card("Selected spend", f"${filtered['spend'].sum():,.0f}", "Filtered media investment")
with metric_cols[1]:
    render_kpi_card(
        "Estimated contribution",
        f"${filtered['contribution'].sum():,.0f}",
        "Model-attributed KPI impact",
    )
with metric_cols[2]:
    render_kpi_card("Average ROI", f"{summary['roi'].mean():.2f}x", "Mean channel efficiency")
with metric_cols[3]:
    render_kpi_card("Mean half-life", f"{summary['half_life'].mean():.1f} weeks", "Carryover duration")

st.markdown(
    """
    <div class="method-note">
        <strong>Model structure:</strong> KPI is decomposed into baseline, seasonality,
        controls, and transformed media. Media spend is first passed through an ad-stock
        function to represent carryover, then through a Hill saturation function:
        response = x^alpha / (x^alpha + ec50^alpha). The alpha parameter controls curve
        steepness; ec50 is the spend level where the channel reaches half of maximum
        response. Bayesian hierarchical priors stabilize channel coefficients and produce
        posterior intervals for contribution and ROI.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

spend_fig = px.area(
    filtered,
    x="week",
    y="spend",
    color="channel",
    color_discrete_map={channel: details["color"] for channel, details in CHANNELS.items()},
    title="Media Spend Over Time by Channel",
    labels={"week": "Week", "spend": "Spend", "channel": "Channel"},
)
spend_fig.update_layout(hovermode="x unified", legend_title_text="Channel")
st.plotly_chart(spend_fig, width="stretch")
render_insight(
    "Spend pacing is the operational input. MMM interpretation begins after spend is transformed into ad-stocked media pressure and then mapped through a nonlinear Hill response curve."
)

kpi_fig = px.line(
    weekly_kpi,
    x="week",
    y=["kpi_sales", "contribution"],
    markers=True,
    title="KPI and Estimated Media Contribution Over Time",
    labels={"week": "Week", "value": "KPI / contribution", "variable": "Series"},
)
kpi_fig.update_layout(hovermode="x unified")
st.plotly_chart(kpi_fig, width="stretch")
render_insight(
    "The KPI view combines baseline demand and media-driven contribution. A useful MMM read asks whether posterior contribution moves plausibly with transformed media pressure, not raw spend alone."
)

left_chart, right_chart = st.columns(2, gap="medium")
with left_chart:
    contribution_fig = px.bar(
        summary,
        x="channel",
        y="contribution",
        color="channel",
        color_discrete_map={channel: details["color"] for channel, details in CHANNELS.items()},
        title="Channel Contribution",
        labels={"channel": "Channel", "contribution": "Estimated Contribution"},
        text_auto=".2s",
    )
    contribution_fig.update_layout(showlegend=False)
    st.plotly_chart(contribution_fig, width="stretch")
    render_insight(
        "Contribution ranks channels by estimated business impact after transformation, baseline adjustment, Bayesian shrinkage, and response modeling."
    )

with right_chart:
    roi_fig = px.bar(
        summary.sort_values("roi", ascending=False),
        x="channel",
        y="roi",
        color="channel",
        color_discrete_map={channel: details["color"] for channel, details in CHANNELS.items()},
        title="ROI / Effectiveness Comparison",
        labels={"channel": "Channel", "roi": "Average ROI"},
        text_auto=".2f",
    )
    roi_fig.update_layout(showlegend=False)
    st.plotly_chart(roi_fig, width="stretch")
    render_insight(
        "High ROI does not always mean higher budget. Saturation, scale, confidence, and business constraints determine the next dollar."
    )

st.divider()
st.subheader("Ad-stock and Saturation Diagnostics")

diagnostic_cols = st.columns(3)
with diagnostic_cols[0]:
    render_kpi_card("Ad-stock parameter", "Half-life", "Channel-specific memory")
with diagnostic_cols[1]:
    render_kpi_card("Hill alpha", "1.00-1.35", "Response curve steepness")
with diagnostic_cols[2]:
    render_kpi_card("Hill ec50", "$52K-$145K", "Half-maximum response")

adstock_fig = px.line(
    filtered,
    x="week",
    y="adstocked_spend",
    color="channel",
    color_discrete_map={channel: details["color"] for channel, details in CHANNELS.items()},
    title="Ad-stocked Media Pressure",
    labels={"week": "Week", "adstocked_spend": "Ad-stocked spend", "channel": "Channel"},
)
adstock_fig.update_layout(hovermode="x unified")
st.plotly_chart(adstock_fig, width="stretch")
render_insight(
    "Ad-stock captures memory: TV and YouTube retain influence longer, while search decays faster. This prevents the model from forcing all media impact into the week spend occurred."
)

curve_col, marginal_col = st.columns(2, gap="medium")
with curve_col:
    curve_fig = px.line(
        filtered_curves,
        x="weekly_spend",
        y="expected_contribution",
        color="channel",
        color_discrete_map={channel: details["color"] for channel, details in CHANNELS.items()},
        title="Saturation Curves",
        labels={
            "weekly_spend": "Weekly spend",
            "expected_contribution": "Expected contribution",
            "channel": "Channel",
        },
    )
    st.plotly_chart(curve_fig, width="stretch")
    render_insight(
        "Saturation curves show diminishing returns. The Hill function makes this explicit: alpha controls steepness and ec50 controls how quickly the channel reaches half of its maximum response."
    )

with marginal_col:
    marginal_fig = px.line(
        filtered_curves,
        x="weekly_spend",
        y="marginal_return",
        color="channel",
        color_discrete_map={channel: details["color"] for channel, details in CHANNELS.items()},
        title="Marginal Return by Spend Level",
        labels={"weekly_spend": "Weekly spend", "marginal_return": "Marginal return"},
    )
    st.plotly_chart(marginal_fig, width="stretch")
    render_insight(
        "Marginal return is the planning layer: channels with high average ROI may still be poor candidates for incremental budget if their posterior response curve is already near saturation."
    )

st.divider()
st.subheader("Budget Planning Scenario")

scenario = summary.copy()
scenario["current_spend"] = scenario["spend"]
scenario["scenario_spend"] = scenario["current_spend"] * (1 + budget_change / 100)
scenario["incremental_spend"] = scenario["scenario_spend"] - scenario["current_spend"]
scenario["estimated_incremental_contribution"] = scenario["incremental_spend"] * scenario["roi"]

scenario_cols = st.columns(3)
with scenario_cols[0]:
    render_kpi_card("Scenario spend", f"${scenario['scenario_spend'].sum():,.0f}", f"{budget_change:+d}% vs current")
with scenario_cols[1]:
    render_kpi_card(
        "Incremental contribution",
        f"${scenario['estimated_incremental_contribution'].sum():,.0f}",
        "Scenario-level estimate",
    )
with scenario_cols[2]:
    render_kpi_card("Channels evaluated", f"{len(scenario)}", "Selected media channels")

scenario_fig = px.bar(
    scenario.sort_values("estimated_incremental_contribution", ascending=False),
    x="channel",
    y="estimated_incremental_contribution",
    color="channel",
    color_discrete_map={channel: details["color"] for channel, details in CHANNELS.items()},
    title=f"Estimated Contribution from a {budget_change:+d}% Selected-channel Budget Scenario",
    labels={"channel": "Channel", "estimated_incremental_contribution": "Incremental contribution"},
)
scenario_fig.update_layout(showlegend=False)
st.plotly_chart(scenario_fig, width="stretch")
render_insight(
    "A production optimizer would apply constraints, uncertainty intervals, minimum spend thresholds, and saturation-aware response functions before final recommendation."
)

with st.expander("Channel model summary"):
    st.dataframe(
        summary[
            [
                "channel",
                "spend",
                "contribution",
                "roi",
                "half_life",
                "ec50",
                "share_of_contribution",
                "response_note",
            ]
        ].style.format(
            {
                "spend": "${:,.0f}",
                "contribution": "${:,.0f}",
                "roi": "{:.2f}x",
                "half_life": "{:.1f}",
                "ec50": "${:,.0f}",
                "share_of_contribution": "{:.1%}",
            }
        ),
        width="stretch",
        hide_index=True,
    )

