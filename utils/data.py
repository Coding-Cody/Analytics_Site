from __future__ import annotations

import numpy as np
import pandas as pd

from utils.theme import CHANNEL_COLORS


CHANNELS = {
    "Paid Search": {
        "base_spend": 82_000,
        "roi": 2.8,
        "half_life": 1.2,
        "alpha": 1.35,
        "ec50": 72_000,
        "color": CHANNEL_COLORS["Paid Search"],
        "response": "High intent demand capture with faster carryover decay.",
    },
    "Paid Social": {
        "base_spend": 58_000,
        "roi": 1.9,
        "half_life": 2.0,
        "alpha": 1.20,
        "ec50": 64_000,
        "color": CHANNEL_COLORS["Paid Social"],
        "response": "Efficient reach and consideration builder with medium carryover.",
    },
    "YouTube": {
        "base_spend": 46_000,
        "roi": 1.6,
        "half_life": 3.4,
        "alpha": 1.10,
        "ec50": 78_000,
        "color": CHANNEL_COLORS["YouTube"],
        "response": "Upper-funnel video with delayed conversion effect.",
    },
    "Display": {
        "base_spend": 34_000,
        "roi": 1.2,
        "half_life": 1.7,
        "alpha": 1.00,
        "ec50": 52_000,
        "color": CHANNEL_COLORS["Display"],
        "response": "Broad reach channel with modest marginal return.",
    },
    "TV": {
        "base_spend": 105_000,
        "roi": 1.4,
        "half_life": 4.6,
        "alpha": 1.05,
        "ec50": 145_000,
        "color": CHANNEL_COLORS["TV"],
        "response": "Scaled awareness channel with longer memory and slower decay.",
    },
}


def _adstock(values: np.ndarray, half_life: float) -> np.ndarray:
    decay = 0.5 ** (1 / half_life)
    adstocked = np.zeros_like(values, dtype=float)
    for index, value in enumerate(values):
        adstocked[index] = value + (adstocked[index - 1] * decay if index else 0)
    return adstocked


def _hill_response(x: np.ndarray | float, alpha: float, ec50: float) -> np.ndarray | float:
    x = np.maximum(x, 0)
    return np.power(x, alpha) / (np.power(x, alpha) + np.power(ec50, alpha))


def load_mmm_case_data() -> pd.DataFrame:
    rng = np.random.default_rng(11)
    weeks = pd.date_range("2025-01-06", periods=52, freq="W-MON")
    rows = []

    for channel, details in CHANNELS.items():
        spend_values = []
        for week_number, week in enumerate(weeks):
            seasonality = 1 + 0.16 * np.sin((week_number - 6) / 52 * 2 * np.pi)
            pulse = 1 + rng.normal(0, 0.11)
            if channel in {"TV", "YouTube"} and week.month in (9, 10, 11):
                pulse += 0.18
            if channel in {"Paid Search", "Paid Social"} and week.month in (4, 5, 12):
                pulse += 0.12
            spend_values.append(max(details["base_spend"] * seasonality * pulse, 0))

        spend_array = np.array(spend_values)
        adstocked = _adstock(spend_array, details["half_life"])
        response = _hill_response(adstocked, details["alpha"], details["ec50"])
        contribution = response * details["base_spend"] * details["roi"] * 2.25

        for week, spend, stock, response_value, contribution_value in zip(
            weeks, spend_array, adstocked, response, contribution
        ):
            rows.append(
                {
                    "week": week,
                    "channel": channel,
                    "spend": spend,
                    "adstocked_spend": stock,
                    "response_index": response_value,
                    "contribution": contribution_value,
                    "roi": contribution_value / spend if spend else 0,
                    "half_life": details["half_life"],
                    "ec50": details["ec50"],
                    "response_note": details["response"],
                }
            )

    df = pd.DataFrame(rows)
    weekly_totals = df.groupby("week", as_index=False)["contribution"].sum()
    baseline = pd.Series(
        480_000
        + 34_000 * np.sin(np.linspace(0, 2 * np.pi, len(weekly_totals)))
        + rng.normal(0, 12_000, len(weekly_totals)),
        index=weekly_totals.index,
    )
    weekly_totals["baseline"] = baseline.clip(lower=410_000)
    weekly_totals["kpi_sales"] = weekly_totals["baseline"] + weekly_totals["contribution"]

    return df.merge(
        weekly_totals[["week", "baseline", "kpi_sales"]],
        on="week",
        how="left",
    )


def summarize_channels(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("channel", as_index=False)
        .agg(
            spend=("spend", "sum"),
            adstocked_spend=("adstocked_spend", "mean"),
            contribution=("contribution", "sum"),
            roi=("roi", "mean"),
            half_life=("half_life", "first"),
            ec50=("ec50", "first"),
            response_note=("response_note", "first"),
        )
        .sort_values("contribution", ascending=False)
    )
    summary["share_of_contribution"] = summary["contribution"] / summary["contribution"].sum()
    return summary


def load_response_curve_data() -> pd.DataFrame:
    rows = []
    for channel, details in CHANNELS.items():
        spend_grid = np.linspace(0, details["base_spend"] * 3.0, 80)
        response = _hill_response(spend_grid, details["alpha"], details["ec50"])
        contribution = response * details["base_spend"] * details["roi"] * 2.25
        marginal = np.gradient(contribution, spend_grid, edge_order=1)
        for spend, response_value, contribution_value, marginal_value in zip(
            spend_grid, response, contribution, marginal
        ):
            rows.append(
                {
                    "channel": channel,
                    "weekly_spend": spend,
                    "response_index": response_value,
                    "expected_contribution": contribution_value,
                    "marginal_return": marginal_value,
                    "ec50": details["ec50"],
                }
            )
    return pd.DataFrame(rows)


def load_geo_test_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(21)
    weeks = pd.date_range("2025-01-06", periods=24, freq="W-MON")
    test_markets = ["Toronto M5V", "Mississauga L5B", "Brampton L6Y", "Hamilton L8P"]
    control_markets = ["Ottawa K1P", "London N6A", "Kitchener N2G", "Kingston K7L"]
    all_markets = test_markets + control_markets
    rows = []

    for market_index, market in enumerate(all_markets):
        is_test = market in test_markets
        market_scale = 1 + market_index * 0.035
        for week_index, week in enumerate(weeks):
            trend = 1000 + week_index * 8
            seasonality = 55 * np.sin(week_index / 24 * 2 * np.pi)
            treatment = is_test and week_index >= 12
            lift = 122 if treatment else 0
            kpi = (trend + seasonality + lift) * market_scale + rng.normal(0, 24)
            rows.append(
                {
                    "week": week,
                    "market": market,
                    "group": "Test markets" if is_test else "Matched controls",
                    "period": "Test period" if week_index >= 12 else "Pre period",
                    "kpi": max(kpi, 0),
                    "spend": 6200 * market_scale if treatment else 0,
                }
            )

    market_df = pd.DataFrame(rows)
    group_df = (
        market_df.groupby(["week", "group", "period"], as_index=False)
        .agg(kpi=("kpi", "mean"), spend=("spend", "sum"))
        .sort_values(["week", "group"])
    )
    return market_df, group_df


def load_synthetic_control_data() -> pd.DataFrame:
    rng = np.random.default_rng(33)
    weeks = pd.date_range("2025-01-06", periods=24, freq="W-MON")
    rows = []
    for week_index, week in enumerate(weeks):
        base = 1180 + week_index * 7 + 62 * np.sin(week_index / 24 * 2 * np.pi)
        synthetic = base + rng.normal(0, 14)
        treated = base + rng.normal(0, 18) + (145 if week_index >= 12 else 0)
        rows.extend(
            [
                {
                    "week": week,
                    "series": "Treated geography",
                    "period": "Test period" if week_index >= 12 else "Pre period",
                    "kpi": treated,
                },
                {
                    "week": week,
                    "series": "Synthetic control",
                    "period": "Test period" if week_index >= 12 else "Pre period",
                    "kpi": synthetic,
                },
            ]
        )
    return pd.DataFrame(rows)


def load_macro_kpi_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    cards = pd.DataFrame(
        [
            {
                "region": "Canada",
                "indicator": "CPI inflation",
                "value": 2.39,
                "unit": "%",
                "period": "Mar 2026",
                "source": "Statistics Canada / Outcome Canada public indicator feed",
                "status": "Watch",
            },
            {
                "region": "Canada",
                "indicator": "Unemployment rate",
                "value": 6.7,
                "unit": "%",
                "period": "Mar 2026",
                "source": "Statistics Canada / Labour Force Survey",
                "status": "Slack",
            },
            {
                "region": "Canada",
                "indicator": "Policy rate",
                "value": 2.2,
                "unit": "%",
                "period": "Apr 2026",
                "source": "Bank of Canada",
                "status": "Easing",
            },
            {
                "region": "Canada",
                "indicator": "Real GDP growth",
                "value": 0.97,
                "unit": "% y/y",
                "period": "Feb 2026",
                "source": "Statistics Canada / Outcome Canada public indicator feed",
                "status": "Growth",
            },
            {
                "region": "Global",
                "indicator": "OECD real GDP per capita",
                "value": 0.8,
                "unit": "% 2025",
                "period": "2025 annual",
                "source": "OECD statistical release, May 2026",
                "status": "Moderate",
            },
            {
                "region": "G7",
                "indicator": "G7 real GDP per capita",
                "value": 0.9,
                "unit": "% 2025",
                "period": "2025 annual",
                "source": "OECD statistical release, May 2026",
                "status": "Moderate",
            },
        ]
    )

    months = pd.period_range("2025-04", "2026-03", freq="M").astype(str)
    trend_rows = []
    canada_inflation = [1.7, 1.8, 1.9, 1.9, 2.0, 2.1, 2.3, 2.4, 2.5, 2.4, 2.4, 2.39]
    canada_unemployment = [6.8, 6.9, 6.9, 6.8, 6.7, 6.6, 6.7, 6.8, 6.8, 6.7, 6.7, 6.7]
    boc_rate = [2.7, 2.7, 2.7, 2.45, 2.45, 2.45, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2]
    global_growth_proxy = [0.5, 0.5, 0.6, 0.6, 0.7, 0.7, 0.7, 0.8, 0.8, 0.8, 0.9, 0.9]
    for month, inflation, unemployment, rate, growth in zip(
        months, canada_inflation, canada_unemployment, boc_rate, global_growth_proxy
    ):
        trend_rows.extend(
            [
                {"period": month, "indicator": "Canada CPI inflation", "value": inflation, "unit": "%"},
                {"period": month, "indicator": "Canada unemployment", "value": unemployment, "unit": "%"},
                {"period": month, "indicator": "Bank of Canada policy rate", "value": rate, "unit": "%"},
                {"period": month, "indicator": "Global growth monitor", "value": growth, "unit": "%"},
            ]
        )
    return cards, pd.DataFrame(trend_rows)


def load_luxury_segmentation_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(71)
    segment_config = {
        "Made-to-Measure Loyalists": {
            "n": 240,
            "annual_spend": 58_000,
            "frequency": 7.2,
            "aov": 8_100,
            "tenure": 6.8,
            "recency": 24,
            "online_share": 0.18,
            "discount_sensitivity": 0.08,
            "appointment_rate": 0.74,
            "event_attendance": 0.66,
            "service_interactions": 4.4,
            "breadth": 4.1,
            "tailoring_intensity": 0.82,
            "clv": 284_000,
            "x": -1.5,
            "y": 1.35,
        },
        "Wardrobe Builders": {
            "n": 190,
            "annual_spend": 32_000,
            "frequency": 4.4,
            "aov": 7_250,
            "tenure": 3.1,
            "recency": 38,
            "online_share": 0.28,
            "discount_sensitivity": 0.14,
            "appointment_rate": 0.61,
            "event_attendance": 0.48,
            "service_interactions": 2.7,
            "breadth": 3.2,
            "tailoring_intensity": 0.48,
            "clv": 158_000,
            "x": -0.25,
            "y": 1.05,
        },
        "Occasion Suit Buyers": {
            "n": 165,
            "annual_spend": 74_000,
            "frequency": 3.1,
            "aov": 23_800,
            "tenure": 8.2,
            "recency": 42,
            "online_share": 0.06,
            "discount_sensitivity": 0.05,
            "appointment_rate": 0.88,
            "event_attendance": 0.72,
            "service_interactions": 5.1,
            "breadth": 2.3,
            "tailoring_intensity": 0.76,
            "clv": 392_000,
            "x": -1.15,
            "y": -0.75,
        },
        "Digital Style Seekers": {
            "n": 310,
            "annual_spend": 9_200,
            "frequency": 2.6,
            "aov": 3_500,
            "tenure": 1.7,
            "recency": 58,
            "online_share": 0.78,
            "discount_sensitivity": 0.22,
            "appointment_rate": 0.18,
            "event_attendance": 0.08,
            "service_interactions": 0.7,
            "breadth": 1.8,
            "tailoring_intensity": 0.16,
            "clv": 36_000,
            "x": 1.3,
            "y": 0.65,
        },
        "Entry Luxury Gifters": {
            "n": 295,
            "annual_spend": 4_800,
            "frequency": 1.4,
            "aov": 3_430,
            "tenure": 1.2,
            "recency": 86,
            "online_share": 0.52,
            "discount_sensitivity": 0.34,
            "appointment_rate": 0.10,
            "event_attendance": 0.04,
            "service_interactions": 0.3,
            "breadth": 1.2,
            "tailoring_intensity": 0.10,
            "clv": 14_500,
            "x": 1.1,
            "y": -1.0,
        },
    }

    regions = ["Toronto", "Vancouver", "Montreal", "Calgary", "New York", "Los Angeles"]
    rows = []
    customer_id = 10000
    for segment, config in segment_config.items():
        for _ in range(config["n"]):
            spend = rng.lognormal(np.log(config["annual_spend"]), 0.34)
            frequency = max(rng.normal(config["frequency"], 0.9), 0.4)
            aov = spend / frequency
            recency = max(rng.normal(config["recency"], 18), 1)
            tenure = max(rng.normal(config["tenure"], 1.4), 0.1)
            online_share = np.clip(rng.normal(config["online_share"], 0.10), 0, 1)
            appointment_rate = np.clip(rng.normal(config["appointment_rate"], 0.12), 0, 1)
            event_attendance = np.clip(rng.normal(config["event_attendance"], 0.12), 0, 1)
            discount_sensitivity = np.clip(rng.normal(config["discount_sensitivity"], 0.08), 0, 1)
            service = max(rng.normal(config["service_interactions"], 0.8), 0)
            breadth = np.clip(rng.normal(config["breadth"], 0.65), 1, 5)
            tailoring_intensity = np.clip(rng.normal(config["tailoring_intensity"], 0.12), 0, 1)
            clv = rng.lognormal(np.log(config["clv"]), 0.30)
            rows.append(
                {
                    "customer_id": f"LC-{customer_id}",
                    "segment": segment,
                    "region": rng.choice(regions, p=[0.26, 0.17, 0.15, 0.10, 0.19, 0.13]),
                    "annual_spend": spend,
                    "purchase_frequency": frequency,
                    "average_order_value": aov,
                    "tenure_years": tenure,
                    "recency_days": recency,
                    "online_share": online_share,
                    "appointment_rate": appointment_rate,
                    "event_attendance": event_attendance,
                    "discount_sensitivity": discount_sensitivity,
                    "service_interactions": service,
                    "category_breadth": breadth,
                    "tailoring_intensity": tailoring_intensity,
                    "predicted_clv": clv,
                    "embedding_x": rng.normal(config["x"], 0.34),
                    "embedding_y": rng.normal(config["y"], 0.30),
                    "preferred_category": rng.choice(
                        ["Tailoring", "Made-to-Measure", "Sportswear", "Footwear", "Accessories"],
                        p=_category_mix_for_segment(segment),
                    ),
                    "lifecycle_stage": rng.choice(
                        ["New", "Developing", "Established", "At Risk"],
                        p=_lifecycle_mix_for_segment(segment),
                    ),
                }
            )
            customer_id += 1

    customers = pd.DataFrame(rows)
    segment_summary = (
        customers.groupby("segment", as_index=False)
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
    segment_summary["customer_share"] = segment_summary["customers"] / segment_summary["customers"].sum()

    features = [
        "annual_spend",
        "predicted_clv",
        "purchase_frequency",
        "average_order_value",
        "recency_days",
        "online_share",
        "appointment_rate",
        "event_attendance",
        "discount_sensitivity",
        "service_interactions",
        "category_breadth",
        "tailoring_intensity",
    ]
    profile_rows = []
    for feature in features:
        values = segment_summary[feature]
        minimum = values.min()
        span = values.max() - minimum
        for _, row in segment_summary.iterrows():
            scaled = 0.5 if span == 0 else (row[feature] - minimum) / span
            if feature == "recency_days":
                scaled = 1 - scaled
            profile_rows.append(
                {
                    "segment": row["segment"],
                    "feature": feature.replace("_", " ").title(),
                    "scaled_score": scaled,
                    "raw_value": row[feature],
                }
            )
    profile = pd.DataFrame(profile_rows)
    return customers, segment_summary, profile


def _category_mix_for_segment(segment: str) -> list[float]:
    mixes = {
        "Made-to-Measure Loyalists": [0.20, 0.46, 0.16, 0.08, 0.10],
        "Wardrobe Builders": [0.32, 0.18, 0.25, 0.13, 0.12],
        "Occasion Suit Buyers": [0.58, 0.10, 0.08, 0.08, 0.16],
        "Digital Style Seekers": [0.18, 0.04, 0.42, 0.22, 0.14],
        "Entry Luxury Gifters": [0.24, 0.03, 0.16, 0.18, 0.39],
    }
    return mixes[segment]


def _lifecycle_mix_for_segment(segment: str) -> list[float]:
    mixes = {
        "Made-to-Measure Loyalists": [0.04, 0.14, 0.72, 0.10],
        "Wardrobe Builders": [0.10, 0.42, 0.38, 0.10],
        "Occasion Suit Buyers": [0.12, 0.26, 0.40, 0.22],
        "Digital Style Seekers": [0.32, 0.44, 0.14, 0.10],
        "Entry Luxury Gifters": [0.42, 0.28, 0.08, 0.22],
    }
    return mixes[segment]
