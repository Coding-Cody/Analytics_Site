from __future__ import annotations

import html

import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --ink: #111827;
                --muted: #526071;
                --line: #dbe3ef;
                --soft: #f6f8fb;
                --blue: #2563eb;
                --teal: #0f766e;
                --rose: #be185d;
            }
            .stApp {
                background:
                    radial-gradient(circle at 0% 0%, rgba(37, 99, 235, 0.10), transparent 34rem),
                    linear-gradient(180deg, #fbfcfe 0%, #f5f7fb 42%, #ffffff 100%);
            }
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1240px;
            }
            h1, h2, h3 {
                letter-spacing: 0;
                color: var(--ink);
            }
            div[data-testid="stSidebar"] {
                background: #f8fafc;
                border-right: 1px solid #e2e8f0;
            }
            div[data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.86);
                border: 1px solid #dbe3ef;
                border-radius: 8px;
                padding: 1rem 1.1rem;
                min-height: 136px;
                height: 100%;
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
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
                border: 1px solid rgba(148, 163, 184, 0.34);
                border-radius: 8px;
                padding: 2.6rem;
                background:
                    linear-gradient(135deg, rgba(37, 99, 235, 0.12), rgba(15, 118, 110, 0.10) 54%, rgba(190, 24, 93, 0.07)),
                    #ffffff;
                box-shadow: 0 24px 60px rgba(15, 23, 42, 0.09);
                margin-bottom: 1.2rem;
            }
            .hero::after {
                content: "";
                position: absolute;
                right: -5rem;
                top: -7rem;
                width: 22rem;
                height: 22rem;
                background: linear-gradient(135deg, rgba(37, 99, 235, 0.14), rgba(15, 118, 110, 0.08));
                transform: rotate(18deg);
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
                color: var(--blue);
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                margin: 0;
                text-transform: uppercase;
            }
            .notice {
                border: 1px solid #dbeafe;
                border-left: 4px solid var(--blue);
                background: rgba(239, 246, 255, 0.78);
                color: #334155;
                padding: 0.9rem 1rem;
                margin: 0.75rem 0 1.25rem 0;
                border-radius: 4px;
            }
            .portfolio-card, .stat-card, .contact-card, .insight-card {
                border: 1px solid var(--line);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.92);
                box-shadow: 0 14px 34px rgba(15, 23, 42, 0.06);
            }
            .portfolio-card {
                height: 282px;
                padding: 1.2rem;
                display: flex;
                flex-direction: column;
                transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
            }
            .portfolio-card:hover, .stat-card:hover {
                border-color: #bfdbfe;
                box-shadow: 0 18px 40px rgba(37, 99, 235, 0.10);
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
                border: 1px solid #bfdbfe;
                border-radius: 999px;
                color: #1d4ed8;
                background: #eff6ff;
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
                color: #1d4ed8;
                font-weight: 650;
                text-decoration: none;
                border-bottom: 1px solid transparent;
                width: fit-content;
            }
            .contact-card a:hover {
                border-bottom-color: #93c5fd;
            }
            .insight-card {
                padding: 1rem;
                margin-top: 0.5rem;
                border-left: 4px solid var(--teal);
            }
            .placeholder-panel {
                border: 1px dashed #94a3b8;
                border-radius: 8px;
                background:
                    linear-gradient(135deg, rgba(37, 99, 235, 0.07), rgba(15, 118, 110, 0.06)),
                    rgba(255, 255, 255, 0.86);
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
                background: rgba(255, 255, 255, 0.78);
                padding: 1.2rem;
                min-height: 100%;
            }
            .welcome-grid-card {
                height: 300px;
                border: 1px solid var(--line);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.94);
                padding: 1.2rem;
                box-shadow: 0 16px 38px rgba(15, 23, 42, 0.07);
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
            }
            .welcome-grid-card:hover {
                transform: translateY(-2px);
                border-color: #bfdbfe;
                box-shadow: 0 20px 44px rgba(37, 99, 235, 0.11);
            }
            .welcome-icon {
                width: 2.45rem;
                height: 2.45rem;
                display: grid;
                place-items: center;
                border-radius: 8px;
                background: linear-gradient(135deg, rgba(37, 99, 235, 0.12), rgba(15, 118, 110, 0.12));
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
                border: 1px solid #dbeafe;
                border-radius: 8px;
                background: rgba(239, 246, 255, 0.78);
                padding: 1rem;
                color: #334155;
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
