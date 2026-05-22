from __future__ import annotations

import html

import plotly.io as pio
import streamlit as st


def inject_global_styles() -> None:
    pio.templates["portfolio_premium"] = {
        "layout": {
            "font": {"family": "Arial, sans-serif", "color": "#17211b"},
            "paper_bgcolor": "rgba(255,253,247,0)",
            "plot_bgcolor": "rgba(255,253,247,0.72)",
            "colorway": ["#0f766e", "#7c3aed", "#b7791f", "#2563eb", "#be185d", "#475569"],
            "xaxis": {
                "gridcolor": "rgba(102,113,102,0.14)",
                "linecolor": "rgba(102,113,102,0.20)",
                "zerolinecolor": "rgba(102,113,102,0.18)",
            },
            "yaxis": {
                "gridcolor": "rgba(102,113,102,0.14)",
                "linecolor": "rgba(102,113,102,0.20)",
                "zerolinecolor": "rgba(102,113,102,0.18)",
            },
            "legend": {"orientation": "h", "y": 1.08, "x": 0},
            "margin": {"l": 32, "r": 24, "t": 72, "b": 48},
            "title": {"font": {"size": 18, "color": "#17211b"}},
        }
    }
    pio.templates.default = "portfolio_premium"

    st.markdown(
        """
        <style>
            :root {
                --ink: #17211b;
                --muted: #667166;
                --line: #ded8c7;
                --soft: #f7f6f1;
                --panel: rgba(255, 253, 247, 0.90);
                --accent: #0f766e;
                --accent-2: #7c3aed;
                --gold: #b7791f;
                --rose: #be185d;
                --shadow: 0 18px 48px rgba(34, 45, 38, 0.10);
            }
            .stApp {
                background:
                    linear-gradient(180deg, #f7f6f1 0%, #f1eee6 45%, #fbfaf6 100%);
            }
            .block-container {
                padding-top: 1.35rem;
                padding-bottom: 3rem;
                max-width: 1260px;
            }
            h1, h2, h3 {
                letter-spacing: 0;
                color: var(--ink);
            }
            div[data-testid="stHeader"] {
                background: rgba(247, 246, 241, 0.86);
                backdrop-filter: blur(14px);
                border-bottom: 1px solid rgba(222, 216, 199, 0.72);
            }
            div[data-testid="stTopNav"] {
                background: rgba(247, 246, 241, 0.80);
                border-bottom: 1px solid rgba(222, 216, 199, 0.72);
                backdrop-filter: blur(16px);
            }
            div[data-testid="stTopNav"] a {
                border-radius: 999px;
                font-weight: 700;
                color: var(--muted);
            }
            div[data-testid="stTopNav"] a:hover {
                color: var(--ink);
                background: rgba(15, 118, 110, 0.08);
            }
            div[data-testid="stSidebar"] {
                background: #f3f0e8;
                border-right: 1px solid var(--line);
            }
            div[data-testid="stMetric"] {
                background: var(--panel);
                border: 1px solid rgba(222, 216, 199, 0.94);
                border-radius: 8px;
                padding: 1rem 1.1rem;
                margin-top: 0.65rem;
                min-height: 136px;
                height: 100%;
                box-shadow: var(--shadow);
            }
            div[data-testid="stMetric"] label {
                min-height: 2.65rem;
                display: flex;
                align-items: flex-start;
            }
            div[data-testid="stMetricValue"] {
                min-height: 2.45rem;
                display: flex;
                align-items: center;
            }
            div[data-testid="stMetricDelta"] {
                min-height: 1.5rem;
            }
            .hero {
                position: relative;
                overflow: hidden;
                border: 1px solid rgba(222, 216, 199, 0.95);
                border-radius: 8px;
                padding: 2.8rem;
                background:
                    linear-gradient(135deg, rgba(255, 253, 247, 0.98), rgba(238, 233, 221, 0.88)),
                    #fffdf7;
                box-shadow: 0 28px 72px rgba(34, 45, 38, 0.12);
                margin-bottom: 1.35rem;
            }
            .hero::after {
                content: "";
                position: absolute;
                right: -3rem;
                top: 0;
                width: 24rem;
                height: 100%;
                background:
                    linear-gradient(135deg, rgba(15, 118, 110, 0.18), rgba(124, 58, 237, 0.10)),
                    repeating-linear-gradient(135deg, rgba(23, 33, 27, 0.08) 0 1px, transparent 1px 14px);
                transform: skewX(-12deg);
                border-radius: 8px;
            }
            .hero h1 {
                position: relative;
                z-index: 1;
                max-width: 860px;
                font-size: 3rem;
                line-height: 1.04;
                margin: 0.25rem 0 1rem 0;
            }
            .hero-copy {
                position: relative;
                z-index: 1;
                max-width: 760px;
                color: var(--muted);
                font-size: 1.05rem;
                line-height: 1.7;
            }
            .eyebrow {
                position: relative;
                z-index: 1;
                color: var(--accent);
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                margin: 0;
                text-transform: uppercase;
            }
            .notice {
                border: 1px solid rgba(15, 118, 110, 0.22);
                border-left: 4px solid var(--accent);
                background: rgba(236, 253, 245, 0.62);
                color: #334155;
                padding: 0.9rem 1rem;
                margin: 0.75rem 0 1.25rem 0;
                border-radius: 4px;
            }
            .portfolio-card, .stat-card, .contact-card, .insight-card {
                border: 1px solid var(--line);
                border-radius: 8px;
                background: var(--panel);
                box-shadow: var(--shadow);
            }
            .portfolio-card {
                height: 282px;
                padding: 1.2rem;
                display: flex;
                flex-direction: column;
                transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
            }
            .portfolio-card:hover, .stat-card:hover {
                border-color: rgba(15, 118, 110, 0.34);
                box-shadow: 0 22px 50px rgba(15, 118, 110, 0.12);
                transform: translateY(-2px);
            }
            .portfolio-card h3 {
                font-size: 1.05rem;
                line-height: 1.25;
                min-height: 2.7rem;
                margin: 0.5rem 0 0.65rem 0;
                display: flex;
                align-items: flex-start;
            }
            .portfolio-card p, .stat-card p, .insight-card p {
                color: var(--muted);
                line-height: 1.55;
                margin-bottom: 0;
            }
            .status-pill {
                display: inline-block;
                border: 1px solid rgba(15, 118, 110, 0.25);
                border-radius: 999px;
                color: #0f766e;
                background: rgba(236, 253, 245, 0.78);
                font-size: 0.76rem;
                font-weight: 700;
                padding: 0.18rem 0.55rem;
            }
            .stat-card {
                height: 170px;
                padding: 1.05rem;
                margin-bottom: 1rem;
                display: flex;
                flex-direction: column;
                transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
            }
            .stat-card strong {
                display: block;
                color: var(--ink);
                font-size: 0.98rem;
                line-height: 1.25;
                min-height: 2.5rem;
                margin-bottom: 0.3rem;
            }
            .contact-card {
                display: grid;
                gap: 0.75rem;
                padding: 1.1rem;
                min-height: 146px;
                align-content: center;
            }
            .contact-card a {
                color: var(--accent);
                font-weight: 650;
                text-decoration: none;
                border-bottom: 1px solid transparent;
                width: fit-content;
            }
            .contact-card a:hover {
                border-bottom-color: rgba(15, 118, 110, 0.44);
            }
            .insight-card {
                padding: 1rem;
                margin-top: 0.5rem;
                border-left: 4px solid var(--accent);
            }
            .placeholder-panel {
                border: 1px dashed #b7ad97;
                border-radius: 8px;
                background:
                    linear-gradient(135deg, rgba(15, 118, 110, 0.07), rgba(183, 121, 31, 0.08)),
                    rgba(255, 253, 247, 0.86);
                padding: 2.1rem;
                min-height: 260px;
                box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.72);
            }
            .placeholder-panel h3 {
                margin-top: 0;
            }
            .section-band {
                border: 1px solid var(--line);
                border-radius: 8px;
                background: rgba(255, 253, 247, 0.82);
                padding: 1.2rem;
                min-height: 100%;
                box-shadow: 0 14px 34px rgba(34, 45, 38, 0.06);
            }
            .paired-card {
                min-height: 286px;
            }
            .market-card {
                border: 1px solid var(--line);
                border-radius: 8px;
                background: rgba(255, 253, 247, 0.82);
                padding: 1.2rem;
                min-height: 286px;
                box-shadow: 0 14px 34px rgba(34, 45, 38, 0.06);
            }
            .market-card h3 {
                margin-top: 0;
                margin-bottom: 0.85rem;
            }
            .market-group-title {
                color: var(--ink);
                font-size: 0.82rem;
                font-weight: 750;
                letter-spacing: 0.04em;
                margin: 0.85rem 0 0.45rem 0;
                text-transform: uppercase;
            }
            .market-chip-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.45rem;
            }
            .market-chip {
                border: 1px solid rgba(15, 118, 110, 0.22);
                border-radius: 999px;
                background: rgba(236, 253, 245, 0.64);
                color: #17453d;
                font-size: 0.84rem;
                font-weight: 650;
                padding: 0.32rem 0.62rem;
            }
            .welcome-grid-card {
                height: 300px;
                border: 1px solid var(--line);
                border-radius: 8px;
                background: var(--panel);
                padding: 1.2rem;
                box-shadow: var(--shadow);
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
            }
            .welcome-grid-card:hover {
                transform: translateY(-2px);
                border-color: rgba(15, 118, 110, 0.34);
                box-shadow: 0 22px 50px rgba(15, 118, 110, 0.12);
            }
            .welcome-icon {
                width: 2.45rem;
                height: 2.45rem;
                display: grid;
                place-items: center;
                border-radius: 8px;
                background: linear-gradient(135deg, rgba(15, 118, 110, 0.14), rgba(183, 121, 31, 0.12));
                font-size: 1.35rem;
                margin-bottom: 0.9rem;
            }
            .welcome-grid-card h3 {
                margin: 0 0 0.5rem 0;
                font-size: 1.04rem;
                line-height: 1.25;
                min-height: 2.6rem;
                display: flex;
                align-items: flex-start;
            }
            .welcome-grid-card p {
                color: var(--muted);
                line-height: 1.52;
                margin: 0;
            }
            .method-note {
                border: 1px solid rgba(15, 118, 110, 0.22);
                border-radius: 8px;
                background: rgba(236, 253, 245, 0.58);
                padding: 1rem;
                color: #334155;
            }
            div[data-testid="stExpander"] {
                border-color: var(--line);
                background: rgba(255, 253, 247, 0.76);
                box-shadow: 0 12px 30px rgba(34, 45, 38, 0.05);
            }
            div[data-testid="stPlotlyChart"] {
                border: 1px solid rgba(222, 216, 199, 0.72);
                border-radius: 8px;
                background: rgba(255, 253, 247, 0.80);
                padding: 0.35rem;
                box-shadow: 0 14px 34px rgba(34, 45, 38, 0.06);
            }
            @media (max-width: 760px) {
                .hero {
                    padding: 1.4rem;
                }
                .hero h1 {
                    font-size: 2.1rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_project_card(title: str, status: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="portfolio-card">
            <span class="status-pill">{html.escape(status)}</span>
            <h3>{html.escape(title)}</h3>
            <p>{html.escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="stat-card">
            <strong>{html.escape(title)}</strong>
            <p>{html.escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight(text: str) -> None:
    st.markdown(
        f"""
        <div class="insight-card">
            <p>{html.escape(text)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_welcome_card(icon: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="welcome-grid-card">
            <div>
                <div class="welcome-icon">{html.escape(icon)}</div>
                <h3>{html.escape(title)}</h3>
                <p>{html.escape(body)}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
