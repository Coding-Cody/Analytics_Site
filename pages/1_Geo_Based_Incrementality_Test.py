from __future__ import annotations

import numpy as np
import plotly.express as px
import streamlit as st

from utils.data import load_geo_test_data, load_synthetic_control_data
from utils.ui import inject_global_styles, render_insight


inject_global_styles()

st.markdown(
    """
    <section class="hero">
        <p class="eyebrow">Incrementality measurement | Geography-level experiment</p>
        <h1>Geo-based incrementality test for market-level media impact.</h1>
        <p class="hero-copy">
            A professional case study structure for estimating incremental lift when
            user-level randomization is not available. The page compares matched-market
            testing with a synthetic-control approach, including pre-period fit,
            difference-in-differences logic, treatment effect estimation, and uncertainty.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

methodology = st.segmented_control(
    "Methodology",
    ["Matched-market test", "Synthetic control"],
    default="Matched-market test",
)

market_df, group_df = load_geo_test_data()
synthetic_df = load_synthetic_control_data()

if methodology == "Matched-market test":
    st.subheader("Matched-market Test Design")
    left, right = st.columns([1.05, 0.95], gap="medium")
    with left:
        st.markdown(
            """
            <div class="section-band">
                <h3>Why matched markets?</h3>
                <p>
                    A one-market-vs-one-market comparison is fragile because market size,
                    baseline demand, seasonality, competitive intensity, and local media
                    consumption can differ materially. A matched-market design compares a
                    group of treated geographies with a group of statistically similar
                    controls, reducing idiosyncratic market noise and improving pre-period
                    fit before the test starts. Matching can use pre-period KPI trend,
                    media availability, population, seasonality, store footprint, and
                    category demand as covariates.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        test_markets = sorted(market_df.loc[market_df["group"] == "Test markets", "market"].unique())
        control_markets = sorted(
            market_df.loc[market_df["group"] == "Matched controls", "market"].unique()
        )
        st.markdown("**Test market group**")
        st.write(", ".join(test_markets))
        st.markdown("**Control market group**")
        st.write(", ".join(control_markets))

    test_post = group_df[(group_df["group"] == "Test markets") & (group_df["period"] == "Test period")][
        "kpi"
    ].mean()
    test_pre = group_df[(group_df["group"] == "Test markets") & (group_df["period"] == "Pre period")][
        "kpi"
    ].mean()
    control_post = group_df[
        (group_df["group"] == "Matched controls") & (group_df["period"] == "Test period")
    ]["kpi"].mean()
    control_pre = group_df[
        (group_df["group"] == "Matched controls") & (group_df["period"] == "Pre period")
    ]["kpi"].mean()
    did_lift = (test_post - test_pre) - (control_post - control_pre)
    lift_pct = did_lift / test_pre
    residual_sigma = (
        group_df.pivot(index="week", columns="group", values="kpi")
        .assign(gap=lambda x: x["Test markets"] - x["Matched controls"])["gap"]
        .std(ddof=1)
    )
    standard_error = residual_sigma / np.sqrt(12)
    t_stat = did_lift / standard_error

    metric_cols = st.columns(4)
    metric_cols[0].metric("Pre-period fit", "2.8% gap")
    metric_cols[1].metric("Difference-in-differences lift", f"{did_lift:,.0f}")
    metric_cols[2].metric("Lift rate", f"{lift_pct:.1%}")
    metric_cols[3].metric("t-statistic", f"{t_stat:.2f}")

    st.markdown(
        """
        <div class="method-note">
            <strong>Statistical read:</strong> the estimand is the average treatment
            effect on treated geographies. In compact form:
            (Test post - Test pre) - (Control post - Control pre). The matched control
            group is preferred over one market vs one market because averaging across
            several comparable FSAs reduces local shocks and improves estimator stability.
        </div>
        """,
        unsafe_allow_html=True,
    )

    fig = px.line(
        group_df,
        x="week",
        y="kpi",
        color="group",
        markers=True,
        title="Average KPI Trend: Test Markets vs Matched Controls",
        labels={"week": "Week", "kpi": "KPI index", "group": "Market group"},
        color_discrete_map={"Test markets": "#2563eb", "Matched controls": "#0f766e"},
    )
    fig.add_vline(x=group_df[group_df["period"] == "Test period"]["week"].min(), line_dash="dash")
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, width="stretch")
    render_insight(
        "The pre-period validates comparability before media activation. The post-period gap is interpreted through a difference-in-differences lens, not a simple before/after read."
    )

    market_fig = px.box(
        market_df,
        x="group",
        y="kpi",
        color="period",
        points="all",
        title="Market-level Distribution by Period",
        labels={"group": "Group", "kpi": "KPI index", "period": "Period"},
        color_discrete_map={"Pre period": "#94a3b8", "Test period": "#2563eb"},
    )
    st.plotly_chart(market_fig, width="stretch")
    render_insight(
        "Looking at the market-level distribution helps confirm that the estimate is not being driven by only one geography."
    )

else:
    st.subheader("Synthetic-control Case Study")
    st.markdown(
        """
        <div class="section-band">
            <h3>Why synthetic control?</h3>
            <p>
                Synthetic control constructs a weighted comparison unit from multiple
                untreated geographies. Instead of choosing a single control market, the
                method optimizes the pre-period match to the treated geography and then
                uses the post-period divergence as the estimated incremental effect.
                In practice, weights are selected to minimize pre-period prediction error,
                often with non-negative weights that sum to one.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    wide = synthetic_df.pivot(index="week", columns="series", values="kpi").reset_index()
    wide["incremental_lift"] = wide["Treated geography"] - wide["Synthetic control"]
    post_lift = wide.loc[wide["week"] >= wide["week"].iloc[12], "incremental_lift"]
    pre_gap = wide.loc[wide["week"] < wide["week"].iloc[12], "incremental_lift"]
    ci = 1.96 * post_lift.std(ddof=1) / np.sqrt(len(post_lift))

    metric_cols = st.columns(4)
    metric_cols[0].metric("Pre-period avg gap", f"{pre_gap.mean():.1f}")
    metric_cols[1].metric("Post-period avg lift", f"{post_lift.mean():.1f}")
    metric_cols[2].metric("Approx. 95% CI", f"+/- {ci:.1f}")
    metric_cols[3].metric("Pre-period RMSE", f"{np.sqrt(np.mean(pre_gap**2)):.1f}")

    st.markdown(
        """
        <div class="method-note">
            <strong>Synthetic-control read:</strong> evaluate the pre-period fit first.
            A low pre-period RMSE means the counterfactual tracks the treated geography
            before media launch. The post-period gap is then interpreted as a treatment
            effect, with placebo tests or market-level permutation checks used in a full
            production analysis.
        </div>
        """,
        unsafe_allow_html=True,
    )

    fig = px.line(
        synthetic_df,
        x="week",
        y="kpi",
        color="series",
        markers=True,
        title="Treated Geography vs Synthetic Control",
        labels={"week": "Week", "kpi": "KPI index", "series": "Series"},
        color_discrete_map={"Treated geography": "#2563eb", "Synthetic control": "#0f766e"},
    )
    fig.add_vline(x=wide["week"].iloc[12], line_dash="dash")
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, width="stretch")
    render_insight(
        "The synthetic control follows the treated geography closely before launch. A sustained post-launch divergence supports a stronger causal read than a raw trend chart."
    )

    lift_fig = px.bar(
        wide,
        x="week",
        y="incremental_lift",
        title="Estimated Incremental Lift Over Time",
        labels={"week": "Week", "incremental_lift": "Treated minus synthetic control"},
    )
    lift_fig.update_traces(marker_color="#be185d")
    st.plotly_chart(lift_fig, width="stretch")
    render_insight(
        "This view converts the test into a week-by-week treatment effect and makes it easier to separate launch noise from sustained incremental impact."
    )

