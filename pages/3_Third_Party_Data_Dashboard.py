from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data import load_sales_dashboard_data
from utils.theme import CHANNEL_COLORS, SALES_COLORS, THEME
from utils.ui import inject_global_styles, render_insight, render_kpi_card


inject_global_styles()


def money_short(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"


def delta_text(current: float, prior: float, suffix: str = "") -> str:
    if prior == 0 or pd.isna(prior):
        return "No prior baseline"
    change = (current - prior) / prior
    return f"{change:+.1%} vs prior period{suffix}"


def summarize(data: pd.DataFrame) -> dict[str, float]:
    revenue = data["revenue"].sum()
    margin = data["gross_margin"].sum()
    orders = data["orders"].sum()
    sessions = data["sessions"].sum()
    return {
        "revenue": revenue,
        "gross_margin": margin,
        "margin_rate": margin / revenue if revenue else 0,
        "orders": orders,
        "aov": revenue / orders if orders else 0,
        "conversion_rate": orders / sessions if sessions else 0,
        "units": data["units"].sum(),
        "discount_rate": (data["revenue"] * data["discount_rate"]).sum() / revenue if revenue else 0,
    }


def filter_sales(
    data: pd.DataFrame,
    start: pd.Timestamp,
    end: pd.Timestamp,
    regions: list[str],
    channels: list[str],
    categories: list[str],
    segments: list[str],
) -> pd.DataFrame:
    return data[
        (data["date"].between(start, end))
        & (data["region"].isin(regions))
        & (data["channel"].isin(channels))
        & (data["category"].isin(categories))
        & (data["customer_segment"].isin(segments))
    ].copy()


@st.cache_data(show_spinner=False)
def get_sales_data() -> pd.DataFrame:
    return load_sales_dashboard_data()


st.markdown(
    """
    <section class="hero">
        <p class="eyebrow">Retail sales analytics | Executive dashboard</p>
        <h1>Sales performance dashboard for revenue, margin, channel mix, and product action.</h1>
        <p class="hero-copy">
            A polished sales analytics workspace for tracking commercial performance:
            revenue quality, gross margin, conversion, channel contribution, product
            momentum, regional mix, customer segment behavior, and operating follow-up.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

sales = get_sales_data()

with st.sidebar:
    st.header("Sales Dashboard Controls")
    min_date = sales["date"].min().date()
    max_date = sales["date"].max().date()
    date_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    selected_regions = st.multiselect(
        "Regions",
        sorted(sales["region"].unique()),
        default=sorted(sales["region"].unique()),
    )
    selected_channels = st.multiselect(
        "Channels",
        sorted(sales["channel"].unique()),
        default=sorted(sales["channel"].unique()),
    )
    selected_categories = st.multiselect(
        "Categories",
        sorted(sales["category"].unique()),
        default=sorted(sales["category"].unique()),
    )
    selected_segments = st.multiselect(
        "Customer segments",
        sorted(sales["customer_segment"].unique()),
        default=sorted(sales["customer_segment"].unique()),
    )

start_date, end_date = date_range if len(date_range) == 2 else (min_date, max_date)
start_ts = pd.Timestamp(start_date)
end_ts = pd.Timestamp(end_date)

if not selected_regions or not selected_channels or not selected_categories or not selected_segments:
    st.info("Select at least one value in each filter to render the sales dashboard.")
    st.stop()

filtered = filter_sales(
    sales,
    start_ts,
    end_ts,
    selected_regions,
    selected_channels,
    selected_categories,
    selected_segments,
)
period_days = max((end_ts - start_ts).days + 1, 1)
prior_end = start_ts - pd.Timedelta(days=1)
prior_start = prior_end - pd.Timedelta(days=period_days - 1)
prior = filter_sales(
    sales,
    prior_start,
    prior_end,
    selected_regions,
    selected_channels,
    selected_categories,
    selected_segments,
)

if filtered.empty:
    st.info("The selected filters return no sales rows.")
    st.stop()

current_summary = summarize(filtered)
prior_summary = summarize(prior) if not prior.empty else {key: 0 for key in current_summary}

st.subheader("1. Executive KPI Snapshot")
kpi_cols = st.columns(6)
with kpi_cols[0]:
    render_kpi_card("Net revenue", money_short(current_summary["revenue"]), delta_text(current_summary["revenue"], prior_summary["revenue"]))
with kpi_cols[1]:
    render_kpi_card("Gross margin", f"{current_summary['margin_rate']:.1%}", delta_text(current_summary["margin_rate"], prior_summary["margin_rate"]))
with kpi_cols[2]:
    render_kpi_card("Orders", f"{current_summary['orders']:,.0f}", delta_text(current_summary["orders"], prior_summary["orders"]))
with kpi_cols[3]:
    render_kpi_card("AOV", money_short(current_summary["aov"]), delta_text(current_summary["aov"], prior_summary["aov"]))
with kpi_cols[4]:
    render_kpi_card("Conversion", f"{current_summary['conversion_rate']:.2%}", delta_text(current_summary["conversion_rate"], prior_summary["conversion_rate"]))
with kpi_cols[5]:
    render_kpi_card("Discount rate", f"{current_summary['discount_rate']:.1%}", delta_text(current_summary["discount_rate"], prior_summary["discount_rate"]))

render_insight(
    "The top line is separated from revenue quality. A strong dashboard should read revenue, margin, conversion, discounting, and order volume together rather than treating sales growth as automatically healthy."
)

st.subheader("2. Weekly Revenue and Margin Trend")
weekly = (
    filtered.groupby("week", as_index=False)
    .agg(revenue=("revenue", "sum"), gross_margin=("gross_margin", "sum"), orders=("orders", "sum"), sessions=("sessions", "sum"))
    .sort_values("week")
)
weekly["gross_margin_rate"] = weekly["gross_margin"] / weekly["revenue"]
weekly_long = weekly.melt(
    id_vars="week",
    value_vars=["revenue", "gross_margin"],
    var_name="Metric",
    value_name="Value",
)
trend_fig = px.line(
    weekly_long,
    x="week",
    y="Value",
    color="Metric",
    markers=True,
    title="Weekly Revenue and Gross Margin",
    labels={"week": "Week", "Value": "Value"},
    color_discrete_map={"revenue": THEME["accent"], "gross_margin": THEME["gold"]},
)
trend_fig.update_layout(hovermode="x unified")
trend_fig.update_traces(line_width=2.6, marker_size=5)
st.plotly_chart(trend_fig, width="stretch")

st.subheader("3. Channel Contribution")
channel_summary = (
    filtered.groupby("channel", as_index=False)
    .agg(revenue=("revenue", "sum"), gross_margin=("gross_margin", "sum"), orders=("orders", "sum"), sessions=("sessions", "sum"))
)
channel_summary["margin_rate"] = channel_summary["gross_margin"] / channel_summary["revenue"]
channel_summary["conversion_rate"] = channel_summary["orders"] / channel_summary["sessions"]

left_chart, right_chart = st.columns(2, gap="medium")
with left_chart:
    channel_fig = px.bar(
        channel_summary.sort_values("revenue", ascending=False),
        x="channel",
        y="revenue",
        color="channel",
        color_discrete_map=SALES_COLORS,
        text_auto=".2s",
        title="Revenue by Channel",
        labels={"channel": "Channel", "revenue": "Revenue"},
    )
    channel_fig.update_layout(showlegend=False)
    channel_fig.update_traces(marker_line_width=0, opacity=0.88, textfont_color=THEME["bar_text"])
    st.plotly_chart(channel_fig, width="stretch")
with right_chart:
    conversion_fig = px.scatter(
        channel_summary,
        x="conversion_rate",
        y="margin_rate",
        size="revenue",
        color="channel",
        color_discrete_map=SALES_COLORS,
        title="Channel Quality: Conversion vs Margin",
        labels={"conversion_rate": "Conversion rate", "margin_rate": "Gross margin rate"},
        hover_data={"revenue": ":$,.0f", "orders": ":,.0f"},
    )
    conversion_fig.update_layout(xaxis_tickformat=".1%", yaxis_tickformat=".1%")
    conversion_fig.update_traces(marker={"opacity": 0.78, "line": {"width": 0}})
    st.plotly_chart(conversion_fig, width="stretch")

st.subheader("4. Category and Product Performance")
category = (
    filtered.groupby(["category", "channel"], as_index=False)
    .agg(revenue=("revenue", "sum"), gross_margin=("gross_margin", "sum"), orders=("orders", "sum"))
)
category_fig = px.bar(
    category,
    x="category",
    y="revenue",
    color="channel",
    color_discrete_map=SALES_COLORS,
    title="Category Revenue by Channel",
    labels={"category": "Category", "revenue": "Revenue", "channel": "Channel"},
)
category_fig.update_layout(barmode="stack", legend={"orientation": "h", "y": 1.12, "x": 1, "xanchor": "right"})
category_fig.update_xaxes(tickangle=-15)
st.plotly_chart(category_fig, width="stretch")

product = (
    filtered.groupby(["product", "category"], as_index=False)
    .agg(revenue=("revenue", "sum"), gross_margin=("gross_margin", "sum"), orders=("orders", "sum"), units=("units", "sum"))
)
product["margin_rate"] = product["gross_margin"] / product["revenue"]
top_products = product.sort_values("revenue", ascending=False).head(12)
product_fig = px.bar(
    top_products.sort_values("revenue"),
    x="revenue",
    y="product",
    color="category",
    color_discrete_sequence=list(CHANNEL_COLORS.values()),
    orientation="h",
    title="Top Products by Revenue",
    labels={"revenue": "Revenue", "product": "Product", "category": "Category"},
    hover_data={"gross_margin": ":$,.0f", "margin_rate": ":.1%", "orders": ":,.0f"},
)
product_fig.update_layout(legend={"orientation": "h", "y": 1.12, "x": 1, "xanchor": "right"}, margin={"l": 120})
st.plotly_chart(product_fig, width="stretch")
render_insight(
    "Product analysis separates high-volume products from high-quality products. The next action is not always more inventory; it may be pricing, channel mix, styling bundles, or discount discipline."
)

st.subheader("5. Regional Performance")
region = (
    filtered.groupby("region", as_index=False)
    .agg(revenue=("revenue", "sum"), gross_margin=("gross_margin", "sum"), orders=("orders", "sum"), sessions=("sessions", "sum"))
)
region["margin_rate"] = region["gross_margin"] / region["revenue"]
region["conversion_rate"] = region["orders"] / region["sessions"]
region_fig = px.scatter(
    region,
    x="revenue",
    y="margin_rate",
    size="orders",
    color="region",
    color_discrete_sequence=list(CHANNEL_COLORS.values()),
    title="Regional Revenue, Margin, and Order Scale",
    labels={"revenue": "Revenue", "margin_rate": "Gross margin rate"},
    hover_data={"orders": ":,.0f", "conversion_rate": ":.2%"},
)
region_fig.update_layout(yaxis_tickformat=".1%")
region_fig.update_traces(marker={"opacity": 0.80, "line": {"width": 0}})
st.plotly_chart(region_fig, width="stretch")

st.subheader("6. Customer Segment Mix")
segment = (
    filtered.groupby(["customer_segment", "channel"], as_index=False)
    .agg(revenue=("revenue", "sum"), gross_margin=("gross_margin", "sum"), orders=("orders", "sum"))
)
segment["margin_rate"] = segment["gross_margin"] / segment["revenue"]
segment_fig = px.bar(
    segment,
    x="customer_segment",
    y="revenue",
    color="channel",
    color_discrete_map=SALES_COLORS,
    title="Revenue by Customer Segment and Channel",
    labels={"customer_segment": "Customer segment", "revenue": "Revenue", "channel": "Channel"},
)
segment_fig.update_layout(barmode="stack", legend={"orientation": "h", "y": 1.12, "x": 1, "xanchor": "right"})
st.plotly_chart(segment_fig, width="stretch")

st.subheader("7. Margin and Discount Diagnostic")
discount = (
    filtered.groupby(["category", "channel"], as_index=False)
    .agg(revenue=("revenue", "sum"), gross_margin=("gross_margin", "sum"), discount_rate=("discount_rate", "mean"))
)
discount["margin_rate"] = discount["gross_margin"] / discount["revenue"]
discount_fig = px.scatter(
    discount,
    x="discount_rate",
    y="margin_rate",
    size="revenue",
    color="channel",
    color_discrete_map=SALES_COLORS,
    facet_col="category",
    facet_col_wrap=3,
    title="Discount Pressure vs Margin by Category",
    labels={"discount_rate": "Average discount rate", "margin_rate": "Gross margin rate"},
)
discount_fig.update_layout(xaxis_tickformat=".1%", yaxis_tickformat=".1%", legend={"orientation": "h", "y": 1.08, "x": 1, "xanchor": "right"})
discount_fig.update_traces(marker={"opacity": 0.78, "line": {"width": 0}})
st.plotly_chart(discount_fig, width="stretch")

st.subheader("8. Operating Heatmap")
heatmap_df = filtered.copy()
heatmap_df["weekday"] = pd.Categorical(
    heatmap_df["date"].dt.day_name(),
    categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    ordered=True,
)
heatmap = (
    heatmap_df.groupby(["weekday", "channel"], observed=True, as_index=False)
    .agg(revenue=("revenue", "sum"))
)
heatmap_fig = px.imshow(
    heatmap.pivot_table(index="weekday", columns="channel", values="revenue", aggfunc="sum"),
    aspect="auto",
    text_auto=".2s",
    color_continuous_scale="Tealgrn",
    title="Revenue Heatmap by Weekday and Channel",
    labels={"x": "Channel", "y": "Weekday", "color": "Revenue"},
)
st.plotly_chart(heatmap_fig, width="stretch")

st.subheader("9. Drill-down Table")
drill = (
    filtered.groupby(["region", "channel", "category", "product"], as_index=False)
    .agg(revenue=("revenue", "sum"), gross_margin=("gross_margin", "sum"), orders=("orders", "sum"), units=("units", "sum"))
)
drill["margin_rate"] = drill["gross_margin"] / drill["revenue"]
drill = drill.sort_values("revenue", ascending=False).head(50)
st.dataframe(
    drill.style.format(
        {
            "revenue": "${:,.0f}",
            "gross_margin": "${:,.0f}",
            "orders": "{:,.0f}",
            "units": "{:,.0f}",
            "margin_rate": "{:.1%}",
        }
    ),
    width="stretch",
    hide_index=True,
)

st.subheader("10. Action Readout")
action_cols = st.columns(3)
with action_cols[0]:
    st.markdown(
        """
        <div class="section-band">
            <h3>Growth lever</h3>
            <p>
                Prioritize channels and regions where revenue growth is paired with
                stable margin and conversion, not just higher order volume.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with action_cols[1]:
    st.markdown(
        """
        <div class="section-band">
            <h3>Margin lever</h3>
            <p>
                Track discount pressure by category and channel. The dashboard flags
                where revenue is being bought with margin leakage.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with action_cols[2]:
    st.markdown(
        """
        <div class="section-band">
            <h3>Product lever</h3>
            <p>
                Use product and category leaders to plan merchandising, inventory
                allocation, stylist bundles, and next-best-offer journeys.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
