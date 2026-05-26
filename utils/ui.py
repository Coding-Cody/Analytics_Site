from __future__ import annotations

import base64
import html
from pathlib import Path

import plotly.io as pio
import streamlit as st

from utils.theme import PLOTLY_COLORWAY, THEME


def inject_global_styles() -> None:
    pio.templates["portfolio_premium"] = {
        "layout": {
            "font": {"family": "Arial, sans-serif", "color": THEME["ink"]},
            "paper_bgcolor": THEME["paper_bg"],
            "plot_bgcolor": THEME["plot_bg"],
            "colorway": PLOTLY_COLORWAY,
            "xaxis": {
                "gridcolor": THEME["grid"],
                "linecolor": THEME["axis"],
                "zerolinecolor": THEME["zero"],
            },
            "yaxis": {
                "gridcolor": THEME["grid"],
                "linecolor": THEME["axis"],
                "zerolinecolor": THEME["zero"],
            },
            "legend": {"orientation": "h", "y": 1.08, "x": 0},
            "margin": {"l": 32, "r": 24, "t": 72, "b": 48},
            "title": {"font": {"size": 18, "color": THEME["ink"]}},
        }
    }
    pio.templates.default = "portfolio_premium"

    st.markdown(
        """
        <style>
            :root {
                --ink: __INK__;
                --deep: __DEEP__;
                --muted: __MUTED__;
                --line: __LINE__;
                --soft: __SOFT__;
                --soft-mid: __SOFT_MID__;
                --soft-light: __SOFT_LIGHT__;
                --sidebar: __SIDEBAR__;
                --panel: __PANEL__;
                --accent: __ACCENT__;
                --accent-2: __ACCENT_2__;
                --gold: __GOLD__;
                --rose: __ROSE__;
                --status-text: __STATUS_TEXT__;
                --placeholder-line: __PLACEHOLDER_LINE__;
                --shadow: __SHADOW__;
                --shadow-strong: __SHADOW_STRONG__;
            }
            .stApp {
                background:
                    linear-gradient(rgba(20, 26, 22, 0.025) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(20, 26, 22, 0.025) 1px, transparent 1px),
                    linear-gradient(180deg, var(--soft) 0%, var(--soft-mid) 45%, var(--soft-light) 100%);
                background-size: 34px 34px, 34px 34px, auto;
            }
            .block-container {
                padding-top: 1.05rem;
                padding-bottom: 3.5rem;
                max-width: 1260px;
            }
            h1, h2, h3 {
                letter-spacing: 0;
                color: var(--ink);
            }
            h2, div[data-testid="stMarkdownContainer"] h2 {
                margin-top: 2rem;
                padding-top: 0.45rem;
                border-top: 1px solid rgba(20, 26, 22, 0.10);
            }
            div[data-testid="stHeader"] {
                background: rgba(244, 239, 227, 0.72);
                backdrop-filter: blur(18px);
                border-bottom: 1px solid rgba(216, 207, 187, 0.62);
            }
            div[data-testid="stTopNav"] {
                width: 100%;
                max-width: 1180px;
                margin: 0.55rem auto 0.4rem auto;
                padding: 0.35rem;
                border: 1px solid rgba(216, 207, 187, 0.88);
                border-radius: 12px;
                background: rgba(255, 250, 240, 0.78);
                box-shadow: 0 16px 44px rgba(20, 26, 22, 0.12);
                backdrop-filter: blur(18px);
                overflow-x: auto;
                scrollbar-width: thin;
            }
            div[data-testid="stTopNav"] a {
                border-radius: 8px;
                font-weight: 760;
                font-size: 0.86rem;
                line-height: 1.1;
                color: var(--muted);
                padding: 0.55rem 0.72rem;
                white-space: nowrap;
                min-height: 2.35rem;
                display: inline-flex;
                align-items: center;
            }
            div[data-testid="stTopNav"] a:hover {
                color: var(--ink);
                background: rgba(20, 184, 166, 0.10);
            }
            div[data-testid="stSidebar"] {
                background: var(--sidebar);
                border-right: 1px solid var(--line);
            }
            div[data-testid="stMetric"] {
                background: rgba(255, 250, 240, 0.94);
                border: 1px solid rgba(222, 216, 199, 0.94);
                border-radius: 8px;
                padding: 1rem 1.1rem;
                margin-top: 0.65rem;
                min-height: 136px;
                height: 100%;
                box-shadow: 0 14px 40px rgba(20, 26, 22, 0.10);
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
                padding: 3.2rem;
                background:
                    linear-gradient(135deg, rgba(16, 22, 17, 0.98), rgba(21, 38, 31, 0.97) 54%, rgba(48, 38, 23, 0.94)),
                    var(--deep);
                box-shadow: var(--shadow-strong);
                margin-bottom: 1.55rem;
            }
            .hero::before {
                content: "";
                position: absolute;
                inset: 0;
                background:
                    repeating-linear-gradient(90deg, rgba(255, 250, 240, 0.055) 0 1px, transparent 1px 42px),
                    repeating-linear-gradient(0deg, rgba(255, 250, 240, 0.040) 0 1px, transparent 1px 42px);
                pointer-events: none;
            }
            .hero::after {
                content: "";
                position: absolute;
                right: -4rem;
                top: 0;
                width: 28rem;
                height: 100%;
                background:
                    linear-gradient(135deg, rgba(20, 184, 166, 0.25), rgba(208, 138, 29, 0.16)),
                    repeating-linear-gradient(135deg, rgba(255, 250, 240, 0.20) 0 1px, transparent 1px 13px);
                transform: skewX(-12deg);
                border-radius: 8px;
            }
            .hero h1 {
                position: relative;
                z-index: 1;
                max-width: 860px;
                font-size: 3.35rem;
                line-height: 1.02;
                margin: 0.25rem 0 1rem 0;
                color: __HERO_TEXT__;
            }
            .hero-copy {
                position: relative;
                z-index: 1;
                max-width: 760px;
                color: rgba(255, 250, 240, 0.76);
                font-size: 1.08rem;
                line-height: 1.7;
            }
            .eyebrow {
                position: relative;
                z-index: 1;
                color: __HERO_EYEBROW__;
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.12em;
                margin: 0;
                text-transform: uppercase;
            }
            .notice {
                border: 1px solid rgba(15, 118, 110, 0.22);
                border-left: 4px solid var(--accent);
                background: rgba(236, 253, 245, 0.62);
                color: __NOTE_TEXT__;
                padding: 0.9rem 1rem;
                margin: 0.75rem 0 1.25rem 0;
                border-radius: 4px;
            }
            .portfolio-card, .stat-card, .contact-card, .insight-card {
                border: 1px solid rgba(216, 207, 187, 0.90);
                border-radius: 8px;
                background:
                    linear-gradient(180deg, rgba(255, 250, 240, 0.96), rgba(248, 241, 226, 0.92));
                box-shadow: var(--shadow);
            }
            .portfolio-card {
                height: 282px;
                padding: 1.2rem;
                display: flex;
                flex-direction: column;
                position: relative;
                overflow: hidden;
                transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
            }
            .portfolio-card::before {
                content: "";
                position: absolute;
                inset: 0 0 auto 0;
                height: 4px;
                background: linear-gradient(90deg, var(--accent), var(--gold), var(--accent-2));
            }
            .portfolio-card:hover, .stat-card:hover {
                border-color: rgba(20, 184, 166, 0.40);
                box-shadow: 0 26px 58px rgba(20, 26, 22, 0.16);
                transform: translateY(-3px);
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
                color: var(--status-text);
                background: rgba(204, 251, 241, 0.48);
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
            .focus-card {
                border: 1px solid var(--line);
                border-radius: 8px;
                background:
                    linear-gradient(135deg, rgba(255, 250, 240, 0.96), rgba(238, 229, 210, 0.84)),
                    var(--panel);
                box-shadow: var(--shadow);
                box-sizing: border-box;
                height: 194px;
                padding: 1rem;
                margin-bottom: 1rem;
                display: flex;
                gap: 0.85rem;
                align-items: flex-start;
                position: relative;
                transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
                overflow: hidden;
            }
            .focus-card::after {
                content: "";
                position: absolute;
                right: -2rem;
                bottom: -2.5rem;
                width: 7rem;
                height: 7rem;
                border: 1px solid rgba(20, 184, 166, 0.12);
                transform: rotate(18deg);
            }
            .focus-card:hover {
                border-color: rgba(20, 184, 166, 0.40);
                box-shadow: 0 24px 58px rgba(20, 26, 22, 0.15);
                transform: translateY(-3px);
            }
            .focus-icon {
                flex: 0 0 auto;
                width: 2.45rem;
                height: 2.45rem;
                border-radius: 8px;
                display: grid;
                place-items: center;
                background:
                    linear-gradient(135deg, rgba(20, 184, 166, 0.15), rgba(208, 138, 29, 0.12));
                border: 1px solid rgba(20, 184, 166, 0.22);
                color: var(--accent);
                box-shadow: inset 0 0 0 1px rgba(255, 250, 240, 0.55);
            }
            .focus-icon svg {
                width: 1.35rem;
                height: 1.35rem;
                stroke: currentColor;
                stroke-width: 2;
                fill: none;
                stroke-linecap: round;
                stroke-linejoin: round;
            }
            .focus-copy strong {
                display: block;
                color: var(--ink);
                font-size: 0.98rem;
                line-height: 1.25;
                min-height: 2.5rem;
                margin-bottom: 0.35rem;
            }
            .focus-copy p {
                color: var(--muted);
                line-height: 1.48;
                margin: 0;
                font-size: 0.92rem;
            }
            .contact-card {
                display: grid;
                grid-template-columns: auto 1fr auto;
                gap: 1.25rem;
                align-items: center;
                padding: 1.2rem;
                min-height: 156px;
                overflow: hidden;
            }
            .contact-avatar-wrap {
                position: relative;
                width: 7rem;
                height: 7rem;
                border-radius: 999px;
                padding: 0.25rem;
                background:
                    linear-gradient(135deg, rgba(20, 184, 166, 0.95), rgba(208, 138, 29, 0.82));
                box-shadow: 0 18px 44px rgba(20, 26, 22, 0.18);
            }
            .contact-avatar {
                width: 100%;
                height: 100%;
                border-radius: 999px;
                object-fit: cover;
                object-position: center;
                border: 3px solid rgba(255, 250, 240, 0.96);
                display: block;
            }
            .contact-copy strong {
                display: block;
                color: var(--ink);
                font-size: 1.22rem;
                line-height: 1.2;
                margin-bottom: 0.35rem;
            }
            .contact-copy p {
                color: var(--muted);
                line-height: 1.55;
                margin: 0;
                max-width: 650px;
            }
            .contact-links {
                display: grid;
                gap: 0.58rem;
                justify-items: start;
                min-width: 13rem;
            }
            .contact-links a {
                color: var(--accent);
                font-weight: 650;
                text-decoration: none;
                border-bottom: 1px solid transparent;
                width: fit-content;
            }
            .contact-links a:hover {
                border-bottom-color: rgba(15, 118, 110, 0.44);
            }
            .insight-card {
                padding: 1rem;
                margin-top: 0.5rem;
                border-left: 4px solid var(--accent);
            }
            .placeholder-panel {
                border: 1px dashed var(--placeholder-line);
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
                background:
                    linear-gradient(180deg, rgba(255, 250, 240, 0.94), rgba(246, 238, 222, 0.88));
                padding: 1.2rem;
                min-height: 100%;
                box-shadow: 0 14px 34px rgba(34, 45, 38, 0.06);
            }
            .paired-card {
                box-sizing: border-box;
                height: 318px;
                overflow: hidden;
            }
            .intro-pair-card {
                box-sizing: border-box;
                height: 210px;
                overflow: hidden;
            }
            .market-card {
                border: 1px solid var(--line);
                border-radius: 8px;
                background:
                    linear-gradient(180deg, rgba(255, 250, 240, 0.94), rgba(246, 238, 222, 0.88));
                padding: 1.2rem;
                box-sizing: border-box;
                height: 318px;
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
                color: __CHIP_TEXT__;
                font-size: 0.84rem;
                font-weight: 650;
                padding: 0.32rem 0.62rem;
            }
            .kpi-card {
                border: 1px solid rgba(222, 216, 199, 0.94);
                border-radius: 8px;
                background:
                    linear-gradient(180deg, rgba(255, 250, 240, 0.96), rgba(245, 238, 222, 0.92));
                box-shadow: var(--shadow);
                box-sizing: border-box;
                height: 158px;
                padding: 1rem 1.05rem;
                margin-top: 0.8rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                overflow: hidden;
            }
            .kpi-label {
                color: var(--muted);
                font-size: 0.78rem;
                font-weight: 760;
                letter-spacing: 0.04em;
                line-height: 1.25;
                min-height: 2rem;
                text-transform: uppercase;
            }
            .kpi-value {
                color: var(--ink);
                font-size: 1.75rem;
                font-weight: 780;
                line-height: 1.12;
                margin: 0.2rem 0 0.35rem 0;
            }
            .kpi-detail {
                color: var(--muted);
                font-size: 0.84rem;
                line-height: 1.35;
                min-height: 2.25rem;
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
                color: __NOTE_TEXT__;
            }
            div[data-testid="stExpander"] {
                border-color: var(--line);
                background: rgba(255, 253, 247, 0.76);
                box-shadow: 0 12px 30px rgba(34, 45, 38, 0.05);
            }
            div[data-testid="stPlotlyChart"] {
                border: 1px solid rgba(222, 216, 199, 0.72);
                border-radius: 8px;
                background: rgba(255, 250, 240, 0.86);
                padding: 0.35rem;
                box-shadow: 0 16px 42px rgba(20, 26, 22, 0.10);
            }
            @media (max-width: 760px) {
                .hero {
                    padding: 1.4rem;
                }
                .hero h1 {
                    font-size: 2.1rem;
                }
                .contact-card {
                    grid-template-columns: 1fr;
                    justify-items: start;
                }
                .contact-links {
                    min-width: 0;
                }
            }
        </style>
        """
        .replace("__INK__", THEME["ink"])
        .replace("__DEEP__", THEME["deep"])
        .replace("__MUTED__", THEME["muted"])
        .replace("__LINE__", THEME["line"])
        .replace("__SOFT__", THEME["soft"])
        .replace("__SOFT_MID__", THEME["soft_mid"])
        .replace("__SOFT_LIGHT__", THEME["soft_light"])
        .replace("__SIDEBAR__", THEME["sidebar"])
        .replace("__PANEL__", THEME["panel"])
        .replace("__ACCENT__", THEME["accent"])
        .replace("__ACCENT_2__", THEME["accent_2"])
        .replace("__GOLD__", THEME["gold"])
        .replace("__ROSE__", THEME["rose"])
        .replace("__STATUS_TEXT__", THEME["status_text"])
        .replace("__PLACEHOLDER_LINE__", THEME["placeholder_line"])
        .replace("__SHADOW__", THEME["shadow"])
        .replace("__SHADOW_STRONG__", THEME["shadow_strong"])
        .replace("__HERO_TEXT__", THEME["hero_text"])
        .replace("__HERO_EYEBROW__", THEME["hero_eyebrow"])
        .replace("__NOTE_TEXT__", THEME["note_text"])
        .replace("__CHIP_TEXT__", THEME["chip_text"]),
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


def render_focus_card(icon: str, title: str, body: str) -> None:
    icons = {
        "target": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"></circle><circle cx="12" cy="12" r="5"></circle><circle cx="12" cy="12" r="1.5"></circle></svg>',
        "map": '<svg viewBox="0 0 24 24"><path d="M9 18l-6 3V6l6-3 6 3 6-3v15l-6 3-6-3z"></path><path d="M9 3v15"></path><path d="M15 6v15"></path></svg>',
        "curve": '<svg viewBox="0 0 24 24"><path d="M4 19V5"></path><path d="M4 19h16"></path><path d="M8 16v-5"></path><path d="M12 16V8"></path><path d="M16 16v-7"></path><path d="M20 16v-3"></path></svg>',
        "dashboard": '<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"></rect><path d="M3 10h18"></path><path d="M9 10v10"></path><path d="M13 15h4"></path></svg>',
        "forecast": '<svg viewBox="0 0 24 24"><path d="M4 18l5-5 4 3 7-9"></path><path d="M15 7h5v5"></path><path d="M4 6v12h16"></path></svg>',
        "experiment": '<svg viewBox="0 0 24 24"><path d="M9 3h6"></path><path d="M10 3v5l-5 9a3 3 0 0 0 2.6 4.5h8.8A3 3 0 0 0 19 17l-5-9V3"></path><path d="M7 16h10"></path></svg>',
        "cluster": '<svg viewBox="0 0 24 24"><circle cx="6" cy="7" r="2.5"></circle><circle cx="16.5" cy="6.5" r="2"></circle><circle cx="17" cy="17" r="2.7"></circle><circle cx="7" cy="16" r="2"></circle><path d="M8.3 8.5l6.1 6.2"></path><path d="M8.5 15.8l6.1-7.7"></path></svg>',
        "database": '<svg viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="8" ry="3"></ellipse><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"></path><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"></path></svg>',
        "globe": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"></circle><path d="M3 12h18"></path><path d="M12 3c2.2 2.4 3.2 5.4 3.2 9S14.2 18.6 12 21"></path><path d="M12 3C9.8 5.4 8.8 8.4 8.8 12S9.8 18.6 12 21"></path></svg>',
        "mlops": '<svg viewBox="0 0 24 24"><rect x="3.5" y="4.5" width="5" height="5" rx="1"></rect><rect x="15.5" y="4.5" width="5" height="5" rx="1"></rect><rect x="9.5" y="14.5" width="5" height="5" rx="1"></rect><path d="M8.5 7h7"></path><path d="M18 9.5v2.2c0 1.5-1.2 2.8-2.8 2.8H12"></path><path d="M6 9.5v2.2c0 1.5 1.2 2.8 2.8 2.8H12"></path><path d="M16.2 17.2l1.3 1.3"></path><path d="M18.5 13.8l-1.1 1.1a2.2 2.2 0 0 0 3.1 3.1l1.1-1.1"></path></svg>',
    }
    icon_markup = icons.get(icon, html.escape(icon))
    st.markdown(
        f"""
        <div class="focus-card">
            <div class="focus-icon">{icon_markup}</div>
            <div class="focus-copy">
                <strong>{html.escape(title)}</strong>
                <p>{html.escape(body)}</p>
            </div>
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


def render_kpi_card(label: str, value: str, detail: str = "") -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{html.escape(label)}</div>
            <div class="kpi-value">{html.escape(value)}</div>
            <div class="kpi-detail">{html.escape(detail)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_contact_card(image_path: str | Path) -> None:
    image = Path(image_path)
    image_markup = ""
    if image.exists():
        encoded = base64.b64encode(image.read_bytes()).decode("ascii")
        image_markup = (
            f'<div class="contact-avatar-wrap">'
            f'<img class="contact-avatar" src="data:image/jpeg;base64,{encoded}" alt="Cody Xu" />'
            f"</div>"
        )

    st.markdown(
        f"""
        <div class="contact-card">
            {image_markup}
            <div class="contact-copy">
                <strong>Cody Xu</strong>
                <p>
                    Senior data scientist focused on marketing analytics, causal
                    measurement, dashboard systems, and decision science.
                </p>
            </div>
            <div class="contact-links">
                <a href="https://www.linkedin.com/in/codyxu94/" target="_blank">LinkedIn: codyxu94</a>
                <a href="https://github.com/Coding-Cody" target="_blank">GitHub: Coding-Cody</a>
                <a href="mailto:codyxu94@gmail.com">codyxu94@gmail.com</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
