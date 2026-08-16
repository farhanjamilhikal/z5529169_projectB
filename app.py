from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src import app_logic

st.set_page_config(
    layout="wide",
    page_title="SignalScope",
    page_icon="◈",
    initial_sidebar_state="auto",
)


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "results" / "data"
TABLES_DIR = ROOT / "results" / "tables"
REPORT_DIR = ROOT / "report"

PAGES = [
    "Overview",
    "Compare Funds",
    "Fund Fact Sheet",
    "Holdings & Allocation",
    "News Sentiment",
    "Movie-to-Market Lab",
    "Methodology & Limitations",
]

PAGE_ICONS = {
    "Overview": "◈",
    "Compare Funds": "▣",
    "Fund Fact Sheet": "◫",
    "Holdings & Allocation": "◬",
    "News Sentiment": "◭",
    "Movie-to-Market Lab": "◎",
    "Methodology & Limitations": "◇",
}

METHOD_LABELS = {
    "equal_weight": "Equal Weight",
    "min_variance": "Minimum Variance",
    "risk_parity": "Inverse-Volatility Risk Parity",
    "sentiment_tilt": "Reliability-Gated Sentiment Tilt",
}

FAMILY_DESCRIPTIONS = {
    "Equity": "50 supplied US equities using the equity trading calendar.",
    "Crypto": "10 supplied cryptocurrencies using the seven-day crypto calendar.",
    "Combined": "The equity universe plus the supplied crypto sleeve on the shared equity decision calendar.",
}

SECTOR_DISPLAY_NAMES = {
    "Comm": "Comm (Communication / Telecom)",
    "Consumer": "Consumer",
    "Energy": "Energy",
    "Financials": "Financials",
    "Healthcare": "Healthcare",
    "Industrials": "Industrials",
    "Materials": "Materials",
    "RealEstate": "Real Estate",
    "Tech": "Tech",
    "Utilities": "Utilities",
}

REQUIRED_ARTIFACTS = {
    "performance_metrics": TABLES_DIR / "performance_metrics.csv",
    "fund_returns": DATA_DIR / "fund_returns.csv",
    "fund_weights": DATA_DIR / "fund_weights.csv",
    "current_holdings": TABLES_DIR / "current_holdings.csv",
    "sector_sentiment_index": DATA_DIR / "sector_sentiment_index.csv",
    "sentiment_validation": TABLES_DIR / "sentiment_validation.csv",
    "dual_domain_validation": TABLES_DIR / "dual_domain_sentiment_validation.csv",
    "finance_validation_metrics": TABLES_DIR / "finance_validation_metrics.csv",
    "finance_confusion_matrix": TABLES_DIR / "finance_confusion_matrix.csv",
    "finance_lexicon": TABLES_DIR / "finance_lexicon_extension.csv",
    "sector_lexicon": TABLES_DIR / "sector_sentiment_lexicon.csv",
    "model_specification": TABLES_DIR / "model_specification.csv",
    "asset_data_use_register": TABLES_DIR / "asset_data_use_register.csv",
    "carried_forward_integrity_audit": TABLES_DIR / "carried_forward_integrity_audit.csv",
    "product_feasibility_scorecard": TABLES_DIR / "product_feasibility_scorecard.csv",
    "risk_mitigation_register": TABLES_DIR / "risk_mitigation_register.csv",
    "sentiment_product_app_checks": TABLES_DIR / "sentiment_product_app_checks.csv",
    "fusion_comparison": TABLES_DIR / "fusion_comparison.csv",
    "movie_lab_event_summary": TABLES_DIR / "movie_lab_event_summary.csv",
    "movie_lab_event_windows": DATA_DIR / "movie_lab_event_windows.csv",
    "movie_lab_external_prices": DATA_DIR / "movie_lab_external_prices_2020_2023.csv",
    "movie_lab_exposure_register": TABLES_DIR / "movie_lab_exposure_register.csv",
    "movie_lab_imdb_ratings": TABLES_DIR / "movie_lab_imdb_aggregate_ratings.csv",
    "movie_lab_sources": TABLES_DIR / "spiderman_barbie_research_sources.csv",
    "movie_lab_gap_closure": TABLES_DIR / "spiderman_barbie_gap_closure.csv",
}

BRAND = "SignalScope"
TAGLINE = "See risk, returns and sentiment in one view."
LONG_DESCRIPTION = (
    "Transparent systematic fund comparison with news-sentiment evidence and "
    "a Movie-to-Market Lab."
)
ACADEMIC_BANNER = (
    "Academic research prototype • Historical 2020-2023 course data • "
    "Backtested and descriptive evidence • Not personal financial advice."
)
MOVIE_TITLE = "Movie-to-Market Lab: Spider-Man versus Barbie"
PUBLIC_REPOSITORY_URL = "https://github.com/farhanjamilhikal/z5529169_projectB"

PALETTE = {
    # Deep navy, matching the report cover's chromatic gradient (blue/purple/magenta glow on near-black).
    "bg": "#080B14",
    "bg_alt": "#0E1120",
    "panel": "#141A30",
    "panel_soft": "#1B2340",
    "border": "#333D63",
    "text": "#F5F7FF",
    "muted": "#AEB4D6",
    # Chart/UI accents (vivid chromatic palette, matching the report cover).
    "pink": "#E23E8C",
    "cyan": "#3E9BFF",
    "purple": "#8B5CF6",
    "positive": "#3DDC97",
    "negative": "#FF5C7A",
    "warning": "#F0B93D",
}


def accent(name: str, dark_mode: bool = True) -> str:
    """SignalScope's chart/UI accent colour. The app is dark-theme only; `dark_mode` is kept for call-site compatibility."""
    return PALETTE[name]


def required_artifact_paths(root: Path = ROOT) -> dict[str, Path]:
    return {
        name: (root / path.relative_to(ROOT) if path.is_absolute() else root / path)
        for name, path in REQUIRED_ARTIFACTS.items()
    }


def missing_required_files(root: Path = ROOT) -> list[Path]:
    return [path for path in required_artifact_paths(root).values() if not path.exists()]


def fmt_pct(value: float | int | str | None, *, signed: bool = False) -> str:
    if value is None or pd.isna(value):
        return "—"
    number = float(value)
    return f"{number:+.2%}" if signed else f"{number:.2%}"


def fmt_ratio(value: float | int | str | None) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):.2f}"


def fmt_date(value: str | pd.Timestamp | None) -> str:
    if value is None or pd.isna(value):
        return "—"
    return pd.to_datetime(value).strftime("%d %b %Y")


def fmt_count(value: float | int | str | None) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{int(float(value)):,}"


def classify_ticker(ticker: str) -> str:
    return "Crypto" if ticker.endswith("-USD") else "Equity"


def inject_css(dark_mode: bool = True) -> None:
    bg = PALETTE["bg"]
    bg_alt = PALETTE["bg_alt"]
    panel = PALETTE["panel"]
    panel_soft = PALETTE["panel_soft"]
    border = PALETTE["border"]
    text = PALETTE["text"]
    muted = PALETTE["muted"]
    panel_accent = PALETTE["text"]
    shadow = "0 10px 24px rgba(8, 19, 28, 0.24)"
    sidebar_bg = PALETTE["bg_alt"]
    sidebar_text = PALETTE["text"]
    st.markdown(
        f"""
        <style>
        :root {{
            --bg: {bg};
            --bg-alt: {bg_alt};
            --panel: {panel};
            --panel-soft: {panel_soft};
            --border: {border};
            --text: {text};
            --muted: {muted};
            --panel-accent: {panel_accent};
            --oxblood: {accent("pink", dark_mode)};
            --blue: {accent("cyan", dark_mode)};
            --brick: {accent("purple", dark_mode)};
            --positive: {accent("positive", dark_mode)};
            --negative: {accent("negative", dark_mode)};
            --warning: {accent("warning", dark_mode)};
            --shadow: {shadow};
            --radius: 18px;
            --content-width: 1280px;
        }}
        html, body, [class*="css"] {{
            font-family: "Inter", "Segoe UI", sans-serif;
        }}
        body {{
            color: var(--text);
        }}
        .stApp {{
            color: var(--text);
            background: var(--bg);
        }}
        [data-testid="stAppViewContainer"] > .main {{
            background: transparent;
        }}
        [data-testid="stHeader"] {{
            background: var(--bg) !important;
        }}
        #MainMenu, footer {{
            visibility: hidden;
        }}
        .block-container {{
            padding-top: 1.1rem !important;
            padding-bottom: 2.5rem !important;
            max-width: var(--content-width);
        }}
        [data-testid="stSidebar"] {{
            background: {sidebar_bg};
            border-right: 1px solid var(--border);
            width: 19rem !important;
        }}
        [data-testid="stSidebar"] * {{
            color: {sidebar_text} !important;
        }}
        [data-testid="stSidebarCollapseButton"] button {{
            color: {sidebar_text} !important;
        }}
        .signal-banner {{
            margin: 0 0 1rem 0;
            padding: 0.9rem 1rem;
            border-radius: 14px;
            border: 1px solid var(--border);
            border-left: 5px solid var(--oxblood);
            background: var(--panel-soft);
            color: var(--text);
            font-weight: 650;
            box-shadow: var(--shadow);
        }}
        .hero-card, .panel-card, .info-card, .badge-card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
        }}
        .hero-card {{
            padding: 1.35rem 1.35rem 1.2rem 1.35rem;
            min-height: 164px;
        }}
        .panel-card {{
            padding: 1rem 1.05rem;
            height: 100%;
            box-sizing: border-box;
        }}
        .info-card {{
            padding: 0.95rem 1rem;
            height: 100%;
        }}
        .badge-card {{
            display: inline-flex;
            gap: 0.4rem;
            align-items: center;
            padding: 0.42rem 0.72rem;
            font-size: 0.86rem;
            font-weight: 700;
            color: var(--text);
        }}
        .eyebrow {{
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.11em;
            font-size: 0.78rem;
            margin-bottom: 0.45rem;
        }}
        .hero-title {{
            font-size: clamp(1.95rem, 3vw, 2.6rem);
            font-weight: 850;
            line-height: 1.05;
            color: var(--text);
            margin: 0 0 0.55rem 0;
        }}
        .hero-subtitle {{
            color: var(--muted);
            font-size: clamp(0.96rem, 1.5vw, 1.04rem);
            max-width: 56rem;
        }}
        .section-title {{
            color: var(--text);
            font-weight: 760;
            font-size: clamp(1.02rem, 1.8vw, 1.18rem);
            margin-bottom: 0.7rem;
        }}
        .section-copy, .helper-text {{
            color: var(--muted);
            font-size: clamp(0.9rem, 1.3vw, 0.97rem);
            line-height: 1.55;
        }}
        .pill-row {{
            display: flex;
            gap: 0.45rem;
            flex-wrap: wrap;
            margin-top: 0.6rem;
        }}
        .pill {{
            background: var(--panel-soft);
            border: 1px solid var(--border);
            color: var(--text);
            border-radius: 999px;
            padding: 0.38rem 0.72rem;
            font-size: 0.82rem;
        }}
        .warning-note {{
            border-left: 4px solid var(--warning);
            padding: 0.9rem 1rem;
            border-radius: 12px;
            background: rgba(255,183,3,0.12);
            color: var(--text);
        }}
        .secondary-badge {{
            display: inline-block;
            border-radius: 999px;
            padding: 0.25rem 0.7rem;
            background: var(--panel-soft);
            border: 1px solid var(--oxblood);
            color: var(--text);
            font-size: 0.82rem;
            font-weight: 700;
        }}
        .positive-text {{ color: var(--positive); font-weight: 700; }}
        .negative-text {{ color: var(--negative); font-weight: 700; }}
        .nav-label {{
            font-size: 0.95rem;
            font-weight: 700;
        }}
        [data-testid="stMetric"] {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 0.95rem 1rem;
            box-shadow: var(--shadow);
        }}
        [data-testid="stMetricLabel"] p {{
            color: var(--muted) !important;
            font-size: 0.84rem;
        }}
        [data-testid="stMetricValue"] div {{
            color: var(--text) !important;
            font-size: clamp(1.35rem, 2vw, 1.75rem);
        }}
        [data-testid="stMetricDelta"] div {{
            font-size: 0.88rem;
        }}
        .stButton > button, .stDownloadButton > button, .stLinkButton > a {{
            min-height: 44px;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.16);
            background: var(--oxblood) !important;
            color: #ffffff !important;
            font-weight: 750;
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.16);
        }}
        .stButton > button:hover, .stDownloadButton > button:hover, .stLinkButton > a:hover {{
            border-color: rgba(255,255,255,0.28);
            color: #ffffff !important;
        }}
        .stButton > button p, .stDownloadButton > button p, .stLinkButton > a p,
        .stButton > button span, .stDownloadButton > button span, .stLinkButton > a span {{
            color: #ffffff !important;
        }}
        .stTextInput input, .stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div {{
            background: var(--panel-soft) !important;
            color: var(--text) !important;
            border-radius: 12px !important;
            border: 1px solid var(--border) !important;
        }}
        [data-baseweb="popover"], [data-baseweb="menu"], ul[role="listbox"] {{
            background: var(--panel-soft) !important;
        }}
        [data-baseweb="popover"] li, [data-baseweb="menu"] li, ul[role="listbox"] li,
        li[role="option"], [data-baseweb="popover"] *, [data-baseweb="menu"] * {{
            background: var(--panel-soft) !important;
            color: var(--text) !important;
        }}
        li[role="option"][aria-selected="true"], li[role="option"]:hover {{
            background: var(--border) !important;
        }}
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea,
        [data-baseweb="select"] span,
        [data-baseweb="select"] input {{
            color: var(--panel-accent) !important;
            -webkit-text-fill-color: var(--panel-accent) !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }}
        code, [data-testid="stSidebar"] code {{
            color: var(--blue) !important;
            -webkit-text-fill-color: var(--blue) !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }}
        div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] li, label, .stCaption {{
            color: var(--text);
        }}
        [data-baseweb="tag"] {{
            background: var(--panel-soft) !important;
            color: var(--text) !important;
        }}
        div[role="radiogroup"] > label {{
            background: var(--panel-soft);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 0.42rem 0.5rem;
            margin-bottom: 0.45rem;
        }}
        div[role="radiogroup"] > label:hover {{
            border-color: var(--blue);
        }}
        div[role="radiogroup"] label p {{
            font-size: 0.95rem;
            font-weight: 700;
        }}
        [data-testid="stDataFrame"] {{
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        [data-testid="stExpander"] {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            overflow: hidden;
            margin-bottom: 0.75rem;
        }}
        [data-testid="stExpander"] summary {{
            padding: 0.75rem 1rem;
            font-weight: 700;
            color: var(--text);
        }}
        [data-testid="stExpander"] summary:hover {{
            color: var(--oxblood);
        }}
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
            padding: 0 1rem 1rem;
        }}
        .plotly-chart {{
            border-radius: 16px;
            max-width: 100%;
            overflow-x: auto;
        }}
        [data-testid="stHorizontalBlock"] {{
            min-width: 0;
            align-items: stretch;
        }}
        [data-testid="stColumn"] {{
            min-width: 0;
            display: flex;
            flex-direction: column;
        }}
        [data-testid="stColumn"] > div {{
            display: flex;
            flex-direction: column;
            flex: 1;
        }}
        [data-testid="stColumn"] [data-testid="stMarkdownContainer"] {{
            display: flex;
            flex-direction: column;
            flex: 1;
        }}
        [data-testid="stColumn"] [data-testid="stMarkdownContainer"] > div {{
            flex: 1;
        }}
        @media (max-width: 1024px) {{
            .block-container {{
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }}
        }}
        @media (max-width: 820px) {{
            .block-container {{
                padding: 0.8rem 0.75rem 2rem !important;
            }}
            .hero-card {{
                min-height: auto;
                padding: 1rem;
            }}
            .signal-banner {{
                font-size: 0.82rem;
                padding: 0.7rem 0.8rem;
            }}
            [data-testid="stHorizontalBlock"] {{
                flex-wrap: wrap;
                gap: 0.75rem !important;
            }}
            [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
                flex: 1 1 100% !important;
                width: 100% !important;
                min-width: 100% !important;
            }}
            [data-testid="stSidebar"] {{
                max-width: 88vw;
            }}
            .stButton > button, .stDownloadButton > button {{
                width: 100%;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def set_query_state(page: str, dark_mode: bool = True) -> None:
    st.query_params["page"] = page


def initialise_state() -> tuple[str, bool]:
    params = st.query_params
    initial_page = params.get("page", PAGES[0])
    if isinstance(initial_page, list):
        initial_page = initial_page[0]
    if initial_page not in PAGES:
        initial_page = PAGES[0]
    st.session_state.setdefault("page", initial_page)
    st.session_state.setdefault("dark_mode", True)
    return st.session_state["page"], st.session_state["dark_mode"]


@st.cache_data(show_spinner=False)
def load_artifacts() -> dict[str, pd.DataFrame]:
    missing = missing_required_files(ROOT)
    if missing:
        raise FileNotFoundError(
            "Missing required result files: " + ", ".join(path.name for path in missing)
        )

    data: dict[str, pd.DataFrame] = {
        "performance_metrics": pd.read_csv(REQUIRED_ARTIFACTS["performance_metrics"]),
        "fund_returns": pd.read_csv(REQUIRED_ARTIFACTS["fund_returns"], parse_dates=["date"]),
        "fund_weights": pd.read_csv(REQUIRED_ARTIFACTS["fund_weights"], parse_dates=["date"]),
        "current_holdings": pd.read_csv(REQUIRED_ARTIFACTS["current_holdings"], parse_dates=["date"]),
        "sector_sentiment_index": pd.read_csv(REQUIRED_ARTIFACTS["sector_sentiment_index"], parse_dates=["date"]),
        "sentiment_validation": pd.read_csv(REQUIRED_ARTIFACTS["sentiment_validation"]),
        "dual_domain_validation": pd.read_csv(REQUIRED_ARTIFACTS["dual_domain_validation"]),
        "finance_validation_metrics": pd.read_csv(
            REQUIRED_ARTIFACTS["finance_validation_metrics"]
        ),
        "finance_confusion_matrix": pd.read_csv(
            REQUIRED_ARTIFACTS["finance_confusion_matrix"]
        ),
        "finance_lexicon": pd.read_csv(REQUIRED_ARTIFACTS["finance_lexicon"]),
        "sector_lexicon": pd.read_csv(REQUIRED_ARTIFACTS["sector_lexicon"]),
        "model_specification": pd.read_csv(REQUIRED_ARTIFACTS["model_specification"]),
        "asset_data_use_register": pd.read_csv(REQUIRED_ARTIFACTS["asset_data_use_register"]),
        "carried_forward_integrity_audit": pd.read_csv(REQUIRED_ARTIFACTS["carried_forward_integrity_audit"]),
        "product_feasibility_scorecard": pd.read_csv(REQUIRED_ARTIFACTS["product_feasibility_scorecard"]),
        "risk_mitigation_register": pd.read_csv(REQUIRED_ARTIFACTS["risk_mitigation_register"]),
        "sentiment_product_app_checks": pd.read_csv(REQUIRED_ARTIFACTS["sentiment_product_app_checks"]),
        "fusion_comparison": pd.read_csv(REQUIRED_ARTIFACTS["fusion_comparison"]),
        "movie_lab_event_summary": pd.read_csv(
            REQUIRED_ARTIFACTS["movie_lab_event_summary"],
            parse_dates=["event_date", "mapped_trading_date", "window_start", "window_end"],
        ),
        "movie_lab_event_windows": pd.read_csv(
            REQUIRED_ARTIFACTS["movie_lab_event_windows"],
            parse_dates=["date", "announced_event_date"],
        ),
        "movie_lab_external_prices": pd.read_csv(
            REQUIRED_ARTIFACTS["movie_lab_external_prices"],
            parse_dates=["date"],
        ),
        "movie_lab_exposure_register": pd.read_csv(REQUIRED_ARTIFACTS["movie_lab_exposure_register"]),
        "movie_lab_imdb_ratings": pd.read_csv(REQUIRED_ARTIFACTS["movie_lab_imdb_ratings"]),
        "movie_lab_sources": pd.read_csv(REQUIRED_ARTIFACTS["movie_lab_sources"]),
        "movie_lab_gap_closure": pd.read_csv(REQUIRED_ARTIFACTS["movie_lab_gap_closure"]),
    }
    return data


@st.cache_data(show_spinner=False)
def load_support_texts() -> dict[str, str]:
    return {
        "student_finalisation": (ROOT / "STUDENT_FINALISATION_REQUIRED.md").read_text(encoding="utf-8"),
        "citation_verification": (ROOT / "CITATION_VERIFICATION.md").read_text(encoding="utf-8"),
        "gap_closure": (ROOT / "student_review" / "SPIDERMAN_BARBIE_GAP_CLOSURE.md").read_text(encoding="utf-8"),
    }


def render_banner_and_header() -> None:
    st.markdown(f'<div class="signal-banner">{ACADEMIC_BANNER}</div>', unsafe_allow_html=True)
    st.title(BRAND)
    st.caption(TAGLINE)
    st.markdown(
        f"""
        <div class="hero-card" style="margin-bottom:1rem;">
            <div class="eyebrow">{BRAND}</div>
            <div class="hero-title">{LONG_DESCRIPTION}</div>
            <div class="hero-subtitle">{TAGLINE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_navigation(current_page: str, dark_mode: bool = True) -> tuple[str, bool]:
    with st.sidebar:
        st.markdown(f"## {BRAND}")
        st.caption(TAGLINE)
        selected_page = st.radio(
            "Navigation",
            PAGES,
            index=PAGES.index(current_page),
            format_func=lambda page: f"{PAGE_ICONS[page]}  {page}",
            help="Open every required SignalScope page from this navigation list.",
        )
        st.markdown("---")
        st.caption("Public source repository; app reads verified `results/` artefacts only.")
        st.link_button("View public GitHub repository", PUBLIC_REPOSITORY_URL)
    return selected_page, dark_mode


def theme_colors(dark_mode: bool = True) -> dict[str, str]:
    return {
        "paper": "rgba(0,0,0,0)",
        "plot": "rgba(0,0,0,0)",
        "text": PALETTE["text"],
        "muted": PALETTE["muted"],
        "grid": "rgba(255,255,255,0.14)",
        "cyan": accent("cyan", dark_mode),
        "pink": accent("pink", dark_mode),
        "purple": accent("purple", dark_mode),
        "positive": accent("positive", dark_mode),
        "negative": accent("negative", dark_mode),
    }


def add_plot_layout(fig: go.Figure, dark_mode: bool = True, *, height: int = 420) -> go.Figure:
    colors = theme_colors(dark_mode)
    annotation_color = "#FFFFFF"
    fig.update_layout(
        paper_bgcolor=colors["paper"],
        plot_bgcolor=colors["plot"],
        font=dict(color=colors["text"], size=12),
        margin=dict(l=64, r=28, t=24, b=64),
        height=height,
        legend=dict(
            orientation="h",
            y=-0.28,
            x=0,
            font=dict(size=11),
            itemsizing="constant",
        ),
        xaxis=dict(
            gridcolor=colors["grid"],
            zeroline=False,
            automargin=True,
            title_font=dict(size=13),
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            gridcolor=colors["grid"],
            zeroline=False,
            automargin=True,
            title_font=dict(size=13),
            tickfont=dict(size=11),
        ),
        hoverlabel=dict(
            bgcolor=PALETTE["bg"],
            font_color=colors["text"],
            font_size=12,
        ),
    )
    fig.update_annotations(
        font=dict(color=annotation_color, size=12),
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)",
    )
    fig.update_traces(
        textfont=dict(color=annotation_color, size=11),
    )
    return fig


def growth_chart(
    fund_returns: pd.DataFrame,
    funds: Iterable[str],
    dark_mode: bool,
    *,
    height: int = 360,
) -> go.Figure:
    selected = list(funds)
    frame = (
        fund_returns[fund_returns["fund"].isin(selected)][["date", "fund", "growth_of_1"]]
        .sort_values("date")
        .pivot(index="date", columns="fund", values="growth_of_1")
    )
    colors = [accent("cyan", dark_mode), accent("pink", dark_mode), accent("purple", dark_mode), accent("positive", dark_mode), "#A78BFA"]
    fig = go.Figure()
    for index, fund in enumerate(frame.columns):
        fig.add_trace(
            go.Scatter(
                x=frame.index,
                y=frame[fund],
                mode="lines",
                name=fund,
                line=dict(width=2.5 if index == 0 else 2.0, color=colors[index % len(colors)]),
            )
        )
    fig.update_yaxes(title="Growth of $1")
    fig.update_xaxes(title="Live out-of-sample date")
    return add_plot_layout(fig, dark_mode, height=height)


def drawdown_chart(
    fund_returns: pd.DataFrame,
    funds: Iterable[str],
    dark_mode: bool,
    *,
    height: int = 340,
) -> go.Figure:
    selected = list(funds)
    frame = (
        fund_returns[fund_returns["fund"].isin(selected)][["date", "fund", "drawdown"]]
        .sort_values("date")
        .pivot(index="date", columns="fund", values="drawdown")
    )
    fig = go.Figure()
    palette = [accent("pink", dark_mode), accent("cyan", dark_mode), accent("purple", dark_mode), accent("positive", dark_mode)]
    for index, fund in enumerate(frame.columns):
        fig.add_trace(
            go.Scatter(
                x=frame.index,
                y=frame[fund],
                mode="lines",
                name=fund,
                line=dict(width=2.0, color=palette[index % len(palette)]),
            )
        )
    fig.update_yaxes(title="Drawdown")
    fig.update_xaxes(title="Live out-of-sample date")
    return add_plot_layout(fig, dark_mode, height=height)


def risk_return_chart(
    metrics: pd.DataFrame,
    dark_mode: bool,
    *,
    height: int = 420,
    x_range: tuple[float, float] | None = None,
    y_range: tuple[float, float] | None = None,
) -> go.Figure:
    colors = {"Equity": accent("cyan", dark_mode), "Crypto": accent("pink", dark_mode), "Combined": accent("purple", dark_mode)}
    fig = go.Figure()
    for family, group in metrics.groupby("family"):
        fig.add_trace(
            go.Scatter(
                x=group["annualised_volatility"] * 100,
                y=group["annualised_return"] * 100,
                mode="markers",
                text=group["fund"],
                name=family,
                marker=dict(
                    size=9,
                    color=colors.get(family, accent("cyan", dark_mode)),
                    opacity=0.78,
                    line=dict(
                        color=PALETTE["bg"],
                        width=1,
                    ),
                ),
                hovertemplate=(
                    "<b>%{text}</b><br>Volatility: %{x:.2f}%<br>Return: %{y:.2f}%"
                    "<br>Sharpe: %{customdata:.2f}<extra></extra>"
                ),
                customdata=group["sharpe_ratio"],
            )
        )
    fig.update_xaxes(title="Annualised volatility (%)")
    fig.update_yaxes(title="Annualised return (%)")
    if x_range is not None:
        fig.update_xaxes(range=list(x_range), dtick=2)
    if y_range is not None:
        fig.update_yaxes(range=list(y_range), dtick=2 if y_range[1] <= 25 else 5)
    return add_plot_layout(fig, dark_mode, height=height)


def render_risk_return_zoom_views(
    metrics: pd.DataFrame,
    dark_mode: bool,
) -> None:
    """Render readable full-width detail views without permanent point labels."""
    clusters = [
        (
            "Lower-volatility detail",
            metrics.loc[metrics["family"] != "Crypto"].copy(),
            (10, 23),
            (4, 17),
            "Equity and combined funds are separated here because the full-universe scale compresses them.",
        ),
        (
            "Higher-volatility cryptocurrency detail",
            metrics.loc[metrics["family"] == "Crypto"].copy(),
            (68, 83),
            (30, 63),
            "Crypto funds remain on their native high-risk scale; hover over a marker for its full name.",
        ),
    ]
    for heading, cluster, x_range, y_range, explanation in clusters:
        if cluster.empty:
            continue
        with st.expander(heading, expanded=False):
            st.caption(explanation)
            st.plotly_chart(
                risk_return_chart(
                    cluster,
                    dark_mode,
                    height=430,
                    x_range=x_range,
                    y_range=y_range,
                ),
                width="stretch",
            )
            detail = cluster[
                ["fund", "annualised_volatility", "annualised_return", "sharpe_ratio"]
            ].copy()
            detail["annualised_volatility"] = detail["annualised_volatility"].map(fmt_pct)
            detail["annualised_return"] = detail["annualised_return"].map(fmt_pct)
            detail["sharpe_ratio"] = detail["sharpe_ratio"].map(fmt_ratio)
            st.dataframe(
                detail.rename(
                    columns={
                        "fund": "Fund",
                        "annualised_volatility": "Volatility",
                        "annualised_return": "Return",
                        "sharpe_ratio": "Sharpe ratio",
                    }
                ),
                width="stretch",
                hide_index=True,
            )


def holdings_bar_chart(holdings: pd.DataFrame, dark_mode: bool, *, height: int = 430) -> go.Figure:
    plot = holdings.copy()
    if len(plot) > 12:
        top = plot.head(11).copy()
        other_weight = plot.iloc[11:]["weight"].sum()
        top = pd.concat(
            [top, pd.DataFrame([{"ticker": "Other", "weight": other_weight}])],
            ignore_index=True,
        )
        plot = top
    fig = go.Figure(
        go.Bar(
            x=plot["weight"] * 100,
            y=plot["ticker"],
            orientation="h",
            marker=dict(color=accent("cyan", dark_mode)),
            text=[f"{weight:.2%}" for weight in plot["weight"]],
            textposition="outside",
        )
    )
    fig.update_xaxes(title="Portfolio weight (%)")
    fig.update_yaxes(title="", autorange="reversed")
    return add_plot_layout(fig, dark_mode, height=height)


def sector_sentiment_chart(
    sector_index: pd.DataFrame,
    selected_sectors: list[str],
    dark_mode: bool,
    *,
    window: int,
    sentiment_column: str = "sentiment",
    height: int = 360,
) -> go.Figure:
    plot = sector_index[sector_index["sector"].isin(selected_sectors)].copy().sort_values(["sector", "date"])
    plot["smoothed"] = plot.groupby("sector")[sentiment_column].transform(
        lambda series: series.rolling(window, min_periods=1).mean()
    )
    fig = go.Figure()
    palette = [accent("cyan", dark_mode), accent("pink", dark_mode), accent("purple", dark_mode), accent("positive", dark_mode), "#A78BFA"]
    for index, (sector, group) in enumerate(plot.groupby("sector")):
        fig.add_trace(
            go.Scatter(
                x=group["date"],
                y=group["smoothed"],
                mode="lines",
                name=sector,
                line=dict(width=2.0, color=palette[index % len(palette)]),
            )
        )
    fig.update_yaxes(title="Sentiment score")
    fig.update_xaxes(title="Date")
    return add_plot_layout(fig, dark_mode, height=height)


def coverage_chart(
    sector_index: pd.DataFrame,
    selected_sectors: list[str],
    dark_mode: bool,
    *,
    window: int,
    column: str,
    title: str,
    height: int = 320,
) -> go.Figure:
    plot = sector_index[sector_index["sector"].isin(selected_sectors)].copy().sort_values(["sector", "date"])
    plot["smoothed"] = plot.groupby("sector")[column].transform(
        lambda series: series.rolling(window, min_periods=1).mean()
    )
    fig = go.Figure()
    palette = [accent("purple", dark_mode), accent("cyan", dark_mode), accent("pink", dark_mode), accent("positive", dark_mode), "#A78BFA"]
    for index, (sector, group) in enumerate(plot.groupby("sector")):
        fig.add_trace(
            go.Scatter(
                x=group["date"],
                y=group["smoothed"],
                mode="lines",
                name=sector,
                line=dict(width=2.0, color=palette[index % len(palette)]),
            )
        )
    fig.update_yaxes(title=title)
    fig.update_xaxes(title="Date")
    return add_plot_layout(fig, dark_mode, height=height)


def movie_event_window_chart(
    event_summary_row: pd.Series,
    external_prices: pd.DataFrame,
    dark_mode: bool,
) -> go.Figure:
    tickers = [event_summary_row["primary_ticker"], "SPY"]
    if event_summary_row["film"] == "Spider-Man: No Way Home":
        tickers.append("DIS")
    if event_summary_row["film"] == "Barbie":
        tickers.append("WBD")
    plot = external_prices[
        (external_prices["ticker"].isin(tickers))
        & (external_prices["date"] >= event_summary_row["window_start"])
        & (external_prices["date"] <= event_summary_row["window_end"])
    ].copy()
    plot["rebased"] = plot.groupby("ticker")["adjClose"].transform(lambda series: series / series.iloc[0])
    fig = go.Figure()
    palette = {
        event_summary_row["primary_ticker"]: accent("pink", dark_mode),
        "SPY": accent("cyan", dark_mode),
        "DIS": accent("purple", dark_mode),
        "WBD": accent("purple", dark_mode),
    }
    for ticker, group in plot.groupby("ticker"):
        fig.add_trace(
            go.Scatter(
                x=group["date"],
                y=group["rebased"],
                mode="lines+markers",
                name=ticker,
                line=dict(width=2.5 if ticker == event_summary_row["primary_ticker"] else 1.9, color=palette.get(ticker, accent("cyan", dark_mode))),
            )
        )
    fig.add_vline(
        x=event_summary_row["mapped_trading_date"],
        line_dash="dash",
        line_color=accent("warning", dark_mode),
        annotation_text="Mapped event day",
        annotation_position="top right",
    )
    fig.update_yaxes(title="Rebased adjusted close")
    fig.update_xaxes(title="Trading date")
    return add_plot_layout(fig, dark_mode, height=390)


def latest_holdings_for_fund(current_holdings: pd.DataFrame, fund: str) -> pd.DataFrame:
    return (
        current_holdings[current_holdings["fund"] == fund]
        .sort_values("weight", ascending=False)
        .reset_index(drop=True)
    )


def top_five_concentration(holdings: pd.DataFrame) -> float:
    return float(holdings.head(5)["weight"].sum())


def asset_family_exposure(holdings: pd.DataFrame) -> pd.DataFrame:
    frame = holdings.copy()
    frame["asset_family"] = frame["ticker"].map(classify_ticker)
    return frame.groupby("asset_family", as_index=False)["weight"].sum().sort_values("weight", ascending=False)


def allocation_builder(
    metrics: pd.DataFrame,
    fund_returns: pd.DataFrame,
    dark_mode: bool,
) -> None:
    st.markdown('<div class="section-title">Hypothetical allocation across the ten offered funds</div>', unsafe_allow_html=True)
    st.caption(
        "This scenario combines the offered funds using their verified historical net-return series. "
        "It is a user-defined educational overlay, not a live account or execution workflow."
    )
    funds = sorted(metrics["fund"].tolist())
    default = [fund for fund in ["Combined Risk Parity", "Equity Equal Weight", "Crypto Minimum Variance"] if fund in funds]
    chosen = st.multiselect(
        "Select two to five funds",
        funds,
        default=default,
        max_selections=5,
        help="The allocation builder uses only the ten verified offered funds.",
    )
    if len(chosen) < 2:
        st.info("Select at least two funds to create a hypothetical allocation.")
        return

    raw_weights: dict[str, int] = {}
    columns = st.columns(len(chosen))
    for column, fund in zip(columns, chosen, strict=False):
        raw_weights[fund] = column.slider(
            fund,
            min_value=0,
            max_value=100,
            value=max(5, int(100 / len(chosen))),
            step=5,
            help="Weights are normalised to sum to 100%.",
        )
    total = sum(raw_weights.values())
    if total == 0:
        st.warning("At least one selected fund must have a non-zero allocation.")
        return
    allocations = {fund: weight / total for fund, weight in raw_weights.items() if weight > 0}
    contributions, series = app_logic.allocation_series(fund_returns, allocations)
    selected_families = set(
        metrics.loc[metrics["fund"].isin(allocations), "family"]
    )
    periods_per_year = 365 if selected_families == {"Crypto"} else 252
    allocation_metrics = app_logic.allocation_metrics(series, periods_per_year)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Annualised return", fmt_pct(allocation_metrics["Return"]))
    m2.metric("Annualised volatility", fmt_pct(allocation_metrics["Volatility"]))
    m3.metric("Sharpe ratio", fmt_ratio(allocation_metrics["Sharpe"]))
    m4.metric("Maximum drawdown", fmt_pct(allocation_metrics["Max drawdown"]))

    growth = (1.0 + series).cumprod().rename("Allocation growth")
    drawdown = growth / growth.cummax() - 1.0
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=growth.index, y=growth, mode="lines", name="Growth of $1", line=dict(color=accent("cyan", dark_mode), width=2.6)))
    fig.add_trace(go.Scatter(x=drawdown.index, y=drawdown, mode="lines", name="Drawdown", line=dict(color=accent("pink", dark_mode), width=2.0), yaxis="y2"))
    fig.update_layout(
        yaxis=dict(title="Growth of $1", gridcolor=theme_colors(dark_mode)["grid"]),
        yaxis2=dict(title="Drawdown", overlaying="y", side="right", gridcolor=theme_colors(dark_mode)["grid"]),
        xaxis=dict(title="Date", gridcolor=theme_colors(dark_mode)["grid"]),
        legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(add_plot_layout(fig, dark_mode, height=360), width="stretch")
    audit = app_logic.allocation_export(contributions, series)
    st.download_button(
        "Download allocation audit CSV",
        data=audit.to_csv(index=False).encode("utf-8"),
        file_name="signalscope_allocation_audit.csv",
        mime="text/csv",
        help="Download date-level fund contributions, portfolio return, growth and drawdown.",
    )
    st.caption(
        f"Annualisation uses {periods_per_year} periods because the scenario "
        + ("contains only crypto funds." if periods_per_year == 365 else "uses the equity decision calendar.")
    )
    st.warning(
        "Duplicate underlying exposures are likely because the offered funds share many of the same assets. "
        "This page does not claim holdings-overlap percentages and does not simulate live trading."
    )


def render_overview(data: dict[str, pd.DataFrame], dark_mode: bool) -> None:
    st.subheader("Overview")
    metrics = data["performance_metrics"].copy()
    fund_returns = data["fund_returns"].copy()
    selected_fund = st.selectbox(
        "Selected fund",
        metrics["fund"].tolist(),
        index=metrics["fund"].tolist().index("Combined Risk Parity"),
        help="Choose a fund to anchor the overview cards while the charts show the wider menu.",
    )
    selected_row = metrics.loc[metrics["fund"] == selected_fund].iloc[0]

    left, right = st.columns([1.45, 1], gap="large")
    with left:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-title">What SignalScope is showing</div>
                <div class="section-copy">
                    SignalScope compares the ten verified Project B funds, the headline-sentiment overlay,
                    and the separate Movie-to-Market Lab without presenting the prototype as a live brokerage
                    or a production-ready investment service.
                </div>
                <div class="pill-row">
                    <span class="pill">2020-2023 official course boundary</span>
                    <span class="pill">10 offered funds</span>
                    <span class="pill">Monthly walk-forward rebalancing</span>
                    <span class="pill">10 bps turnover cost</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-title">Flagship balanced reference</div>
                <div class="section-copy">
                    Combined Risk Parity is the preferred balanced flagship in this historical sample because
                    it leads the combined-fund family on Sharpe ratio. It is not a universal winner and does
                    not remove drawdown risk.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title" style="margin-top:1.5rem;">Key metrics for the selected fund</div>',
        unsafe_allow_html=True,
    )
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Annualised return", fmt_pct(selected_row["annualised_return"]))
    m2.metric("Annualised volatility", fmt_pct(selected_row["annualised_volatility"]))
    m3.metric("Sharpe ratio", fmt_ratio(selected_row["sharpe_ratio"]))
    m4.metric("Maximum drawdown", fmt_pct(selected_row["maximum_drawdown"]))

    compare_funds = ["Combined Risk Parity", selected_fund, "Equity Equal Weight", "Crypto Minimum Variance"]
    compare_funds = list(dict.fromkeys(compare_funds))
    st.markdown('<div class="section-title">Compact growth-of-$1 comparison</div>', unsafe_allow_html=True)
    st.plotly_chart(growth_chart(fund_returns, compare_funds, dark_mode, height=330), width="stretch")
    st.caption("Historical growth of $1 after the 10 bps turnover-cost assumption. Dates remain out-of-sample live dates only.")

    st.markdown('<div class="section-title">Risk-return comparison across all ten funds</div>', unsafe_allow_html=True)
    st.plotly_chart(risk_return_chart(metrics, dark_mode, height=460), width="stretch")
    st.caption("Combined Risk Parity is the strongest balanced anchor in this sample, while Crypto Minimum Variance earns the highest Sharpe ratio with materially larger downside risk.")
    render_risk_return_zoom_views(metrics, dark_mode)

    st.markdown('<div class="section-title">Decision Studio</div>', unsafe_allow_html=True)
    objective = st.selectbox(
        "Historical objective",
        [
            "Diversified balance",
            "Capital stability",
            "Transparent simplicity",
            "Maximum historical growth",
            "Sentiment research",
        ],
        help="This educational selector maps an objective to historical evidence. It does not provide personal advice.",
    )
    candidate, evidence, drawback = app_logic.objective_candidate(metrics, objective)
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Historical candidate", candidate["fund"])
    d2.metric("Return", fmt_pct(candidate["annualised_return"]))
    d3.metric("Volatility", fmt_pct(candidate["annualised_volatility"]))
    d4.metric("Maximum drawdown", fmt_pct(candidate["maximum_drawdown"]))
    st.success(f"Evidence used: {evidence}")
    st.warning(f"What could invalidate the choice: {drawback}")

    with st.expander("Fund families & methods reference", expanded=False):
        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.markdown('<div class="section-title">Fund families</div>', unsafe_allow_html=True)
            for family, description in FAMILY_DESCRIPTIONS.items():
                st.markdown(
                    f'<div class="info-card" style="margin-bottom:0.75rem;"><strong>{family}</strong><br><span class="helper-text">{description}</span></div>',
                    unsafe_allow_html=True,
                )
        with c2:
            st.markdown('<div class="section-title">Fund methods</div>', unsafe_allow_html=True)
            method_copy = {
                "Equal Weight": "Every asset in the relevant universe receives the same target share.",
                "Minimum Variance": "Historical covariance is used to minimise volatility subject to long-only caps.",
                "Inverse-Volatility Risk Parity": "Weights scale inversely with volatility rather than solving the full-covariance equal-risk-contribution problem.",
            }
            for label, copy in method_copy.items():
                st.markdown(
                    f'<div class="info-card" style="margin-bottom:0.75rem;"><strong>{label}</strong><br><span class="helper-text">{copy}</span></div>',
                    unsafe_allow_html=True,
                )
    if st.button("Open the Movie-to-Market Lab", help="Jump to the separate Spider-Man versus Barbie research extension."):
        st.session_state["page"] = "Movie-to-Market Lab"
        set_query_state("Movie-to-Market Lab", dark_mode)
        st.rerun()


def render_compare_funds(data: dict[str, pd.DataFrame], dark_mode: bool) -> None:
    st.subheader("Compare Funds")
    metrics = data["performance_metrics"].copy()
    fund_returns = data["fund_returns"].copy()
    family_filter = st.multiselect(
        "Family filter",
        sorted(metrics["family"].unique()),
        default=sorted(metrics["family"].unique()),
        help="Filter the table and charts by fund family.",
    )
    method_filter = st.multiselect(
        "Method filter",
        sorted(metrics["method"].map(lambda method: METHOD_LABELS.get(method, method)).unique()),
        default=sorted(metrics["method"].map(lambda method: METHOD_LABELS.get(method, method)).unique()),
        help="Compare method structures without changing the underlying source files.",
    )
    filtered = metrics[
        metrics["family"].isin(family_filter)
        & metrics["method"].map(lambda method: METHOD_LABELS.get(method, method)).isin(method_filter)
    ].copy()
    chosen_funds = st.multiselect(
        "Funds to compare",
        filtered["fund"].tolist(),
        default=filtered["fund"].tolist()[:4],
        help="Select the funds to display in the growth and drawdown charts.",
    )
    table = filtered.copy()
    table["Method"] = table["method"].map(lambda method: METHOD_LABELS.get(method, method))
    table["Annualised return"] = table["annualised_return"].map(fmt_pct)
    table["Annualised volatility"] = table["annualised_volatility"].map(fmt_pct)
    table["Sharpe ratio"] = table["sharpe_ratio"].map(fmt_ratio)
    table["Maximum drawdown"] = table["maximum_drawdown"].map(fmt_pct)
    table["Ending value"] = table["ending_value"].map(lambda value: f"{float(value):.2f}")
    table["Turnover"] = table["total_turnover"].map(lambda value: f"{float(value):.2f}")
    table["Transaction cost (bps)"] = table["transaction_cost_bps"].map(lambda value: f"{float(value):.0f}")
    st.dataframe(
        table[
            [
                "fund",
                "family",
                "Method",
                "Annualised return",
                "Annualised volatility",
                "Sharpe ratio",
                "Maximum drawdown",
                "Ending value",
                "Turnover",
                "Transaction cost (bps)",
            ]
        ].rename(columns={"fund": "Fund", "family": "Family"}),
        width="stretch",
        hide_index=True,
    )
    st.caption("Percentages show two decimal places. Ending value is the historical growth of $1 over the live out-of-sample sample. Turnover is one-way total turnover.")

    if chosen_funds:
        st.plotly_chart(growth_chart(fund_returns, chosen_funds, dark_mode), width="stretch")
        st.plotly_chart(drawdown_chart(fund_returns, chosen_funds, dark_mode), width="stretch")
    st.markdown('<div class="section-title">Full-universe risk-return view</div>', unsafe_allow_html=True)
    st.plotly_chart(risk_return_chart(filtered, dark_mode, height=460), width="stretch")
    if len(filtered) > 4:
        render_risk_return_zoom_views(filtered, dark_mode)
    with st.expander("Metric definitions and disclosures"):
        st.markdown(
            """
            - Annualised return: geometric historical growth rate over the live out-of-sample record.
            - Annualised volatility: standard deviation of daily net returns annualised using 252 or 365 periods according to family.
            - Sharpe ratio: annualised return divided by annualised volatility under the permitted 0% risk-free assumption.
            - Maximum drawdown: worst peak-to-trough historical loss in the live record.
            - Ending value: growth of $1 after the transaction-cost deduction.
            - Turnover: total one-way turnover implied by monthly rebalancing.
            - Transaction cost assumption: 10 bps per unit of one-way turnover.
            """
        )


def fact_sheet_warning(row: pd.Series) -> str:
    if row["fund"] == "Crypto Minimum Variance":
        return (
            "Crypto Minimum Variance achieved the highest historical Sharpe ratio in this sample, but its drawdown remained deeper than 70%. "
            "It must not be described as low risk."
        )
    if row["family"] == "Crypto":
        return "The seven-day crypto calendar preserves weekend returns and can amplify both historical gains and drawdowns."
    if row["method"] == "sentiment_tilt":
        return "The sentiment overlay remains a modest extension of Equity Minimum Variance rather than an independent return engine."
    return "Historical outperformance on one objective does not make this fund universally preferred."


def render_fact_sheet(data: dict[str, pd.DataFrame], dark_mode: bool) -> None:
    st.subheader("Fund Fact Sheet")
    metrics = data["performance_metrics"].copy()
    holdings_data = data["current_holdings"].copy()
    fund = st.selectbox(
        "Fund",
        metrics["fund"].tolist(),
        index=metrics["fund"].tolist().index("Combined Risk Parity"),
        help="Open a single-fund sheet using only verified finale outputs.",
    )
    row = metrics.loc[metrics["fund"] == fund].iloc[0]
    holdings = latest_holdings_for_fund(holdings_data, fund)
    concentration = top_five_concentration(holdings)
    exposure = asset_family_exposure(holdings)

    top = st.columns(5)
    top[0].metric("Annualised return", fmt_pct(row["annualised_return"]))
    top[1].metric("Annualised volatility", fmt_pct(row["annualised_volatility"]))
    top[2].metric("Sharpe ratio", fmt_ratio(row["sharpe_ratio"]))
    top[3].metric("Maximum drawdown", fmt_pct(row["maximum_drawdown"]))
    top[4].metric("Ending value", f"{float(row['ending_value']):.2f}")

    summary_left, summary_right = st.columns([1.15, 1], gap="large")
    with summary_left:
        st.markdown(
            f"""
            <div class="panel-card">
                <div class="section-title">{fund}</div>
                <div class="section-copy">
                    Family: <strong>{row['family']}</strong><br>
                    Method: <strong>{METHOD_LABELS.get(row['method'], row['method'])}</strong><br>
                    Live sample: <strong>{fmt_date(row['first_live_date'])}</strong> to <strong>{fmt_date(row['last_live_date'])}</strong><br>
                    Estimation window: <strong>{int(row['estimation_window'])}</strong> observations<br>
                    Rebalancing: <strong>First observed day of each month</strong><br>
                    Transaction cost assumption: <strong>{float(row['transaction_cost_bps']):.0f} bps per unit of one-way turnover</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.warning(fact_sheet_warning(row))
        st.info(app_logic.fact_sheet_interpretation(row, metrics))
    with summary_right:
        st.metric("Turnover", f"{float(row['total_turnover']):.2f}")
        st.metric("Top-five concentration", fmt_pct(concentration))
        exposure_display = exposure.copy()
        exposure_display["weight"] = exposure_display["weight"].map(fmt_pct)
        st.dataframe(
            exposure_display.rename(columns={"asset_family": "Asset family", "weight": "Latest weight"}),
            width="stretch",
            hide_index=True,
        )

    st.plotly_chart(holdings_bar_chart(holdings, dark_mode), width="stretch")

    holdings_show = holdings.copy()
    holdings_show["weight"] = holdings_show["weight"].map(fmt_pct)
    st.dataframe(
        holdings_show.rename(columns={"ticker": "Ticker", "weight": "Latest weight"}),
        width="stretch",
        hide_index=True,
    )
    with st.expander("How to read the fact-sheet metrics"):
        st.markdown(
            """
            - Return: the historical compound rate achieved over the live out-of-sample sample.
            - Volatility: the dispersion of daily net returns, annualised to the relevant calendar.
            - Sharpe ratio: return scaled by volatility under the permitted zero risk-free assumption.
            - Maximum drawdown: the largest historical peak-to-trough loss.
            - Concentration: the share of the current target held in the top five weights.
            - Turnover: how much the portfolio historically traded when the monthly weights changed.
            """
        )


def render_holdings_and_allocation(data: dict[str, pd.DataFrame], dark_mode: bool) -> None:
    st.subheader("Holdings & Allocation")
    metrics = data["performance_metrics"]
    fund_returns = data["fund_returns"]
    holdings_data = data["current_holdings"]
    fund = st.selectbox(
        "Selected fund for holdings view",
        metrics["fund"].tolist(),
        index=metrics["fund"].tolist().index("Combined Risk Parity"),
    )
    holdings = latest_holdings_for_fund(holdings_data, fund)
    exposure = asset_family_exposure(holdings)

    left, right = st.columns([1.15, 0.85], gap="large")
    with left:
        st.markdown('<div class="section-title">Latest holdings</div>', unsafe_allow_html=True)
        st.plotly_chart(holdings_bar_chart(holdings, dark_mode), width="stretch")
        holdings_table = holdings.copy()
        holdings_table["weight"] = holdings_table["weight"].map(fmt_pct)
        st.dataframe(
            holdings_table.rename(columns={"ticker": "Ticker", "weight": "Latest weight"}),
            width="stretch",
            hide_index=True,
        )
    with right:
        st.markdown('<div class="section-title">Concentration and asset-family exposure</div>', unsafe_allow_html=True)
        st.metric("Top-five concentration", fmt_pct(top_five_concentration(holdings)))
        exposure_table = exposure.copy()
        exposure_table["weight"] = exposure_table["weight"].map(fmt_pct)
        st.dataframe(
            exposure_table.rename(columns={"asset_family": "Asset family", "weight": "Latest weight"}),
            width="stretch",
            hide_index=True,
        )
        st.caption("Combined funds can hold both equities and cryptocurrencies; crypto tickers are identified by the `-USD` suffix.")
    allocation_builder(metrics, fund_returns, dark_mode)


def render_news_sentiment(data: dict[str, pd.DataFrame], dark_mode: bool) -> None:
    st.subheader("News Sentiment")
    sector_index = data["sector_sentiment_index"].copy()
    sentiment_validation = data["sentiment_validation"].copy()
    dual_domain = data["dual_domain_validation"].copy()
    finance_metrics = data["finance_validation_metrics"].copy()
    finance_confusion = data["finance_confusion_matrix"].copy()
    finance_lexicon = data["finance_lexicon"].copy()
    sector_lexicon = data["sector_lexicon"].copy()
    fusion = data["fusion_comparison"].copy()
    checks = data["sentiment_product_app_checks"].copy()
    fund_returns = data["fund_returns"].copy()

    definitions = st.columns(3)
    definitions[0].markdown(
        '<div class="info-card"><strong>Positive finance sentiment</strong><br><span class="helper-text">Favourable investor-oriented language such as upgrades, beats or improving business conditions.</span></div>',
        unsafe_allow_html=True,
    )
    definitions[1].markdown(
        '<div class="info-card"><strong>Neutral finance sentiment</strong><br><span class="helper-text">The headline does not support a directional investor judgement, including many no-news or low-information states.</span></div>',
        unsafe_allow_html=True,
    )
    definitions[2].markdown(
        '<div class="info-card"><strong>Negative finance sentiment</strong><br><span class="helper-text">Adverse investor-oriented language such as downgrades, misses, fraud or bankruptcy-related wording.</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="panel-card" style="margin-top:1rem;">
            <div class="section-title">Sentiment model boundary</div>
            <div class="section-copy">
                Standard VADER is the baseline rule-based model. The finale adds a transparent
                18-term finance lexicon, keeps a neutral no-news treatment alongside an observed-only
                sensitivity comparison, applies a one-trading-day lag to tradable sentiment, and applies
                the signal only to equities because the supplied crypto dataset is price-only.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title" style="margin-top:1.5rem;">Sentiment coverage metrics</div>',
        unsafe_allow_html=True,
    )
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Usable unique headlines", fmt_count(checks.loc[checks["check"] == "Scored headline coverage", "observed"].iloc[0]))
    m2.metric("Baseline neutral share", fmt_pct(sentiment_validation.loc[sentiment_validation["diagnostic"] == "baseline_neutral_share", "value"].iloc[0]))
    m3.metric("Augmented neutral share", fmt_pct(sentiment_validation.loc[sentiment_validation["diagnostic"] == "finance_augmented_neutral_share", "value"].iloc[0]))
    m4.metric("Sign-changed share", fmt_pct(sentiment_validation.loc[sentiment_validation["diagnostic"] == "sign_changed_share", "value"].iloc[0]))

    snapshot = app_logic.latest_sector_snapshot(sector_index)
    snapshot_show = snapshot[["sector", "smoothed_sentiment", "smoothed_coverage"]].copy()
    snapshot_show["smoothed_sentiment"] = snapshot_show["smoothed_sentiment"].map(
        lambda value: f"{value:+.3f}"
    )
    snapshot_show["smoothed_coverage"] = snapshot_show["smoothed_coverage"].map(fmt_pct)
    with st.expander("Latest 21-trading-day sector snapshot", expanded=False):
        st.dataframe(
            snapshot_show.rename(
                columns={
                    "sector": "Sector",
                    "smoothed_sentiment": "Smoothed sentiment",
                    "smoothed_coverage": "Average ticker coverage",
                }
            ),
            width="stretch",
            hide_index=True,
        )

    sectors = sorted(sector_index["sector"].unique())
    selected_sectors = st.multiselect("Sectors", sectors, default=sectors[:4], help="Compare sector-level sentiment and coverage using the precomputed finale artefacts.")
    smooth_window = st.select_slider("Smoothing window", options=[5, 21, 63], value=21)
    if not selected_sectors:
        st.info("Select at least one sector.")
        return
    st.plotly_chart(sector_sentiment_chart(sector_index, selected_sectors, dark_mode, window=smooth_window), width="stretch")
    st.plotly_chart(coverage_chart(sector_index, selected_sectors, dark_mode, window=21, column="coverage_rate", title="Coverage rate"), width="stretch")
    st.plotly_chart(coverage_chart(sector_index, selected_sectors, dark_mode, window=21, column="article_count", title="Article count"), width="stretch")

    focus_sector = st.selectbox("Observed-only sensitivity sector", sectors, index=0)
    focus = sector_index[sector_index["sector"] == focus_sector].copy().sort_values("date").tail(180)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=focus["date"], y=focus["sentiment"], mode="lines", name="Neutral-fill sentiment", line=dict(color=accent("cyan", dark_mode), width=2.2)))
    fig.add_trace(go.Scatter(x=focus["date"], y=focus["observed_only_sentiment"], mode="lines", name="Observed-only sentiment", line=dict(color=accent("pink", dark_mode), width=2.0)))
    if "sector_augmented_sentiment" in focus.columns:
        fig.add_trace(go.Scatter(x=focus["date"], y=focus["sector_augmented_sentiment"], mode="lines", name="Sector-augmented sentiment (research extension)", line=dict(color=accent("purple", dark_mode), width=1.8, dash="dot")))
    st.plotly_chart(add_plot_layout(fig, dark_mode, height=320), width="stretch")
    st.caption("The observed-only sensitivity removes the neutral fill from no-news sector dates. The gap should be read as a model-governance check, not as a trading edge. Sector-augmented sentiment adds the sector-specific phrase lexicon on top of the finance-augmented score.")

    fusion_left, fusion_right = st.columns([1, 1], gap="large")
    with fusion_left:
        base = fusion.loc[fusion["fund"] == "Equity Minimum Variance"].iloc[0]
        tilted = fusion.loc[fusion["fund"] == "Equity Reliability-Gated Sentiment"].iloc[0]
        st.markdown('<div class="section-title">Fusion result</div>', unsafe_allow_html=True)
        st.metric("Annualised return change", fmt_pct(float(tilted["annualised_return"]) - float(base["annualised_return"]), signed=True))
        st.metric("Sharpe ratio change", fmt_ratio(float(tilted["sharpe_ratio"]) - float(base["sharpe_ratio"])))
        st.metric("Maximum drawdown change", fmt_pct(float(tilted["maximum_drawdown"]) - float(base["maximum_drawdown"]), signed=True))
    with fusion_right:
        pivot = fund_returns[fund_returns["fund"].isin(["Equity Minimum Variance", "Equity Reliability-Gated Sentiment"])].pivot(index="date", columns="fund", values="net_return")
        corr = pivot.corr().iloc[0, 1]
        st.markdown('<div class="section-title">Interpretive boundary</div>', unsafe_allow_html=True)
        st.metric("Daily return correlation", fmt_ratio(corr))
        st.caption(
            "The sentiment fund remains highly correlated with Equity Minimum Variance. The historical improvement is modest and does not establish independent return generation."
        )

    st.markdown('<div class="section-title">Finance holdout validation</div>', unsafe_allow_html=True)
    overall = finance_metrics.loc[finance_metrics["class"] == "overall"].copy()

    def finance_value(model: str, metric: str) -> float:
        return float(
            overall.loc[
                (overall["model"] == model) & (overall["metric"] == metric),
                "value",
            ].iloc[0]
        )

    standard_accuracy = finance_value("standard_vader", "accuracy")
    augmented_accuracy = finance_value("finance_augmented_vader", "accuracy")
    standard_macro_f1 = finance_value("standard_vader", "macro_f1")
    augmented_macro_f1 = finance_value("finance_augmented_vader", "macro_f1")
    kappa = finance_value("reviewer_agreement", "cohens_kappa")
    v1, v2, v3, v4 = st.columns(4)
    v1.metric("Internally labelled headlines", "1,000")
    v2.metric("Reviewer agreement κ", f"{kappa:.3f}")
    v3.metric(
        "Augmented accuracy",
        f"{augmented_accuracy:.1%}",
        f"{(augmented_accuracy - standard_accuracy) * 100:+.1f} percentage points",
    )
    v4.metric(
        "Augmented macro-F1",
        f"{augmented_macro_f1:.3f}",
        f"{augmented_macro_f1 - standard_macro_f1:+.3f}",
    )
    has_sector_model = ((overall["model"] == "sector_augmented_vader")).any()
    if has_sector_model:
        sector_accuracy = finance_value("sector_augmented_vader", "accuracy")
        sector_macro_f1 = finance_value("sector_augmented_vader", "macro_f1")
        st.caption("Research extension, evaluated on the same 1,000-headline holdout:")
        v5, v6 = st.columns(2)
        v5.metric(
            "Sector-augmented accuracy",
            f"{sector_accuracy:.1%}",
            f"{(sector_accuracy - augmented_accuracy) * 100:+.1f} pp vs finance-augmented",
        )
        v6.metric(
            "Sector-augmented macro-F1",
            f"{sector_macro_f1:.3f}",
            f"{sector_macro_f1 - augmented_macro_f1:+.3f} vs finance-augmented",
        )
    class_metrics = finance_metrics.loc[
        finance_metrics["class"].isin(["Positive", "Neutral", "Negative"])
    ].pivot_table(index=["model", "class"], columns="metric", values="value").reset_index()
    for column in ["precision", "recall", "f1"]:
        class_metrics[column] = class_metrics[column].map(lambda value: f"{value:.3f}")
    st.dataframe(
        class_metrics.rename(
            columns={
                "model": "Model",
                "class": "Class",
                "precision": "Precision",
                "recall": "Recall",
                "f1": "F1",
            }
        ),
        width="stretch",
        hide_index=True,
    )
    augmented_confusion = finance_confusion.loc[
        finance_confusion["model"] == "finance_augmented_vader"
    ].pivot(index="actual", columns="predicted", values="count")
    st.caption("Finance-augmented VADER confusion matrix; rows are actual labels and columns are predicted labels.")
    st.dataframe(augmented_confusion, width="stretch")
    st.warning(
        "The 1,000-headline holdout is separately held and internally human-labelled. It is useful internal evidence, not independent expert or commercial validation. Classification performance does not prove return predictability."
    )

    st.markdown('<div class="section-title">Separate movie-language validation</div>', unsafe_allow_html=True)
    dual_show = dual_domain.copy()
    dual_show = dual_show.loc[dual_show["domain"] == "Movie reviews (NLTK binary)"]
    dual_show["accuracy"] = dual_show["accuracy"].replace("", np.nan)
    dual_show["macro_f1"] = dual_show["macro_f1"].replace("", np.nan)
    dual_show["Accuracy"] = dual_show["accuracy"].map(lambda value: "—" if pd.isna(value) else f"{float(value):.3f}")
    dual_show["Macro-F1"] = dual_show["macro_f1"].map(lambda value: "—" if pd.isna(value) else f"{float(value):.3f}")
    st.dataframe(
        dual_show[["domain", "model", "observations", "Accuracy", "Macro-F1", "status", "limitation"]].rename(
            columns={
                "domain": "Domain",
                "model": "Model",
                "observations": "Observations",
                "status": "Status",
                "limitation": "Limitation",
            }
        ),
        width="stretch",
        hide_index=True,
    )
    st.caption("The movie-review check tests general-language non-degradation only. It does not validate financial forecasting or the Movie-to-Market event study.")
    with st.expander("Transparent 18-term finance lexicon"):
        st.dataframe(finance_lexicon.rename(columns={"term": "Term", "assigned_score": "Assigned score", "status": "Status"}), width="stretch", hide_index=True)
    with st.expander(f"Sector-specific sentiment lexicon research extension ({len(sector_lexicon):,} phrases across {sector_lexicon['sector'].nunique()} sectors)"):
        st.caption(
            "Student research extension: sector-scoped positive/negative/neutral phrase lists layered on top of "
            "the finance-augmented VADER score above. Positive and negative phrases are scored ±1.5; neutral "
            "phrases carry no score. Applied only to headlines tagged with the matching sector, exposed as the "
            "separate `sector_augmented_sentiment` field so the validated 18-term pathway above is unchanged."
        )
        sector_order = sorted(sector_lexicon["sector"].unique())
        sector_tabs = st.tabs([SECTOR_DISPLAY_NAMES.get(sector, sector) for sector in sector_order])
        for tab, sector in zip(sector_tabs, sector_order, strict=False):
            with tab:
                sector_rows = sector_lexicon[sector_lexicon["sector"] == sector]
                counts = sector_rows["category"].value_counts()
                c1, c2, c3 = st.columns(3)
                c1.metric("Positive phrases", fmt_count(counts.get("positive", 0)))
                c2.metric("Negative phrases", fmt_count(counts.get("negative", 0)))
                c3.metric("Neutral phrases", fmt_count(counts.get("neutral", 0)))
                st.dataframe(
                    sector_rows[["category", "phrase", "score"]]
                    .sort_values(["category", "phrase"])
                    .rename(columns={"category": "Category", "phrase": "Phrase", "score": "Score"}),
                    width="stretch",
                    hide_index=True,
                )

                sector_history = sector_index[sector_index["sector"] == sector].sort_values("date")
                if "sector_augmented_sentiment" in sector_history.columns and not sector_history.empty:
                    recent = sector_history.tail(180)
                    shift = (recent["sector_augmented_sentiment"] - recent["sentiment"]).abs().mean()
                    tilt = (recent["sector_augmented_sentiment"] - recent["sentiment"]).mean()
                    direction = "more positive" if tilt > 0 else "more negative" if tilt < 0 else "unchanged"
                    st.caption(
                        f"On real {SECTOR_DISPLAY_NAMES.get(sector, sector)} headlines over the last "
                        f"{len(recent)} trading days, this lexicon shifts the average day-level sentiment score "
                        f"by {shift:.3f} (mean absolute change) and leans the sector index {direction} on net "
                        f"({tilt:+.3f}) relative to the finance-augmented baseline."
                    )
                    trend_fig = go.Figure()
                    trend_fig.add_trace(
                        go.Scatter(
                            x=recent["date"], y=recent["sentiment"], mode="lines",
                            name="Finance-augmented", line=dict(color=accent("cyan", dark_mode), width=1.8),
                        )
                    )
                    trend_fig.add_trace(
                        go.Scatter(
                            x=recent["date"], y=recent["sector_augmented_sentiment"], mode="lines",
                            name="Sector-augmented", line=dict(color=accent("purple", dark_mode), width=1.8, dash="dot"),
                        )
                    )
                    st.plotly_chart(add_plot_layout(trend_fig, dark_mode, height=260), width="stretch")
                else:
                    st.caption("Sector-augmented sentiment history is not available yet for this sector; rerun the pipeline to populate it.")


def render_movie_lab(data: dict[str, pd.DataFrame], dark_mode: bool) -> None:
    st.subheader(MOVIE_TITLE)
    summary = data["movie_lab_event_summary"].copy()
    external_prices = data["movie_lab_external_prices"].copy()
    exposure = data["movie_lab_exposure_register"].copy()
    ratings = data["movie_lab_imdb_ratings"].copy()
    sources = data["movie_lab_sources"].copy()
    gap = data["movie_lab_gap_closure"].copy()

    st.markdown('<div class="secondary-badge">Secondary research extension</div>', unsafe_allow_html=True)
    st.caption("The lab is separate from the official ten funds. SONY, MAT and WBD remain outside the supplied 50-equity course universe.")
    st.markdown(
        '<div class="warning-note"><strong>Descriptive association only.</strong> These event windows do not establish that movie marketing caused the observed share-price movement.</div>',
        unsafe_allow_html=True,
    )

    film = st.selectbox("Film", sorted(summary["film"].unique()), help="Choose either Spider-Man: No Way Home or Barbie.")
    film_events = summary[summary["film"] == film].copy().sort_values("event_date")
    event_stage = st.selectbox("Event stage", film_events["event_stage"].tolist(), help="The six predeclared events remain the only event stages shown here.")
    selected = film_events[film_events["event_stage"] == event_stage].iloc[0]

    m1, m2, m3 = st.columns(3)
    m1.metric("Primary exposure", selected["primary_ticker"])
    m2.metric("Event-day company return", fmt_pct(selected["event_day_return"], signed=True))
    m3.metric("Event-day market-adjusted return", fmt_pct(selected["event_day_market_adjusted_return"], signed=True))

    m4, m5, m6 = st.columns(3)
    m4.metric("Event-day SPY return", fmt_pct(selected["benchmark_event_day_return"], signed=True))
    m5.metric("11-trading-day company return", fmt_pct(selected["eleven_trading_day_return"], signed=True))
    m6.metric("11-trading-day market-adjusted return", fmt_pct(selected["eleven_day_market_adjusted_return"], signed=True))

    st.plotly_chart(movie_event_window_chart(selected, external_prices, dark_mode), width="stretch")
    st.caption("Primary exposure and SPY are shown for every event; DIS or WBD appears only as contextual exposure where relevant.")

    event_table = film_events.copy()
    for column in [
        "event_day_return",
        "benchmark_event_day_return",
        "event_day_market_adjusted_return",
        "eleven_trading_day_return",
        "benchmark_eleven_day_return",
        "eleven_day_market_adjusted_return",
    ]:
        event_table[column] = event_table[column].map(lambda value: fmt_pct(value, signed=True))
    st.dataframe(
        event_table[
            [
                "event_stage",
                "event_date",
                "primary_ticker",
                "event_day_return",
                "benchmark_event_day_return",
                "event_day_market_adjusted_return",
                "eleven_trading_day_return",
                "benchmark_eleven_day_return",
                "eleven_day_market_adjusted_return",
            ]
        ].rename(
            columns={
                "event_stage": "Event stage",
                "event_date": "Event date",
                "primary_ticker": "Primary ticker",
                "event_day_return": "Event-day company return",
                "benchmark_event_day_return": "Event-day SPY return",
                "event_day_market_adjusted_return": "Event-day market-adjusted",
                "eleven_trading_day_return": "11-day company return",
                "benchmark_eleven_day_return": "11-day SPY return",
                "eleven_day_market_adjusted_return": "11-day market-adjusted",
            }
        ),
        width="stretch",
        hide_index=True,
    )

    st.markdown('<div class="section-title">Exposure register</div>', unsafe_allow_html=True)
    st.dataframe(exposure[exposure["film"] == film], width="stretch", hide_index=True)

    st.markdown('<div class="section-title">IMDb aggregate ratings</div>', unsafe_allow_html=True)
    st.dataframe(ratings[ratings["film"] == film], width="stretch", hide_index=True)
    st.caption("IMDb ratings are current aggregates retrieved on 14 Aug 2026. They are not dated historical reviews and do not enter the portfolio model.")

    used_source_ids = set(film_events["source_id"].dropna().astype(str))
    for value in exposure[exposure["film"] == film]["evidence_source_ids"]:
        used_source_ids.update(part.strip() for part in str(value).split(";") if part.strip())
    st.markdown('<div class="section-title">Evidence sources and hierarchy</div>', unsafe_allow_html=True)
    st.caption("Primary filings and campaign material outrank retrospective commentary. Evidence strength and limitations are displayed explicitly.")
    st.dataframe(sources[sources["source_id"].isin(sorted(used_source_ids))], width="stretch", hide_index=True)

    with st.expander("Gap-closure implementation status"):
        st.dataframe(gap, width="stretch", hide_index=True)
    st.info(
        "The Movie-to-Market Lab does not change the ten offered funds, does not validate the finance lexicon, and does not imply causality between film marketing and equity returns."
    )


def render_methodology(data: dict[str, pd.DataFrame], support_text: dict[str, str], dark_mode: bool) -> None:
    st.subheader("Methodology & Limitations")
    spec = data["model_specification"].copy()
    use_register = data["asset_data_use_register"].copy()
    audit = data["carried_forward_integrity_audit"].copy()
    feasibility = data["product_feasibility_scorecard"].copy()
    risks = data["risk_mitigation_register"].copy()
    fund_weights = data["fund_weights"].copy()
    sentiment_index = data["sector_sentiment_index"].copy()

    unique_tickers = fund_weights["ticker"].dropna().unique().tolist()
    equity_count = sum(1 for ticker in unique_tickers if classify_ticker(ticker) == "Equity")
    crypto_count = sum(1 for ticker in unique_tickers if classify_ticker(ticker) == "Crypto")
    start_year = pd.to_datetime(sentiment_index["date"]).min().year
    end_year = pd.to_datetime(sentiment_index["date"]).max().year

    cards = st.columns(4)
    cards[0].metric("Official sample boundary", f"{start_year}-{end_year}")
    cards[1].metric("Supplied equities", f"{equity_count}")
    cards[2].metric("Supplied cryptocurrencies", f"{crypto_count}")
    cards[3].metric("Turnover cost assumption", "10 bps")

    st.markdown(
        """
        <div class="panel-card" style="margin-top:1rem;">
            <div class="section-title">Prototype methodology</div>
            <div class="section-copy">
                Returns are built from adjusted closes. Equities and combined funds use 252-period annualisation on
                the equity decision calendar, while crypto-only funds use 365-period annualisation on the seven-day
                crypto calendar. Every offered fund is long-only, monthly rebalanced, estimated on past-only windows,
                and charged 10 bps per unit of one-way turnover.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(spec.rename(columns={"parameter": "Decision", "value": "Setting", "reason": "Reason"}), width="stretch", hide_index=True)

    st.markdown('<div class="section-title">Models, equations and symbol guide</div>', unsafe_allow_html=True)
    with st.expander("1. Asset return and net portfolio return", expanded=True):
        st.latex(r"r_{i,t}=\frac{P_{i,t}}{P_{i,t-1}}-1\,;")
        st.markdown(
            "Here, `rᵢ,ₜ` is asset *i*'s return on date *t*; `Pᵢ,ₜ` is its adjusted close on date *t*; and `Pᵢ,ₜ₋₁` is the preceding adjusted close."
        )
        st.latex(r"r^{net}_{p,t}=\sum_{i=1}^{N}w_{i,t-1}r_{i,t}-c\tau_t\,;")
        st.markdown(
            "Here, `rᵖⁿᵉᵗ,ₜ` is the fund's net return; `N` is the number of assets; `wᵢ,ₜ₋₁` is the prior target weight; `rᵢ,ₜ` is the asset return; `c` is 0.001, or 10 bps; and `τₜ` is one-way turnover."
        )
    with st.expander("2. Covariance shrinkage and minimum variance"):
        st.latex(r"\widehat{\Sigma}_{\lambda}=(1-\lambda)\widehat{\Sigma}+\lambda\operatorname{diag}(\widehat{\Sigma})\,,\quad \lambda=0.10\,;")
        st.markdown(
            "Here, `Σ̂` is the sample covariance matrix; `diag(Σ̂)` keeps only its variances; and `λ` is the fixed 10% shrinkage strength used to reduce unstable off-diagonal estimates."
        )
        st.latex(r"\min_{w}\;w^{\top}\widehat{\Sigma}_{\lambda}w\quad\text{s.t.}\quad\mathbf{1}^{\top}w=1\,,\;0\leq w_i\leq u_i\,.")
        st.markdown(
            "Here, `w` is the weight vector; `wᵀΣ̂λw` is portfolio variance; `1ᵀw = 1` makes weights sum to 100%; and `uᵢ` is the asset-specific upper cap."
        )
    with st.expander("3. Inverse-volatility risk parity"):
        st.latex(r"w_i=\frac{\sigma_i^{-1}}{\sum_{j=1}^{N}\sigma_j^{-1}}\,;")
        st.markdown(
            "Here, `σᵢ` is asset *i*'s estimated volatility; `σᵢ⁻¹` is inverse volatility; and the denominator normalises all weights to sum to 100%. This is inverse-volatility risk parity. It is not full-covariance equal-risk-contribution optimisation."
        )
    with st.expander("4. Annualised Sharpe ratio"):
        st.latex(r"SR=\frac{\overline{r}}{s_r}\sqrt{A}\,;")
        st.markdown(
            "Here, `SR` is the historical Sharpe ratio; `r̄` is mean daily net return; `sᵣ` is its sample standard deviation; and `A` is 252 for equity or combined funds and 365 for crypto-only funds. The permitted risk-free rate is 0%."
        )
    with st.expander("5. Reliability-gated sentiment multiplier"):
        st.latex(r"m_{i,t}=\operatorname{clip}\!\left(1+\alpha s_{i,t-1}q_{i,t-1},\,m_{\min},\,m_{\max}\right)\,;")
        st.markdown(
            "Here, `mᵢ,ₜ` is the equity weight multiplier; `α` controls tilt strength; `sᵢ,ₜ₋₁` is lagged finance-augmented VADER sentiment; `qᵢ,ₜ₋₁` is lagged reliability; and `mₘᵢₙ` and `mₘₐₓ` cap the change. The adjusted weights are renormalised and recapped."
        )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="section-title">Sentiment and leakage controls</div>', unsafe_allow_html=True)
        st.markdown(
            """
            - Sentiment is aligned to the next equity trading day before any tradable use.
            - The investable sentiment signal uses a one-trading-day lag.
            - No same-day headline leakage is allowed.
            - The app does not rerun the backtest or download external data during normal rendering.
            - A separately held, internally human-labelled 1,000-headline finance set shows very high reviewer agreement and modest classification improvement from the finance-augmented lexicon over Standard VADER.
            """
        )
    with c2:
        st.markdown('<div class="section-title">Prototype limitations</div>', unsafe_allow_html=True)
        st.markdown(
            """
            - No live fills, execution routing, custody or incident process.
            - No calibrated slippage or market-impact model beyond the 10 bps turnover assumption.
            - No legal suitability assessment or production investment authorisation.
            - No claim that the prototype is production-investable.
            - External movie prices and IMDb aggregates remain outside the official course-data fund universe.
            """
        )

    with st.expander("Asset use register and integrity audit"):
        st.dataframe(use_register, width="stretch", hide_index=True)
        st.dataframe(audit, width="stretch", hide_index=True)

    st.markdown('<div class="section-title">Publication status and student-controlled actions</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    p1.success("Public GitHub repository: complete and independently observed.")
    p1.link_button("Open Project B repository", PUBLIC_REPOSITORY_URL)
    p2.warning("Live Streamlit URL and signed-out deployment test: not yet evidenced.")
    with st.expander("Student finalisation requirements"):
        st.markdown(support_text["student_finalisation"])
    with st.expander("Citation verification requirements"):
        st.markdown(support_text["citation_verification"])
    with st.expander("Movie-lab technical reconciliation note"):
        st.markdown(support_text["gap_closure"])

    st.markdown('<div class="section-title">Product readiness boundary</div>', unsafe_allow_html=True)
    st.dataframe(feasibility, width="stretch", hide_index=True)
    st.dataframe(risks, width="stretch", hide_index=True)


def render_missing_files_message(missing: list[Path]) -> None:
    inject_css(True)
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-title">{BRAND} cannot start</div>
            <div class="hero-subtitle">
                Required precomputed artefacts are missing. The app will not invent replacement values.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.error("Missing files:\n- " + "\n- ".join(path.name for path in missing))
    st.info("Regenerate the finale outputs from this project folder, then reopen the app.")


def main() -> None:
    current_page, dark_mode = initialise_state()
    inject_css(dark_mode)
    selected_page, dark_mode = sidebar_navigation(current_page, dark_mode)
    st.session_state["page"] = selected_page
    st.session_state["dark_mode"] = dark_mode
    set_query_state(selected_page, dark_mode)
    inject_css(dark_mode)

    missing = missing_required_files(ROOT)
    if missing:
        render_missing_files_message(missing)
        st.stop()

    try:
        data = load_artifacts()
        support_text = load_support_texts()
    except Exception as exc:  # pragma: no cover - user-facing error path
        st.error(
            "SignalScope could not load the finale artefacts cleanly. "
            "Check the local results files and rerun the verified build if necessary."
        )
        st.caption(str(exc))
        st.stop()

    render_banner_and_header()
    if selected_page == "Overview":
        render_overview(data, dark_mode)
    elif selected_page == "Compare Funds":
        render_compare_funds(data, dark_mode)
    elif selected_page == "Fund Fact Sheet":
        render_fact_sheet(data, dark_mode)
    elif selected_page == "Holdings & Allocation":
        render_holdings_and_allocation(data, dark_mode)
    elif selected_page == "News Sentiment":
        render_news_sentiment(data, dark_mode)
    elif selected_page == "Movie-to-Market Lab":
        render_movie_lab(data, dark_mode)
    else:
        render_methodology(data, support_text, dark_mode)

    st.markdown("---")
    st.caption(
        f"{BRAND} | {TAGLINE} | Public-source academic prototype using precomputed finale artefacts only."
    )


if __name__ == "__main__":
    main()
