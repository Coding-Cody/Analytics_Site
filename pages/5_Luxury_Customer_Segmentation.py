from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

from utils.data import load_luxury_segmentation_data
from utils.theme import CHANNEL_COLORS, SEGMENT_COLORS, THEME
from utils.ui import inject_global_styles, render_insight, render_kpi_card


inject_global_styles()

st.markdown(
    """
    <section class="hero">
        <p class="eyebrow">Premium menswear retail | Customer segmentation</p>
        <h1>Customer segmentation for clienteling, wardrobe growth, and lifecycle strategy.</h1>
        <p class="hero-copy">
            Client project structure for a premium menswear retailer similar to Harry Rosen:
            customer-level feature engineering, clustering methodology, segment economics,
            product affinity, lifecycle movement, and advisor-ready activation design.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

customers, segment_summary, profile = load_luxury_segmentation_data()

with st.sidebar:
    st.header("Segmentation Controls")
    selected_segments = st.multiselect(
        "Segments",
        sorted(customers["segment"].unique()),
        default=sorted(customers["segment"].unique()),
    )
    selected_regions = st.multiselect(
        "Regions",
        sorted(customers["region"].unique()),
        default=sorted(customers["region"].unique()),
    )
    selected_lifecycle = st.multiselect(
        "Lifecycle stage",
        sorted(customers["lifecycle_stage"].unique()),
        default=sorted(customers["lifecycle_stage"].unique()),
    )
    min_clv, max_clv = st.slider(
        "Predicted CLV range",
        min_value=0,
        max_value=450_000,
        value=(0, 450_000),
        step=10_000,
        format="$%d",
    )

filtered = customers[
    (customers["segment"].isin(selected_segments))
    & (customers["region"].isin(selected_regions))
    & (customers["lifecycle_stage"].isin(selected_lifecycle))
    & (customers["predicted_clv"].between(min_clv, max_clv))
].copy()

if filtered.empty:
    st.info("Adjust filters to return at least one customer segment.")
    st.stop()

filtered_summary = (
    filtered.groupby("segment", as_index=False)
    .agg(
        customers=("customer_id", "count"),
        annual_spend=("annual_spend", "mean"),
        predicted_clv=("predicted_clv", "mean"),
        purchase_frequency=("purchase_frequency", "mean"),
        average_order_value=("average_order_value", "mean"),
        recency_days=("recency_days", "mean"),
        online_share=("online_share", "mean"),
        appointment_rate=("appointment_rate", "mean"),
        event_attendance=("event_attendance", "mean"),
        discount_sensitivity=("discount_sensitivity", "mean"),
        service_interactions=("service_interactions", "mean"),
        category_breadth=("category_breadth", "mean"),
        tailoring_intensity=("tailoring_intensity", "mean"),
    )
    .sort_values("predicted_clv", ascending=False)
)
filtered_summary["customer_share"] = filtered_summary["customers"] / filtered_summary["customers"].sum()

st.subheader("1. Business Question")
left, right = st.columns(2, gap="small")
with left:
    st.markdown(
        """
        <div class="section-band intro-pair-card">
            <h3>Commercial objective</h3>
            <p>
                The segmentation was structured to support differentiated clienteling:
                which customers should receive made-to-measure outreach, who is ready
                for wardrobe expansion, which digital buyers can be migrated into store
                appointments, and which gifting customers need lower-friction journeys.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        """
        <div class="section-band intro-pair-card">
            <h3>Analytical objective</h3>
            <p>
                The model groups customers by behavioral similarity, not by one metric.
                Spend, frequency, recency, product breadth, tailoring behavior, channel
                mix, appointment engagement, service intensity, and discount sensitivity
                are interpreted together before segment strategy is written.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("2. Customer Grain and Data Model")
schema_cols = st.columns(4)
with schema_cols[0]:
    render_kpi_card("Customer grain", "1 row", "Customer x 12-month window")
with schema_cols[1]:
    render_kpi_card("Core features", "10+", "Behavioral, product, channel, and clienteling signals")
with schema_cols[2]:
    render_kpi_card("Segments", f"{filtered['segment'].nunique()}", "Selected cluster labels")
with schema_cols[3]:
    render_kpi_card("Customers", f"{len(filtered):,}", "Filtered population")

render_insight(
    "The project data model joins POS transactions, ecommerce behavior, clienteling notes, appointment logs, alteration/service history, product hierarchy, campaign exposure, and consent status at a stable customer key."
)

st.subheader("3. Feature Engineering")
feature_rows = pd.DataFrame(
    [
        {"Customer feature": "Annual spend", "Definition": "12-month net sales after returns and adjustments"},
        {"Customer feature": "Average order value", "Definition": "transaction-level value signal for premium basket behavior"},
        {"Customer feature": "Purchase frequency", "Definition": "repeat cadence across online and store channels"},
        {"Customer feature": "Recency", "Definition": "days since last purchase, inverted for profile scoring"},
        {"Customer feature": "Predicted CLV", "Definition": "forward-looking value score used for prioritization"},
        {"Customer feature": "Category breadth", "Definition": "number of categories purchased across tailoring, sportswear, footwear, accessories"},
        {"Customer feature": "Tailoring intensity", "Definition": "made-to-measure, suit, and alteration-related purchase behavior"},
        {"Customer feature": "Online share", "Definition": "share of transactions initiated or completed digitally"},
        {"Customer feature": "Appointment rate", "Definition": "store appointment and advisor-assisted selling behavior"},
        {"Customer feature": "Event engagement", "Definition": "trunk show, seasonal event, and private shopping attendance"},
        {"Customer feature": "Service interactions", "Definition": "alterations, wardrobe consultation, and post-purchase service touches"},
        {"Customer feature": "Discount sensitivity", "Definition": "promotion exposure and markdown purchase ratio"},
    ]
)
st.dataframe(
    feature_rows,
    hide_index=True,
    width="stretch",
)

st.markdown(
    """
    <div class="method-note">
        <strong>Preprocessing logic:</strong> monetary features are log-transformed,
        rate features are clipped to stable bounds, recency is directionally inverted
        during profiling, and tailoring-related variables are reviewed for collinearity
        so suit spend does not dominate the distance metric twice.
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("4. Clustering Methodology")
method_cols = st.columns(3)
with method_cols[0]:
    st.markdown(
        """
        <div class="section-band">
            <h3>Scaling</h3>
            <p>
                Robust scaling is preferred for premium retail spend because purchase value is
                highly skewed. Log spend and CLV reduce extreme-client leverage while
                preserving relative value differences.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with method_cols[1]:
    st.markdown(
        """
        <div class="section-band">
            <h3>Model selection</h3>
            <p>
                Candidate k values are evaluated with silhouette, Davies-Bouldin,
                segment size stability, profile separability, and commercial
                interpretability. The final k must support action, not just fit metrics.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with method_cols[2]:
    st.markdown(
        """
        <div class="section-band">
            <h3>Interpretation</h3>
            <p>
                Cluster labels are assigned after profiling. The workflow treats labels
                as business-facing interpretations of the feature space, not as model
                outputs that are meaningful without context.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="method-note">
        <strong>Feature weighting:</strong> the clustering distance is not treated as
        a flat average of raw variables. Customer value and lifecycle signals anchor
        the segmentation, while product, channel, and service signals explain how to
        activate each segment.
    </div>
    """,
    unsafe_allow_html=True,
)
weight_rows = pd.DataFrame(
    [
        {"Feature group": "Customer value", "Weight": 0.28, "Feature examples": "annual spend, AOV, predicted CLV"},
        {"Feature group": "Lifecycle timing", "Weight": 0.18, "Feature examples": "purchase frequency, recency"},
        {"Feature group": "Product behavior", "Weight": 0.22, "Feature examples": "category breadth, tailoring intensity"},
        {"Feature group": "Channel and clienteling", "Weight": 0.20, "Feature examples": "online share, appointment rate, event engagement"},
        {"Feature group": "Sensitivity and service", "Weight": 0.12, "Feature examples": "discount sensitivity, service interactions"},
    ]
)
weight_fig = px.bar(
    weight_rows,
    x="Feature group",
    y="Weight",
    color="Feature group",
    color_discrete_sequence=list(CHANNEL_COLORS.values()),
    text_auto=".0%",
    title="Feature Weighting Used for Clustering Distance",
    labels={"Weight": "Weight", "Feature group": "Feature group"},
)
weight_fig.update_layout(showlegend=False, yaxis_tickformat=".0%", margin={"b": 90})
weight_fig.update_xaxes(tickangle=-18)
weight_fig.update_traces(marker_line_width=0, opacity=0.88, textfont_color=THEME["bar_text"])
st.plotly_chart(weight_fig, width="stretch")

st.subheader("5. Segment Portfolio Snapshot")
metric_cols = st.columns(4)
with metric_cols[0]:
    render_kpi_card("Filtered customers", f"{len(filtered):,}", "Current population")
with metric_cols[1]:
    render_kpi_card("Avg annual spend", f"${filtered['annual_spend'].mean():,.0f}", "Mean 12-month value")
with metric_cols[2]:
    render_kpi_card("Avg predicted CLV", f"${filtered['predicted_clv'].mean():,.0f}", "Longer-term value signal")
with metric_cols[3]:
    render_kpi_card("Appointment rate", f"{filtered['appointment_rate'].mean():.0%}", "Clienteling engagement")

portfolio_fig = px.bar(
    filtered_summary,
    x="segment",
    y="customers",
    color="segment",
    color_discrete_map=SEGMENT_COLORS,
    text="customers",
    title="Segment Size",
    labels={"segment": "Segment", "customers": "Customers"},
)
portfolio_fig.update_layout(showlegend=False)
portfolio_fig.update_traces(marker_line_width=0, opacity=0.88, textposition="outside", textfont_color=THEME["bar_text"])
st.plotly_chart(portfolio_fig, width="stretch")
render_insight(
    "Segment size is checked before activation. Smaller high-value groups support advisor-led outreach, while larger moderate-value groups need scalable email, SMS, and ecommerce journey design."
)

st.subheader("6. Customer Map")
scatter_fig = px.scatter(
    filtered,
    x="embedding_x",
    y="embedding_y",
    color="segment",
    size="predicted_clv",
    hover_data={
        "customer_id": True,
        "region": True,
        "annual_spend": ":$,.0f",
        "predicted_clv": ":$,.0f",
        "appointment_rate": ":.0%",
        "embedding_x": False,
        "embedding_y": False,
    },
    color_discrete_map=SEGMENT_COLORS,
    title="Two-dimensional Customer Similarity Map",
    labels={"embedding_x": "Similarity axis 1", "embedding_y": "Similarity axis 2"},
)
scatter_fig.update_traces(marker={"opacity": 0.72, "line": {"width": 0}})
st.plotly_chart(scatter_fig, width="stretch")
render_insight(
    "The map is a visualization layer for the clustered feature space. It should not be used alone to define segments; it is used to inspect separation, overlap, and potential transition zones."
)

st.subheader("7. Segment Economics")
econ_left, econ_right = st.columns(2, gap="medium")
with econ_left:
    clv_fig = px.bar(
        filtered_summary,
        x="segment",
        y="predicted_clv",
        color="segment",
        color_discrete_map=SEGMENT_COLORS,
        title="Average Predicted CLV by Segment",
        labels={"segment": "Segment", "predicted_clv": "Predicted CLV"},
        text_auto=".2s",
    )
    clv_fig.update_layout(showlegend=False)
    clv_fig.update_traces(marker_line_width=0, opacity=0.88, textfont_color=THEME["bar_text"])
    st.plotly_chart(clv_fig, width="stretch")
with econ_right:
    spend_fig = px.box(
        filtered,
        x="segment",
        y="annual_spend",
        color="segment",
        color_discrete_map=SEGMENT_COLORS,
        points="outliers",
        title="Annual Spend Distribution",
        labels={"segment": "Segment", "annual_spend": "Annual spend"},
    )
    spend_fig.update_layout(showlegend=False)
    st.plotly_chart(spend_fig, width="stretch")

st.subheader("8. Segment Profile Diagnostics")
profile_filtered = profile[profile["segment"].isin(filtered["segment"].unique())]
heatmap_fig = px.imshow(
    profile_filtered.pivot_table(
        index="segment",
        columns="feature",
        values="scaled_score",
        aggfunc="mean",
    ),
    aspect="auto",
    color_continuous_scale="Tealgrn",
    title="Scaled Segment Profile Heatmap",
    labels={"x": "Feature", "y": "Segment", "color": "Scaled score"},
)
st.plotly_chart(heatmap_fig, width="stretch")
render_insight(
    "The heatmap identifies what makes each segment distinct. This is the main bridge from clustering output to business language."
)

selected_profile_segment = st.selectbox(
    "Profile detail",
    filtered_summary["segment"].tolist(),
)
radar_features = [
    "Annual Spend",
    "Predicted Clv",
    "Purchase Frequency",
    "Average Order Value",
    "Online Share",
    "Appointment Rate",
    "Event Attendance",
    "Category Breadth",
    "Tailoring Intensity",
]
radar_df = profile_filtered[
    (profile_filtered["segment"] == selected_profile_segment)
    & (profile_filtered["feature"].isin(radar_features))
].copy()
radar_fig = go.Figure()
radar_fig.add_trace(
    go.Scatterpolar(
        r=radar_df["scaled_score"].tolist() + [radar_df["scaled_score"].iloc[0]],
        theta=radar_df["feature"].tolist() + [radar_df["feature"].iloc[0]],
        fill="toself",
        name=selected_profile_segment,
        line_color=SEGMENT_COLORS.get(selected_profile_segment, THEME["accent"]),
    )
)
radar_fig.update_layout(
    title=f"Profile Shape: {selected_profile_segment}",
    polar={"radialaxis": {"visible": True, "range": [0, 1]}},
    showlegend=False,
)
st.plotly_chart(radar_fig, width="stretch")

st.subheader("9. Product Affinity and Channel Behavior")
category = (
    filtered.groupby(["segment", "preferred_category"], as_index=False)
    .agg(customers=("customer_id", "count"))
)
category["share"] = category["customers"] / category.groupby("segment")["customers"].transform("sum")
category_fig = px.bar(
    category,
    x="segment",
    y="share",
    color="preferred_category",
    color_discrete_sequence=list(CHANNEL_COLORS.values()),
    title="Preferred Category Mix by Segment",
    labels={"segment": "Segment", "share": "Customer share", "preferred_category": "Preferred category"},
)
category_fig.update_layout(
    barmode="stack",
    yaxis_tickformat=".0%",
    margin={"t": 110, "b": 120},
    legend={
        "orientation": "h",
        "yanchor": "bottom",
        "y": 1.12,
        "xanchor": "right",
        "x": 1,
    },
)
category_fig.update_xaxes(tickangle=-22)
st.plotly_chart(category_fig, width="stretch")
render_insight(
    "Menswear segmentation needs product context. Two customers with similar spend can require different treatment if one is tailoring-led, another is sportswear-led, and another is occasion-gifting led."
)

st.subheader("10. Lifecycle Actions")
activation = {
    "Made-to-Measure Loyalists": "Protect the relationship with advisor-led appointments, seasonal fabric previews, alteration follow-ups, and private wardrobe reviews.",
    "Wardrobe Builders": "Drive category expansion through curated outfits, sportswear-to-tailoring bridges, and occasion-based recommendations.",
    "Occasion Suit Buyers": "Use wedding, event, and business-season triggers to reactivate customers before the next high-intent need.",
    "Digital Style Seekers": "Build online-to-store migration paths with stylist appointments, fit guidance, and personalized product discovery.",
    "Entry Luxury Gifters": "Use gifting reminders, accessory education, lower-friction replenishment moments, and clear next-best-product journeys.",
}
activation_rows = [
    {"Segment": segment, "Activation logic": activation[segment]}
    for segment in filtered_summary["segment"]
]
st.dataframe(activation_rows, width="stretch", hide_index=True)

lifecycle = (
    filtered.groupby(["segment", "lifecycle_stage"], as_index=False)
    .agg(customers=("customer_id", "count"))
)
lifecycle["share"] = lifecycle["customers"] / lifecycle.groupby("segment")["customers"].transform("sum")
lifecycle_fig = px.bar(
    lifecycle,
    x="segment",
    y="share",
    color="lifecycle_stage",
    color_discrete_sequence=list(CHANNEL_COLORS.values()),
    title="Lifecycle Mix by Segment",
    labels={"segment": "Segment", "share": "Customer share", "lifecycle_stage": "Lifecycle stage"},
)
lifecycle_fig.update_layout(
    barmode="stack",
    yaxis_tickformat=".0%",
    margin={"t": 110, "b": 120},
    legend={
        "orientation": "h",
        "yanchor": "bottom",
        "y": 1.12,
        "xanchor": "right",
        "x": 1,
    },
)
lifecycle_fig.update_xaxes(tickangle=-22)
st.plotly_chart(lifecycle_fig, width="stretch")

st.subheader("11. Measurement and Governance")
governance_cols = st.columns(3)
with governance_cols[0]:
    st.markdown(
        """
        <div class="section-band">
            <h3>Stability</h3>
            <p>
                Monitor segment migration, population drift, centroid movement, and
                changes in feature distributions before refreshing labels.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with governance_cols[1]:
    st.markdown(
        """
        <div class="section-band">
            <h3>Activation testing</h3>
            <p>
                Use holdouts or geo/customer-level experiments to measure whether
                segment-specific treatments improve margin, CLV, and retention.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with governance_cols[2]:
    st.markdown(
        """
        <div class="section-band">
            <h3>Operational rules</h3>
            <p>
                Keep segment labels explainable, consent-aware, and integrated with
                CRM workflows so client advisors can act on them consistently.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
