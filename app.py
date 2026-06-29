# Student Performance Analytics Dashboard
# Project Visualisasi Data - Streamlit App
# Running Instructions:
# 1. conda env create -f environment.yml
# 2. conda activate vd-env
# 3. streamlit run Streamlit/app.py

from __future__ import annotations

import html
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# 1. PAGE CONFIG
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 2. GLOBAL STYLE & CONSTANTS
COLORS = {
    "bg": "#F8FAFC",
    "surface": "#FFFFFF",
    "text": "#0F172A",
    "muted": "#64748B",
    "primary": "#2563EB",
    "primary_dark": "#1E3A8A",
    "secondary": "#06B6D4",
    "positive": "#16A34A",
    "warning": "#F59E0B",
    "negative": "#DC2626",
    "purple": "#7C3AED",
    "border": "#E2E8F0",
}

PERFORMANCE_ORDER = ["At Risk", "Needs Improvement", "Good", "Excellent"]
PERFORMANCE_COLORS = {
    "At Risk": COLORS["negative"],
    "Needs Improvement": COLORS["warning"],
    "Good": COLORS["primary"],
    "Excellent": COLORS["positive"],
}

RISK_ORDER = ["Low Risk", "Medium Risk", "High Risk"]
RISK_COLORS = {
    "Low Risk": COLORS["positive"],
    "Medium Risk": COLORS["warning"],
    "High Risk": COLORS["negative"],
}

STRESS_ORDER = ["Low", "Medium", "High"]
ANXIETY_ORDER = ["Low", "Medium", "High"]

CORE_NUMERIC_COLS = [
    "Age",
    "Hours_Studied",
    "Attendance",
    "Sleep_Hours",
    "Stress_Level",
    "Screen_Time",
    "Previous_GPA_Cleaned",
    "Tutoring_Sessions_Per_Week",
    "Exam_Anxiety_Score",
    "Final_Score",
]

CORE_CATEGORICAL_COLS = [
    "Gender",
    "Part_Time_Job",
    "Study_Method",
    "Diet_Quality",
    "Internet_Quality",
    "Extracurricular",
    "Family_Income_Level",
    "Performance_Category",
    "Risk_Level",
    "Academic_Risk_Level",
]

PLOTLY_TEMPLATE = "plotly_white"
SEMANTIC_COLORSCALE = [
    [0.00, COLORS["negative"]],
    [0.50, COLORS["warning"]],
    [1.00, COLORS["positive"]],
]


# 3. CSS INJECTION
def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        .stApp {{
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(180deg, #F1F5F9 0%, #E8EEF8 100%);
            color: {COLORS['text']};
        }}

        .main .block-container {{
            padding-top: 1.4rem;
        }}

        section[data-testid="stSidebar"] {{
            background: #F8FAFC;
            border-right: 1px solid {COLORS['border']};
        }}

        section[data-testid="stSidebar"] > div {{
            background: #F8FAFC;
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {{
            color: {COLORS['text']};
        }}

        section[data-testid="stSidebar"] div[data-testid="stCaptionContainer"],
        section[data-testid="stSidebar"] small {{
            color: #475569;
        }}

        section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
        section[data-testid="stSidebar"] div[data-baseweb="input"] > div,
        section[data-testid="stSidebar"] div[data-baseweb="textarea"] > div {{
            background-color: #FFFFFF;
            color: {COLORS['text']};
            border-color: #CBD5E1;
        }}

        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea,
        section[data-testid="stSidebar"] div[data-baseweb="input"] input {{
            color: {COLORS['text']};
            -webkit-text-fill-color: {COLORS['text']};
        }}

        section[data-testid="stSidebar"] input::placeholder,
        section[data-testid="stSidebar"] textarea::placeholder {{
            color: #64748B;
            opacity: 1;
            -webkit-text-fill-color: #64748B;
        }}

        section[data-testid="stSidebar"] div[data-testid="stExpander"] {{
            background: #FFFFFF;
            border: 1px solid {COLORS['border']};
            border-radius: 14px;
            overflow: hidden;
        }}

        section[data-testid="stSidebar"] div[role="radiogroup"] label,
        section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] label,
        section[data-testid="stSidebar"] div[data-testid="stSlider"] label,
        section[data-testid="stSidebar"] div[data-testid="stTextInput"] label {{
            color: {COLORS['text']};
            font-weight: 650;
        }}

        section[data-testid="stSidebar"] div[data-testid="stButton"] button,
        section[data-testid="stSidebar"] div[data-testid="stDownloadButton"] button,
        div[data-testid="stDownloadButton"] button {{
            background: #FFFFFF;
            color: {COLORS['text']};
            border: 1px solid #CBD5E1;
            border-radius: 10px;
            font-weight: 750;
        }}

        section[data-testid="stSidebar"] div[data-testid="stButton"] button *,
        section[data-testid="stSidebar"] div[data-testid="stDownloadButton"] button *,
        div[data-testid="stDownloadButton"] button * {{
            color: {COLORS['text']};
        }}

        section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover,
        section[data-testid="stSidebar"] div[data-testid="stDownloadButton"] button:hover,
        div[data-testid="stDownloadButton"] button:hover {{
            background: {COLORS['primary']};
            border-color: {COLORS['primary']};
            color: #FFFFFF;
        }}

        section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover *,
        section[data-testid="stSidebar"] div[data-testid="stDownloadButton"] button:hover *,
        div[data-testid="stDownloadButton"] button:hover * {{
            color: #FFFFFF;
        }}

        section[data-testid="stSidebar"] div[data-testid="stMetric"] {{
            background: #FFFFFF;
            border: 1px solid {COLORS['border']};
            padding: 14px 16px;
            border-radius: 14px;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
        }}

        div[data-testid="stExpander"] details {{
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 14px;
            overflow: hidden;
        }}

        div[data-testid="stExpander"] details summary,
        div[data-testid="stExpander"] details summary:hover,
        div[data-testid="stExpander"] details summary:focus,
        div[data-testid="stExpander"] details summary:focus-visible {{
            background: #1F2937;
            color: #F8FAFC;
            border-radius: 14px 14px 0 0;
            font-weight: 750;
            outline: none;
        }}

        div[data-testid="stExpander"] details:not([open]) summary {{
            border-radius: 14px;
        }}

        div[data-testid="stExpander"] details summary *,
        div[data-testid="stExpander"] details summary:hover *,
        div[data-testid="stExpander"] details summary:focus *,
        div[data-testid="stExpander"] details summary:focus-visible * {{
            color: #F8FAFC;
            fill: #F8FAFC;
            stroke: #F8FAFC;
        }}

        div[data-testid="stExpander"] details summary:hover {{
            background: #111827;
        }}

        div[data-testid="stTabs"] button[role="tab"] {{
            color: #334155;
            font-weight: 700;
            border-radius: 12px 12px 0 0;
        }}

        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
            color: {COLORS['primary_dark']};
            background: rgba(37, 99, 235, 0.08);
        }}

        div[data-testid="stMetric"] {{
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            padding: 16px 18px;
            border-radius: 18px;
            box-shadow: 0 14px 30px rgba(15, 23, 42, 0.09);
        }}

        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] p {{
            color: #334155;
            font-weight: 750;
        }}

        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] div {{
            color: {COLORS['text']};
            font-weight: 850;
        }}

        div[data-testid="stMetricDelta"],
        div[data-testid="stMetricDelta"] div {{
            color: {COLORS['positive']};
            font-weight: 750;
        }}

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] p,
        div[data-testid="stMetric"] span {{
            color: {COLORS['text']} !important;
            -webkit-text-fill-color: {COLORS['text']} !important;
        }}

        div[data-testid="stMetric"] div[data-testid="stMetricLabel"] *,
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] * {{
            color: {COLORS['text']} !important;
            -webkit-text-fill-color: {COLORS['text']} !important;
        }}

        div[data-testid="stMetric"] * {{
            color: {COLORS['text']} !important;
            -webkit-text-fill-color: {COLORS['text']} !important;
        }}

        div[data-testid="stMetricDelta"] *,
        div[data-testid="stMetric"] div[data-testid="stMetricDelta"] * {{
            color: {COLORS['positive']} !important;
            -webkit-text-fill-color: {COLORS['positive']} !important;
        }}

        div[data-testid="stSelectbox"] label,
        div[data-testid="stRadio"] label,
        div[data-testid="stRadio"] div[role="radiogroup"] label,
        div[data-testid="stRadio"] div[role="radiogroup"] label *,
        div[data-testid="stSelectbox"] label * {{
            color: {COLORS['text']} !important;
            -webkit-text-fill-color: {COLORS['text']} !important;
            font-weight: 700;
        }}

        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
            background: #FFFFFF;
            color: {COLORS['text']} !important;
            border-color: #CBD5E1;
        }}

        div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] svg {{
            color: {COLORS['text']} !important;
            fill: {COLORS['text']} !important;
        }}

        .hero-card {{
            background: radial-gradient(circle at 10% 20%, rgba(6,182,212,.25), transparent 28%),
                        linear-gradient(135deg, #0F172A 0%, #1E3A8A 48%, #2563EB 100%);
            color: white;
            padding: 30px 34px;
            border-radius: 28px;
            box-shadow: 0 22px 50px rgba(30, 58, 138, 0.28);
            margin-bottom: 18px;
            border: 1px solid rgba(255,255,255,.18);
        }}

        .hero-title {{
            font-size: 34px;
            line-height: 1.12;
            font-weight: 850;
            margin: 0 0 8px 0;
            letter-spacing: -0.035em;
        }}

        .hero-subtitle {{
            font-size: 15.5px;
            line-height: 1.7;
            max-width: 980px;
            margin: 0;
            color: rgba(255,255,255,.88);
        }}

        .hero-info {{
            display: inline-block;
            margin-top: 16px;
            padding: 14px 16px;
            background: rgba(255,255,255,.12);
            border: 1px solid rgba(255,255,255,.22);
            border-radius: 18px;
            color: rgba(255,255,255,.94);
            font-size: 14px;
            line-height: 1.7;
        }}

        .hero-info strong {{
            color: #FFFFFF;
            font-weight: 800;
        }}

        .badge-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 18px;
        }}

        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255,255,255,.13);
            color: white;
            border: 1px solid rgba(255,255,255,.22);
            border-radius: 999px;
            padding: 7px 11px;
            font-size: 12px;
            font-weight: 650;
        }}

        .metric-card-custom {{
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 18px;
            padding: 15px 16px;
            box-shadow: 0 14px 32px rgba(15, 23, 42, 0.10);
            position: relative;
            overflow: hidden;
            min-height: 116px;
            margin-bottom: 14px;
        }}

        .metric-card-custom::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: var(--accent);
        }}

        .metric-icon {{
            width: 34px;
            height: 34px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(37, 99, 235, .12);
            color: var(--accent);
            font-weight: 800;
            font-size: 18px;
            margin-bottom: 8px;
        }}

        .metric-title {{
            font-size: 12px;
            color: {COLORS['muted']};
            text-transform: uppercase;
            letter-spacing: .055em;
            font-weight: 750;
        }}

        .metric-value {{
            color: {COLORS['text']};
            font-size: 26px;
            line-height: 1.15;
            font-weight: 850;
            margin-top: 5px;
            letter-spacing: -0.03em;
        }}

        .metric-caption {{
            color: {COLORS['muted']};
            font-size: 12px;
            line-height: 1.45;
            margin-top: 6px;
        }}

        .insight-card {{
            background: #FFFFFF;
            border: 1px solid {COLORS['border']};
            border-left: 6px solid var(--accent);
            border-radius: 18px;
            padding: 16px 18px;
            box-shadow: 0 12px 28px rgba(15,23,42,.06);
            margin: 8px 0;
        }}

        .insight-title {{
            color: {COLORS['text']};
            font-size: 14px;
            font-weight: 800;
            margin-bottom: 4px;
        }}

        .insight-body {{
            color: {COLORS['muted']};
            font-size: 13.5px;
            line-height: 1.62;
        }}

        .section-note {{
            background: #DBEAFE;
            border: 1px solid #93C5FD;
            border-radius: 16px;
            padding: 13px 15px;
            color: #1E3A8A;
            font-size: 13.5px;
            line-height: 1.55;
            margin: 8px 0 18px 0;
        }}

        .danger-note {{
            background: #FEE2E2;
            border: 1px solid #FCA5A5;
            border-radius: 16px;
            padding: 13px 15px;
            color: #991B1B;
            font-size: 13.5px;
            line-height: 1.55;
            margin: 8px 0 18px 0;
        }}

        .small-muted {{
            color: {COLORS['muted']};
            font-size: 12.5px;
            line-height: 1.5;
        }}

        .data-source-pill {{
            background: #FFFFFF;
            color: #334155;
            border: 1px solid #CBD5E1;
            border-radius: 999px;
            padding: 8px 12px;
            font-size: 12px;
            font-weight: 650;
            margin-bottom: 10px;
            display: inline-block;
        }}

        .sidebar-section-title {{
            color: {COLORS['text']};
            font-size: 13px;
            font-weight: 800;
            margin: 18px 0 8px 0;
            padding-top: 4px;
        }}

        div[data-testid="stPlotlyChart"] {{
            background: #FFFFFF;
            border: 1px solid #D7E1EE;
            border-radius: 18px;
            padding: 0;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
            overflow: hidden;
        }}

        div[data-testid="stPlotlyChart"] > div {{
            border-radius: 18px;
            overflow: hidden;
        }}

        div[data-testid="stDataFrame"] {{
            border: 1px solid {COLORS['border']};
            border-radius: 18px;
            overflow: hidden;
        }}

        @media (max-width: 1100px) {{
            .hero-title {{ font-size: 28px; }}
        }}

        @media (max-width: 720px) {{
            .hero-card {{ padding: 24px; }}
            .hero-title {{ font-size: 24px; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# 4. PATH & DATA LOADING HELPERS
def unique_paths(paths: Iterable[Path]) -> list[Path]:
    seen: set[str] = set()
    output: list[Path] = []
    for path in paths:
        try:
            key = str(path.resolve())
        except Exception:
            key = str(path)
        if key not in seen:
            seen.add(key)
            output.append(path)
    return output


def get_search_roots() -> list[Path]:
    roots: list[Path] = []

    roots.append(Path.cwd())
    try:
        app_dir = Path(__file__).resolve().parent
        roots.extend([app_dir, app_dir.parent, app_dir.parent.parent])
    except NameError:
        pass

    # Include the /mnt/data directory for cloud environments like Google Colab or Kaggle.
    roots.append(Path("/mnt/data"))

    return [p for p in unique_paths(roots) if p.exists() and p.is_dir()]


def find_dataset_path() -> Optional[Path]:
    """Auto-search dataset path."""
    preferred_relative_paths = [
        Path("Data") / "cleaned_student_performance.csv",
        Path("Data") / "student_performance_finalscore.csv",
        Path("cleaned_student_performance.csv"),
        Path("student_performance_finalscore.csv"),
    ]

    for root in get_search_roots():
        for rel_path in preferred_relative_paths:
            candidate = root / rel_path
            if candidate.exists() and candidate.is_file():
                return candidate

    # Recursive fallback, limited to expected filenames only.
    filenames = ["cleaned_student_performance.csv", "student_performance_finalscore.csv"]
    for root in get_search_roots():
        for filename in filenames:
            try:
                matches = list(root.rglob(filename))
            except Exception:
                matches = []
            if matches:
                # Prefer files inside a Data folder, then shortest path.
                matches = sorted(
                    matches,
                    key=lambda p: ("Data" not in [part for part in p.parts], len(str(p))),
                )
                return matches[0]

    return None


@st.cache_data(show_spinner="Membaca dataset...")
def load_csv_from_path(path_str: str) -> pd.DataFrame:
    return pd.read_csv(path_str)


# 5. DATA PREPARATION & FEATURE ENGINEERING
def safe_to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def performance_category(score: float) -> str:
    if pd.isna(score):
        return "Unknown"
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Good"
    if score >= 60:
        return "Needs Improvement"
    return "At Risk"


def study_group(hours: float) -> str:
    if pd.isna(hours):
        return "Unknown"
    if hours < 3:
        return "Low Study (<3h)"
    if hours <= 6:
        return "Moderate Study (3-6h)"
    return "High Study (>6h)"


def attendance_group(attendance: float) -> str:
    if pd.isna(attendance):
        return "Unknown"
    if attendance < 70:
        return "Low Attendance (<70%)"
    if attendance <= 85:
        return "Moderate Attendance (70-85%)"
    return "High Attendance (>85%)"


def sleep_category(hours: float) -> str:
    if pd.isna(hours):
        return "Unknown"
    if hours < 6:
        return "Short Sleep (<6h)"
    if hours <= 8:
        return "Ideal Sleep (6-8h)"
    return "Long Sleep (>8h)"


def scale_category(value: float) -> str:
    if pd.isna(value):
        return "Unknown"
    if value <= 3:
        return "Low"
    if value <= 6:
        return "Medium"
    return "High"


def screen_time_group(hours: float) -> str:
    if pd.isna(hours):
        return "Unknown"
    if hours <= 2:
        return "Low Screen Time (≤2h)"
    if hours <= 5:
        return "Moderate Screen Time (2-5h)"
    return "High Screen Time (>5h)"


def iqr_outlier_flag(series: pd.Series) -> pd.Series:
    numeric = safe_to_numeric(series)
    q1 = numeric.quantile(0.25)
    q3 = numeric.quantile(0.75)
    iqr = q3 - q1
    if pd.isna(iqr) or iqr == 0:
        return pd.Series(False, index=series.index)
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return (numeric < lower_bound) | (numeric > upper_bound)


def prepare_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare raw or cleaned dataset so the app can run from either file."""
    data = df.copy()
    data.columns = [str(col).strip() for col in data.columns]

    # Drop exact duplicate rows.
    data = data.drop_duplicates().reset_index(drop=True)

    # Numeric conversion for expected columns.
    numeric_candidates = [
        "Age",
        "Hours_Studied",
        "Attendance",
        "Sleep_Hours",
        "Stress_Level",
        "Screen_Time",
        "Previous_GPA",
        "Previous_GPA_Cleaned",
        "Tutoring_Sessions_Per_Week",
        "Exam_Anxiety_Score",
        "Final_Score",
        "Risk_Score",
        "Academic_Risk_Score",
    ]
    for col in numeric_candidates:
        if col in data.columns:
            data[col] = safe_to_numeric(data[col])

    # Fill numeric missing values with median, categorical with Unknown.
    for col in data.columns:
        if pd.api.types.is_numeric_dtype(data[col]):
            if data[col].isna().any():
                data[col] = data[col].fillna(data[col].median())
        elif data[col].dtype == "object":
            data[col] = data[col].fillna("Unknown").astype(str).str.strip()

    # Previous GPA anomaly handling.
    if "Previous_GPA" in data.columns:
        if "Previous_GPA_Anomaly_Flag" not in data.columns:
            data["Previous_GPA_Anomaly_Flag"] = data["Previous_GPA"] > 4
        if "Previous_GPA_Cleaned" not in data.columns:
            data["Previous_GPA_Cleaned"] = data["Previous_GPA"].clip(lower=0, upper=4)

    # IQR outlier flags for key numeric variables.
    iqr_cols = [
        "Age",
        "Hours_Studied",
        "Attendance",
        "Sleep_Hours",
        "Stress_Level",
        "Screen_Time",
        "Previous_GPA",
        "Previous_GPA_Cleaned",
        "Tutoring_Sessions_Per_Week",
        "Exam_Anxiety_Score",
        "Final_Score",
    ]
    for col in iqr_cols:
        if col in data.columns:
            flag_col = f"{col}_IQR_Outlier_Flag"
            if flag_col not in data.columns:
                data[flag_col] = iqr_outlier_flag(data[col])

    # Feature engineering for storytelling and filters.
    if "Final_Score" in data.columns and "Performance_Category" not in data.columns:
        data["Performance_Category"] = data["Final_Score"].apply(performance_category)
    if "Hours_Studied" in data.columns and "Study_Hours_Group" not in data.columns:
        data["Study_Hours_Group"] = data["Hours_Studied"].apply(study_group)
    if "Attendance" in data.columns and "Attendance_Group" not in data.columns:
        data["Attendance_Group"] = data["Attendance"].apply(attendance_group)
    if "Sleep_Hours" in data.columns and "Sleep_Category" not in data.columns:
        data["Sleep_Category"] = data["Sleep_Hours"].apply(sleep_category)
    if "Stress_Level" in data.columns and "Stress_Category" not in data.columns:
        data["Stress_Category"] = data["Stress_Level"].apply(scale_category)
    if "Exam_Anxiety_Score" in data.columns and "Anxiety_Category" not in data.columns:
        data["Anxiety_Category"] = data["Exam_Anxiety_Score"].apply(scale_category)
    if "Screen_Time" in data.columns and "Screen_Time_Group" not in data.columns:
        data["Screen_Time_Group"] = data["Screen_Time"].apply(screen_time_group)

    # Risk_Level from notebook: post-evaluation segmentation using Final_Score.
    required_post_risk_cols = ["Final_Score", "Hours_Studied", "Attendance", "Stress_Level", "Exam_Anxiety_Score"]
    if all(col in data.columns for col in required_post_risk_cols) and "Risk_Level" not in data.columns:
        risk_score = (
            (data["Final_Score"] < 75).astype(int)
            + (data["Hours_Studied"] < 3).astype(int)
            + (data["Attendance"] < 70).astype(int)
            + (data["Stress_Level"] > 6).astype(int)
            + (data["Exam_Anxiety_Score"] > 6).astype(int)
        )
        data["Risk_Score"] = risk_score
        data["Risk_Level"] = pd.cut(
            risk_score,
            bins=[-1, 1, 3, 5],
            labels=RISK_ORDER,
        ).astype(str)

    # Academic_Risk_Level: early-warning style segmentation without Final_Score.
    required_academic_risk_cols = ["Hours_Studied", "Attendance", "Stress_Level", "Exam_Anxiety_Score"]
    if all(col in data.columns for col in required_academic_risk_cols):
        academic_risk_score = (
            (data["Hours_Studied"] < 3).astype(int)
            + (data["Attendance"] < 70).astype(int)
            + (data["Stress_Level"] > 6).astype(int)
            + (data["Exam_Anxiety_Score"] > 6).astype(int)
        )
        if "Screen_Time" in data.columns:
            academic_risk_score += (data["Screen_Time"] > 5).astype(int)
        data["Academic_Risk_Score"] = academic_risk_score
        data["Academic_Risk_Level"] = pd.cut(
            academic_risk_score,
            bins=[-1, 1, 3, 5],
            labels=RISK_ORDER,
        ).astype(str)

    # Enforce category order where relevant.
    ordered_categories = {
        "Performance_Category": PERFORMANCE_ORDER,
        "Risk_Level": RISK_ORDER,
        "Academic_Risk_Level": RISK_ORDER,
        "Stress_Category": STRESS_ORDER,
        "Anxiety_Category": ANXIETY_ORDER,
    }
    for col, order in ordered_categories.items():
        if col in data.columns:
            data[col] = pd.Categorical(data[col], categories=order, ordered=True)

    return data


# 6. DISPLAY HELPERS
def format_number(value: float | int, decimals: int = 0) -> str:
    if pd.isna(value):
        return "-"
    if decimals == 0:
        return f"{value:,.0f}"
    return f"{value:,.{decimals}f}"


def html_escape(value: object) -> str:
    return html.escape(str(value))


def display_label(value: object) -> str:
    return str(value).replace("_", " ")


def display_dataset_path(path: Optional[Path]) -> str:
    if path is None:
        return "Uploaded file"

    resolved_path = path.resolve()
    for root in get_search_roots():
        try:
            relative_path = resolved_path.relative_to(root.resolve())
        except ValueError:
            continue
        if relative_path.parts and relative_path.parts[0] == "Data":
            return relative_path.as_posix()

    if resolved_path.parent.name == "Data":
        return (Path("Data") / resolved_path.name).as_posix()
    return resolved_path.name


def metric_card(title: str, value: str, caption: str, accent: str, icon: str) -> str:
    return f"""
    <div class="metric-card-custom" style="--accent:{accent};">
        <div class="metric-icon">{html_escape(icon)}</div>
        <div class="metric-title">{html_escape(title)}</div>
        <div class="metric-value">{html_escape(value)}</div>
        <div class="metric-caption">{html_escape(caption)}</div>
    </div>
    """


def render_metric_grid(cards: list[str], cards_per_row: int = 4) -> None:
    for start in range(0, len(cards), cards_per_row):
        cols = st.columns(cards_per_row, gap="medium")
        for col, card in zip(cols, cards[start : start + cards_per_row]):
            with col:
                st.markdown(card, unsafe_allow_html=True)


def insight_card(title: str, body: str, accent: str = COLORS["primary"]) -> None:
    st.markdown(
        f"""
        <div class="insight-card" style="--accent:{accent};">
            <div class="insight-title">{html_escape(title)}</div>
            <div class="insight-body">{html_escape(body)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_note(text: str, kind: str = "info") -> None:
    class_name = "danger-note" if kind == "danger" else "section-note"
    st.markdown(f"<div class='{class_name}'>{html_escape(text)}</div>", unsafe_allow_html=True)


def apply_plot_style(fig: go.Figure, height: int = 520, title: Optional[str] = None) -> go.Figure:
    if title:
        fig.update_layout(title=title)
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=height,
        font=dict(family="Inter, Arial, sans-serif", size=13, color=COLORS["text"]),
        title=dict(font=dict(size=20, color=COLORS["text"]), x=0.02, xanchor="left"),
        margin=dict(l=55, r=36, t=88, b=58),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#CBD5E1",
            font=dict(color=COLORS["text"], size=12, family="Inter, Arial, sans-serif"),
        ),
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="right",
            x=0.88,
            font=dict(color=COLORS["text"], size=12),
            bgcolor="rgba(255,255,255,0.86)",
        ),
    )
    fig.update_xaxes(
        gridcolor="#DDE7F3",
        zerolinecolor="#CBD5E1",
        tickfont=dict(color="#334155"),
        title_font=dict(color="#334155"),
        linecolor="#CBD5E1",
    )
    fig.update_yaxes(
        gridcolor="#DDE7F3",
        zerolinecolor="#CBD5E1",
        tickfont=dict(color="#334155"),
        title_font=dict(color="#334155"),
        linecolor="#CBD5E1",
    )
    return fig


def safe_plotly_chart(fig: go.Figure, key: Optional[str] = None) -> None:
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": "hover", "responsive": True},
        key=key,
    )


# 7. ANALYTICAL HELPERS
def available_cols(data: pd.DataFrame, cols: Iterable[str]) -> list[str]:
    return [col for col in cols if col in data.columns]


def compute_target_correlations(data: pd.DataFrame, target: str = "Final_Score") -> pd.DataFrame:
    if target not in data.columns:
        return pd.DataFrame(columns=["Variabel", "Korelasi", "Arah", "Abs_Korelasi"])

    candidate_cols = available_cols(data, CORE_NUMERIC_COLS)
    candidate_cols = [col for col in candidate_cols if col != target]
    if not candidate_cols:
        return pd.DataFrame(columns=["Variabel", "Korelasi", "Arah", "Abs_Korelasi"])

    corr_rows = []
    for col in candidate_cols:
        series = safe_to_numeric(data[col])
        target_series = safe_to_numeric(data[target])
        if series.nunique(dropna=True) <= 1 or target_series.nunique(dropna=True) <= 1:
            continue
        corr_value = series.corr(target_series)
        if pd.notna(corr_value):
            corr_rows.append(
                {
                    "Variabel": col,
                    "Korelasi": corr_value,
                    "Arah": "Positif" if corr_value >= 0 else "Negatif",
                    "Abs_Korelasi": abs(corr_value),
                }
            )
    return pd.DataFrame(corr_rows).sort_values("Abs_Korelasi", ascending=False)


def get_top_correlated_variable(data: pd.DataFrame) -> tuple[str, float] | tuple[None, None]:
    corr_df = compute_target_correlations(data)
    if corr_df.empty:
        return None, None
    top = corr_df.iloc[0]
    return str(top["Variabel"]), float(top["Korelasi"])


def make_master_matrix() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Nama Fitur/Kolom": "Final_Score",
                "Tipe Data": "Kuantitatif",
                "Strategi Visual": "Explanation",
                "Rencana Grafik": "Histogram, KPI Card, dan distribusi kategori performa",
            },
            {
                "Nama Fitur/Kolom": "Hours_Studied",
                "Tipe Data": "Kuantitatif",
                "Strategi Visual": "Explanation",
                "Rencana Grafik": "Scatter plot dengan trendline terhadap Final_Score",
            },
            {
                "Nama Fitur/Kolom": "Exam_Anxiety_Score",
                "Tipe Data": "Kuantitatif / Ordinal skala",
                "Strategi Visual": "Explanation",
                "Rencana Grafik": "Scatter plot dan heatmap Anxiety x Stress",
            },
            {
                "Nama Fitur/Kolom": "Stress_Level",
                "Tipe Data": "Kuantitatif / Ordinal skala",
                "Strategi Visual": "Explanation",
                "Rencana Grafik": "Scatter plot dan heatmap risiko psikologis",
            },
            {
                "Nama Fitur/Kolom": "Tutoring_Sessions_Per_Week",
                "Tipe Data": "Kuantitatif diskrit",
                "Strategi Visual": "Explanation",
                "Rencana Grafik": "Bar chart rata-rata Final_Score per jumlah sesi tutoring",
            },
            {
                "Nama Fitur/Kolom": "Attendance",
                "Tipe Data": "Kuantitatif",
                "Strategi Visual": "Explanation",
                "Rencana Grafik": "Scatter plot atau binned bar chart terhadap Final_Score",
            },
            {
                "Nama Fitur/Kolom": "Study_Method",
                "Tipe Data": "Nominal",
                "Strategi Visual": "Exploration",
                "Rencana Grafik": "Boxplot dan sorted bar chart mean Final_Score",
            },
            {
                "Nama Fitur/Kolom": "Diet_Quality",
                "Tipe Data": "Ordinal",
                "Strategi Visual": "Exploration",
                "Rencana Grafik": "Boxplot dan bar chart rata-rata Final_Score",
            },
        ]
    )


def read_master_matrix() -> pd.DataFrame:
    for root in get_search_roots():
        candidate = root / "Reports" / "master_matrix_tipe_data.xlsx"
        if candidate.exists():
            try:
                return pd.read_excel(candidate)
            except Exception:
                break
    return make_master_matrix()


def outlier_summary(data: pd.DataFrame) -> pd.DataFrame:
    flag_cols = [col for col in data.columns if col.endswith("_IQR_Outlier_Flag")]
    rows = []
    for flag_col in flag_cols:
        base_col = flag_col.replace("_IQR_Outlier_Flag", "")
        count = int(data[flag_col].fillna(False).astype(bool).sum())
        rows.append(
            {
                "Variabel": display_label(base_col),
                "Jumlah Outlier": count,
                "Persentase": (count / len(data) * 100) if len(data) else 0,
            }
        )
    return pd.DataFrame(rows).sort_values("Jumlah Outlier", ascending=False)


def profile_table(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in data.columns:
        rows.append(
            {
                "Kolom": col,
                "Tipe Data": str(data[col].dtype),
                "Missing": int(data[col].isna().sum()),
                "Missing (%)": round(float(data[col].isna().mean() * 100), 2),
                "Unique": int(data[col].nunique(dropna=True)),
            }
        )
    return pd.DataFrame(rows)


def describe_numeric(data: pd.DataFrame) -> pd.DataFrame:
    cols = available_cols(data, CORE_NUMERIC_COLS)
    if not cols:
        return pd.DataFrame()
    desc = data[cols].describe().T
    desc["median"] = data[cols].median(numeric_only=True)
    desc["range"] = desc["max"] - desc["min"]
    desc = desc.rename(
        columns={
            "count": "count",
            "mean": "mean",
            "std": "std_dev",
            "min": "min",
            "max": "max",
        }
    )
    ordered = ["count", "mean", "median", "std_dev", "min", "max", "range"]
    return desc[ordered].round(2).reset_index().rename(columns={"index": "Variabel"})


def make_download_csv(data: pd.DataFrame) -> bytes:
    return data.to_csv(index=False).encode("utf-8")


# 8. FILTER HELPERS
def reset_filter_state() -> None:
    keys_to_delete = [
        key
        for key in st.session_state.keys()
        if key.startswith("filter_") or key.startswith("slider_") or key in {"student_id_search"}
    ]
    for key in keys_to_delete:
        del st.session_state[key]


def sorted_unique_strings(series: pd.Series, preferred_order: Optional[list[str]] = None) -> list[str]:
    values = series.dropna().astype(str).unique().tolist()
    if preferred_order:
        ordered = [item for item in preferred_order if item in values]
        remaining = sorted([item for item in values if item not in ordered])
        return ordered + remaining
    return sorted(values)


def sidebar_multiselect(data: pd.DataFrame, col: str, label: str, preferred_order: Optional[list[str]] = None) -> list[str]:
    options = sorted_unique_strings(data[col], preferred_order)
    return st.multiselect(
        label,
        options=options,
        default=options,
        key=f"filter_{col}",
    )


def sidebar_range_slider(data: pd.DataFrame, col: str, label: str, step: float = 0.1) -> tuple[float, float]:
    min_value = float(data[col].min())
    max_value = float(data[col].max())
    if min_value == max_value:
        st.caption(f"{label}: semua nilai = {min_value:.2f}")
        return min_value, max_value
    return st.slider(
        label,
        min_value=min_value,
        max_value=max_value,
        value=(min_value, max_value),
        step=step,
        key=f"slider_{col}",
    )


def build_sidebar_filters(data: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
    st.sidebar.markdown("## 🎛️ Filter Dashboard")
    st.sidebar.caption("Semua KPI, grafik, insight, dan tabel akan berubah mengikuti filter.")

    if st.sidebar.button("↻ Reset semua filter", use_container_width=True):
        reset_filter_state()
        st.rerun()

    risk_mode = st.sidebar.radio(
        "Definisi risiko",
        options=[
            "Post-evaluation Risk Level",
            "Early-warning Academic Risk Level",
        ],
        index=0,
        help=(
            "Post-evaluation memakai Final Score sebagai salah satu indikator. "
            "Early-warning tidak memakai Final Score, sehingga lebih cocok untuk prediksi awal."
        ),
    )
    risk_col = "Academic_Risk_Level" if risk_mode.startswith("Early") else "Risk_Level"
    if risk_col not in data.columns:
        risk_col = "Risk_Level" if "Risk_Level" in data.columns else "Academic_Risk_Level"

    filtered = data.copy()

    with st.sidebar.expander("Kategori mahasiswa", expanded=False):
        category_filters = [
            ("Gender", "Gender", None),
            ("Study_Method", "Metode belajar", None),
            ("Diet_Quality", "Kualitas diet", None),
            ("Internet_Quality", "Kualitas internet", None),
            ("Family_Income_Level", "Level pendapatan keluarga", None),
            ("Part_Time_Job", "Part-time job", None),
            ("Extracurricular", "Ekstrakurikuler", None),
            ("Performance_Category", "Kategori performa", PERFORMANCE_ORDER),
            (risk_col, "Kategori risiko", RISK_ORDER),
        ]
        for col, label, order in category_filters:
            if col in filtered.columns:
                selected = sidebar_multiselect(data, col, label, order)
                if selected:
                    filtered = filtered[filtered[col].astype(str).isin(selected)]

    with st.sidebar.expander("Rentang numerik", expanded=False):
        numeric_filters = [
            ("Hours_Studied", "Jam belajar", 0.1),
            ("Attendance", "Attendance (%)", 0.1),
            ("Stress_Level", "Stress level", 0.1),
            ("Exam_Anxiety_Score", "Exam anxiety", 0.1),
            ("Screen_Time", "Screen time", 0.1),
            ("Final_Score", "Final Score", 0.1),
        ]
        for col, label, step in numeric_filters:
            if col in data.columns:
                min_val, max_val = sidebar_range_slider(data, col, label, step)
                filtered = filtered[filtered[col].between(min_val, max_val, inclusive="both")]

    with st.sidebar.expander("Pencarian mahasiswa", expanded=False):
        search_term = st.text_input(
            "Cari Student_ID",
            placeholder="Contoh: STU00001",
            key="student_id_search",
        ).strip()
        if search_term and "Student_ID" in filtered.columns:
            filtered = filtered[filtered["Student_ID"].astype(str).str.contains(search_term, case=False, na=False)]

    st.sidebar.markdown("---")
    st.sidebar.metric("Data terfilter", f"{len(filtered):,}", f"dari {len(data):,} mahasiswa")
    st.sidebar.progress(0 if len(data) == 0 else min(len(filtered) / len(data), 1.0))

    st.sidebar.download_button(
        label="⬇️ Download data terfilter",
        data=make_download_csv(filtered),
        file_name="filtered_student_performance.csv",
        mime="text/csv",
        use_container_width=True,
    )

    return filtered.reset_index(drop=True), risk_col, risk_mode


# 9. CHART FUNCTIONS
def chart_final_score_distribution(data: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        data,
        x="Final_Score",
        color="Performance_Category" if "Performance_Category" in data.columns else None,
        color_discrete_map=PERFORMANCE_COLORS,
        nbins=32,
        marginal="box",
        opacity=0.88,
        labels={"Final_Score": "Final Score", "count": "Jumlah Mahasiswa"},
        title="Distribusi Final Score Mahasiswa",
    )
    fig.update_traces(marker_line_width=0.4, marker_line_color="white")
    return apply_plot_style(fig, height=540)


def chart_performance_composition(data: pd.DataFrame) -> go.Figure:
    if "Performance_Category" not in data.columns:
        return go.Figure()
    counts = (
        data["Performance_Category"]
        .astype(str)
        .value_counts()
        .reindex(PERFORMANCE_ORDER)
        .dropna()
        .reset_index()
    )
    counts.columns = ["Performance_Category", "Jumlah"]
    counts["Persentase"] = counts["Jumlah"] / counts["Jumlah"].sum() * 100

    fig = px.bar(
        counts,
        y="Performance_Category",
        x="Jumlah",
        orientation="h",
        text=counts["Persentase"].map(lambda x: f"{x:.1f}%"),
        color="Performance_Category",
        color_discrete_map=PERFORMANCE_COLORS,
        labels={"Performance_Category": "Kategori Performa", "Jumlah": "Jumlah Mahasiswa"},
        title="Komposisi Kategori Performa",
    )
    fig.update_traces(textposition="outside", marker_line_width=0.6, marker_line_color="white")
    fig.update_yaxes(categoryorder="array", categoryarray=PERFORMANCE_ORDER[::-1])
    fig.update_layout(showlegend=False)
    return apply_plot_style(fig, height=430)


def chart_average_score_gauge(data: pd.DataFrame) -> go.Figure:
    avg_score = float(data["Final_Score"].mean()) if "Final_Score" in data.columns and len(data) else 0
    bar_color = COLORS["positive"] if avg_score >= 85 else COLORS["warning"] if avg_score >= 75 else COLORS["negative"]

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=avg_score,
            number={"suffix": "", "font": {"size": 38}},
            delta={"reference": 83.21, "relative": False, "valueformat": ".2f"},
            title={"text": "Average Final Score", "font": {"size": 18}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": COLORS["muted"]},
                "bar": {"color": bar_color, "thickness": 0.22},
                "bgcolor": "white",
                "borderwidth": 1,
                "bordercolor": COLORS["border"],
                "steps": [
                    {"range": [0, 60], "color": "rgba(220,38,38,.12)"},
                    {"range": [60, 75], "color": "rgba(245,158,11,.15)"},
                    {"range": [75, 90], "color": "rgba(37,99,235,.12)"},
                    {"range": [90, 100], "color": "rgba(22,163,74,.14)"},
                ],
                "threshold": {
                    "line": {"color": COLORS["text"], "width": 3},
                    "thickness": 0.8,
                    "value": avg_score,
                },
            },
        )
    )
    return apply_plot_style(fig, height=430, title="Indikator Rata-rata Nilai")


def chart_correlation_bar(data: pd.DataFrame) -> go.Figure:
    corr_df = compute_target_correlations(data).head(10)
    if corr_df.empty:
        return go.Figure()
    corr_df = corr_df.sort_values("Korelasi", ascending=True)
    corr_df["Variabel"] = corr_df["Variabel"].map(display_label)
    color_map = {"Positif": COLORS["positive"], "Negatif": COLORS["negative"]}
    fig = px.bar(
        corr_df,
        x="Korelasi",
        y="Variabel",
        orientation="h",
        color="Arah",
        color_discrete_map=color_map,
        text=corr_df["Korelasi"].map(lambda x: f"{x:.2f}"),
        title="Faktor Numerik yang Paling Berkaitan dengan Final Score",
        labels={"Korelasi": "Korelasi Pearson", "Variabel": "Variabel"},
    )
    fig.update_traces(textposition="outside", marker_line_width=0.6, marker_line_color="white")
    fig.add_vline(x=0, line_width=1.4, line_dash="dash", line_color=COLORS["muted"])
    return apply_plot_style(fig, height=520)


def chart_scatter_with_trend(
    data: pd.DataFrame,
    x_col: str,
    y_col: str = "Final_Score",
    color_col: Optional[str] = "Performance_Category",
    title: str = "Scatter Plot",
    labels: Optional[dict[str, str]] = None,
    size_col: Optional[str] = None,
    height: int = 560,
    opacity: float = 0.72,
) -> go.Figure:
    if labels is None:
        labels = {}
    plot_data = data.copy()
    if len(plot_data) > 5000:
        plot_data = plot_data.sample(5000, random_state=42)

    display_labels = {col: display_label(col) for col in plot_data.columns}
    display_labels.update(labels)
    if color_col:
        display_labels[color_col] = display_label(color_col)
    if size_col:
        display_labels[size_col] = display_label(size_col)

    color_map = PERFORMANCE_COLORS if color_col == "Performance_Category" else RISK_COLORS if color_col in ["Risk_Level", "Academic_Risk_Level"] else None

    try:
        fig = px.scatter(
            plot_data,
            x=x_col,
            y=y_col,
            color=color_col if color_col in plot_data.columns else None,
            size=size_col if size_col in plot_data.columns else None,
            color_discrete_map=color_map,
            trendline="ols" if len(plot_data) >= 3 and plot_data[x_col].nunique() > 1 else None,
            opacity=opacity,
            hover_data=available_cols(plot_data, ["Student_ID", "Attendance", "Stress_Level", "Exam_Anxiety_Score", "Hours_Studied", "Tutoring_Sessions_Per_Week"]),
            title=title,
            labels=display_labels,
        )
    except Exception:
        fig = px.scatter(
            plot_data,
            x=x_col,
            y=y_col,
            color=color_col if color_col in plot_data.columns else None,
            size=size_col if size_col in plot_data.columns else None,
            color_discrete_map=color_map,
            opacity=opacity,
            hover_data=available_cols(plot_data, ["Student_ID", "Attendance", "Stress_Level", "Exam_Anxiety_Score", "Hours_Studied", "Tutoring_Sessions_Per_Week"]),
            title=title,
            labels=display_labels,
        )
    fig.update_traces(marker=dict(line=dict(width=0.4, color="white")))
    return apply_plot_style(fig, height=height)


def chart_tutoring_effect(data: pd.DataFrame) -> go.Figure:
    group = (
        data.groupby("Tutoring_Sessions_Per_Week", observed=True)
        .agg(
            Mean_Final_Score=("Final_Score", "mean"),
            Median_Final_Score=("Final_Score", "median"),
            Jumlah=("Final_Score", "size"),
        )
        .reset_index()
        .sort_values("Tutoring_Sessions_Per_Week")
    )
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=group["Tutoring_Sessions_Per_Week"],
            y=group["Mean_Final_Score"],
            text=group["Mean_Final_Score"].map(lambda x: f"{x:.1f}"),
            textposition="outside",
            marker_color=COLORS["primary"],
            marker_line_color="white",
            marker_line_width=0.7,
            name="Mean Final Score",
            customdata=np.stack([group["Jumlah"]], axis=-1),
            hovertemplate="Sesi tutoring: %{x}<br>Mean score: %{y:.2f}<br>Jumlah mahasiswa: %{customdata[0]:,}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=group["Tutoring_Sessions_Per_Week"],
            y=group["Median_Final_Score"],
            mode="lines+markers",
            line=dict(color=COLORS["positive"], width=3),
            marker=dict(size=9, line=dict(color="white", width=1)),
            name="Median Final Score",
        )
    )
    fig.update_layout(
        title="Rata-rata Final Score Berdasarkan Jumlah Sesi Tutoring",
        xaxis_title="Tutoring Sessions per Week",
        yaxis_title="Final Score",
    )
    return apply_plot_style(fig, height=520)


def chart_group_mean_bar(data: pd.DataFrame, group_col: str, title: str, order: Optional[list[str]] = None) -> go.Figure:
    group = (
        data.groupby(group_col, observed=True)
        .agg(Mean_Final_Score=("Final_Score", "mean"), Jumlah=("Final_Score", "size"))
        .reset_index()
    )
    group[group_col] = group[group_col].astype(str)
    if order:
        group[group_col] = pd.Categorical(group[group_col], categories=order, ordered=True)
        group = group.sort_values(group_col)
    else:
        group = group.sort_values("Mean_Final_Score", ascending=False)
    fig = px.bar(
        group,
        x=group_col,
        y="Mean_Final_Score",
        color="Mean_Final_Score",
        color_continuous_scale=SEMANTIC_COLORSCALE,
        text=group["Mean_Final_Score"].map(lambda x: f"{x:.1f}"),
        hover_data={"Jumlah": ":,", "Mean_Final_Score": ":.2f"},
        title=title,
        labels={group_col: display_label(group_col), "Mean_Final_Score": "Rata-rata Final Score"},
    )
    fig.update_traces(textposition="outside", marker_line_width=0.7, marker_line_color="white")
    fig.update_layout(coloraxis_showscale=False)
    return apply_plot_style(fig, height=500)


def chart_stress_anxiety_heatmap(data: pd.DataFrame) -> go.Figure:
    pivot = (
        data.pivot_table(
            index="Stress_Category",
            columns="Anxiety_Category",
            values="Final_Score",
            aggfunc="mean",
            observed=True,
        )
        .reindex(index=STRESS_ORDER, columns=ANXIETY_ORDER)
        .round(2)
    )

    count_pivot = (
        data.pivot_table(
            index="Stress_Category",
            columns="Anxiety_Category",
            values="Final_Score",
            aggfunc="size",
            observed=True,
        )
        .reindex(index=STRESS_ORDER, columns=ANXIETY_ORDER)
        .fillna(0)
        .astype(int)
    )

    text = pivot.copy().astype(object)
    for idx in pivot.index:
        for col in pivot.columns:
            value = pivot.loc[idx, col]
            count = count_pivot.loc[idx, col]
            text.loc[idx, col] = "-" if pd.isna(value) else f"{value:.1f}<br>n={count:,}"

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns.astype(str),
            y=pivot.index.astype(str),
            colorscale=SEMANTIC_COLORSCALE,
            text=text.values,
            texttemplate="%{text}",
            hovertemplate="Stress: %{y}<br>Anxiety: %{x}<br>Mean Final Score: %{z:.2f}<extra></extra>",
            colorbar=dict(title="Mean Score"),
            zmin=max(0, np.nanmin(pivot.values) - 3) if np.isfinite(np.nanmin(pivot.values)) else 0,
            zmax=min(100, np.nanmax(pivot.values) + 3) if np.isfinite(np.nanmax(pivot.values)) else 100,
        )
    )
    fig.update_layout(
        title="Heatmap Final Score: Kombinasi Stress dan Anxiety",
        xaxis_title="Anxiety Category",
        yaxis_title="Stress Category",
    )
    return apply_plot_style(fig, height=500)


def chart_risk_summary(data: pd.DataFrame, risk_col: str) -> go.Figure:
    counts = (
        data[risk_col]
        .astype(str)
        .value_counts()
        .reindex(RISK_ORDER)
        .dropna()
        .reset_index()
    )
    counts.columns = [risk_col, "Jumlah"]
    counts["Persentase"] = counts["Jumlah"] / counts["Jumlah"].sum() * 100
    fig = px.bar(
        counts,
        x=risk_col,
        y="Jumlah",
        color=risk_col,
        color_discrete_map=RISK_COLORS,
        text=counts["Persentase"].map(lambda x: f"{x:.1f}%"),
        title=f"Distribusi {display_label(risk_col)}",
        labels={risk_col: "Kategori Risiko", "Jumlah": "Jumlah Mahasiswa"},
    )
    fig.update_traces(textposition="outside", marker_line_width=0.7, marker_line_color="white")
    fig.update_layout(showlegend=False)
    return apply_plot_style(fig, height=430)


def chart_risk_performance_stack(data: pd.DataFrame, risk_col: str) -> go.Figure:
    ctab = pd.crosstab(data[risk_col].astype(str), data["Performance_Category"].astype(str), normalize="index") * 100
    ctab = ctab.reindex(index=RISK_ORDER, columns=PERFORMANCE_ORDER).fillna(0)
    long_df = ctab.reset_index().melt(id_vars=risk_col, var_name="Performance_Category", value_name="Persentase")
    fig = px.bar(
        long_df,
        x=risk_col,
        y="Persentase",
        color="Performance_Category",
        color_discrete_map=PERFORMANCE_COLORS,
        category_orders={risk_col: RISK_ORDER, "Performance_Category": PERFORMANCE_ORDER},
        text=long_df["Persentase"].map(lambda x: f"{x:.0f}%" if x >= 4 else ""),
        title="Komposisi Performa di Tiap Kategori Risiko",
        labels={risk_col: "Kategori Risiko", "Persentase": "Persentase (%)"},
    )
    fig.update_traces(textposition="inside", marker_line_width=0.3, marker_line_color="white")
    fig.update_layout(barmode="stack", yaxis_ticksuffix="%")
    return apply_plot_style(fig, height=500)


def chart_category_box(data: pd.DataFrame, category_col: str) -> go.Figure:
    fig = px.box(
        data,
        x=category_col,
        y="Final_Score",
        points="outliers",
        title=f"Distribusi Final Score Berdasarkan {display_label(category_col)}",
        labels={category_col: display_label(category_col), "Final_Score": "Final Score"},
    )
    fig.update_traces(marker_color=COLORS["primary"], line_color=COLORS["primary"])
    fig.update_layout(showlegend=False)
    return apply_plot_style(fig, height=520)


def chart_category_performance_heatmap(data: pd.DataFrame, category_col: str) -> go.Figure:
    ctab = pd.crosstab(data[category_col].astype(str), data["Performance_Category"].astype(str), normalize="index") * 100
    ctab = ctab.reindex(columns=PERFORMANCE_ORDER).fillna(0).round(1)
    fig = go.Figure(
        data=go.Heatmap(
            z=ctab.values,
            x=ctab.columns,
            y=ctab.index,
            colorscale="Blues",
            text=ctab.values,
            texttemplate="%{text:.1f}%",
            hovertemplate=f"{display_label(category_col)}: %{{y}}<br>Performance: %{{x}}<br>Persentase: %{{z:.1f}}%<extra></extra>",
            colorbar=dict(title="%"),
        )
    )
    fig.update_layout(
        title=f"Proporsi Performance Category per {display_label(category_col)}",
        xaxis_title="Performance Category",
        yaxis_title=display_label(category_col),
    )
    return apply_plot_style(fig, height=500)


# 10. PAGE/TAB RENDER FUNCTIONS
def render_header(data: pd.DataFrame, dataset_path: Optional[Path], risk_mode: str) -> None:
    source_text = display_dataset_path(dataset_path)
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-title">🎓 Student Performance Analytics Dashboard</div>
            <p class="hero-subtitle">Dashboard interaktif Visualisasi Data untuk eksplorasi performa akademik mahasiswa.</p>
            <div class="hero-info">
                <strong>Visualisasi Data – Kelas B</strong><br>
                Dosen Pengampu: Supriyanto<br><br>
                <strong>Anggota Kelompok:</strong><br>
                2300018407 – Agnes Putri Alfalahi<br>
                2300018437 – Alya Aulia Azzahra<br>
                2300018444 – Caressa Suchi Dabrila
            </div>
            <div class="badge-row">
                <span class="badge">📊 {len(data):,} students</span>
                <span class="badge">🧩 {data.shape[1]:,} features</span>
                <span class="badge">🧼 {int(data.isna().sum().sum()):,} missing values</span>
                <span class="badge">⚙️ {html_escape(risk_mode)}</span>
            </div>
        </div>
        <span class="data-source-pill">Data source: {html_escape(source_text)}</span>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_cards(data: pd.DataFrame, risk_col: str) -> None:
    total = len(data)
    avg_score = data["Final_Score"].mean() if "Final_Score" in data.columns and total else np.nan
    med_score = data["Final_Score"].median() if "Final_Score" in data.columns and total else np.nan
    excellent_count = int((data["Performance_Category"].astype(str) == "Excellent").sum()) if "Performance_Category" in data.columns else 0
    at_risk_count = int((data["Performance_Category"].astype(str) == "At Risk").sum()) if "Performance_Category" in data.columns else 0
    high_risk_count = int((data[risk_col].astype(str) == "High Risk").sum()) if risk_col in data.columns else 0
    avg_study = data["Hours_Studied"].mean() if "Hours_Studied" in data.columns and total else np.nan
    avg_anxiety = data["Exam_Anxiety_Score"].mean() if "Exam_Anxiety_Score" in data.columns and total else np.nan
    avg_stress = data["Stress_Level"].mean() if "Stress_Level" in data.columns and total else np.nan

    cards = [
        metric_card("Total Students", format_number(total), "Jumlah mahasiswa pada data terfilter", COLORS["primary"], "👥"),
        metric_card("Average Score", format_number(avg_score, 2), "Rata-rata Final Score", COLORS["positive"] if avg_score >= 85 else COLORS["warning"], "🎯"),
        metric_card("Median Score", format_number(med_score, 2), "Median lebih stabil terhadap outlier", COLORS["secondary"], "📌"),
        metric_card("Excellent", f"{excellent_count:,}", "Mahasiswa dengan Final Score ≥ 90", COLORS["positive"], "🏆"),
        metric_card("At Risk", f"{at_risk_count:,}", "Final Score < 60", COLORS["negative"], "⚠️"),
        metric_card("High Risk", f"{high_risk_count:,}", f"Berdasarkan {display_label(risk_col)}", COLORS["negative"], "🚨"),
        metric_card("Avg Study Hours", format_number(avg_study, 2), "Rata-rata jam belajar", COLORS["primary"], "📚"),
        metric_card("Avg Anxiety / Stress", f"{avg_anxiety:.2f} / {avg_stress:.2f}", "Rata-rata anxiety dan stress", COLORS["warning"], "🧠"),
    ]
    render_metric_grid(cards)


def render_dynamic_insights(data: pd.DataFrame, risk_col: str) -> None:
    if len(data) == 0:
        return

    st.markdown("### 🔎 Insight Otomatis dari Data Terfilter")
    top_var, top_corr = get_top_correlated_variable(data)
    if top_var is not None:
        direction = "positif" if top_corr >= 0 else "negatif"
        insight_card(
            "Faktor paling terkait dengan Final Score",
            f"{display_label(top_var)} memiliki korelasi {direction} paling kuat terhadap Final Score pada data terfilter (r = {top_corr:.2f}).",
            COLORS["primary"] if top_corr >= 0 else COLORS["negative"],
        )

    if all(col in data.columns for col in ["Stress_Category", "Anxiety_Category", "Final_Score"]):
        low_group = data[(data["Stress_Category"].astype(str) == "Low") & (data["Anxiety_Category"].astype(str) == "Low")]
        high_group = data[(data["Stress_Category"].astype(str) == "High") & (data["Anxiety_Category"].astype(str) == "High")]
        if len(low_group) > 0 and len(high_group) > 0:
            insight_card(
                "Kombinasi stress dan anxiety terlihat penting",
                f"Kelompok Low Stress + Low Anxiety memiliki rata-rata Final Score {low_group['Final_Score'].mean():.2f}, sedangkan High Stress + High Anxiety {high_group['Final_Score'].mean():.2f}.",
                COLORS["warning"],
            )

    if all(col in data.columns for col in [risk_col, "Final_Score"]):
        high_risk = data[data[risk_col].astype(str) == "High Risk"]
        high_risk_pct = len(high_risk) / len(data) * 100 if len(data) else 0
        insight_card(
            "Segmentasi risiko",
            f"Terdapat {len(high_risk):,} mahasiswa High Risk ({high_risk_pct:.2f}% dari data terfilter). Rata-rata Final Score kelompok ini adalah {high_risk['Final_Score'].mean():.2f} jika kelompok tersedia.",
            COLORS["negative"] if len(high_risk) else COLORS["positive"],
        )


def render_overview_tab(data: pd.DataFrame, risk_col: str) -> None:
    render_kpi_cards(data, risk_col)
    render_dynamic_insights(data, risk_col)

    section_note(
        "Tab ini memberikan gambaran umum performa mahasiswa: nilai rata-rata, distribusi Final Score, komposisi Performance Category, dan indikator risiko utama."
    )

    col1, col2 = st.columns([1.45, 1], gap="large")
    with col1:
        safe_plotly_chart(chart_final_score_distribution(data), key="overview_distribution")
    with col2:
        safe_plotly_chart(chart_average_score_gauge(data), key="overview_gauge")

    col3, col4 = st.columns([1, 1], gap="large")
    with col3:
        safe_plotly_chart(chart_performance_composition(data), key="overview_performance")
    with col4:
        safe_plotly_chart(chart_risk_summary(data, risk_col), key="overview_risk")


def render_academic_tab(data: pd.DataFrame, risk_col: str) -> None:
    section_note(
        "Bagian ini berfokus pada academic drivers: jam belajar, attendance, tutoring, dan riwayat GPA. Visualisasi dipilih untuk menjelaskan hubungan antarvariabel kuantitatif terhadap Final Score."
    )

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        safe_plotly_chart(chart_correlation_bar(data), key="academic_corr")
    with col2:
        if all(col in data.columns for col in ["Tutoring_Sessions_Per_Week", "Final_Score"]):
            safe_plotly_chart(chart_tutoring_effect(data), key="academic_tutoring")

    col3, col4 = st.columns([1.15, 1], gap="large")
    with col3:
        if all(col in data.columns for col in ["Hours_Studied", "Final_Score"]):
            safe_plotly_chart(
                chart_scatter_with_trend(
                    data,
                    x_col="Hours_Studied",
                    y_col="Final_Score",
                    color_col="Performance_Category",
                    title="Hubungan Jam Belajar dan Final Score",
                    labels={"Hours_Studied": "Jam Belajar", "Final_Score": "Final Score"},
                    height=560,
                ),
                key="academic_hours_scatter",
            )
    with col4:
        if all(col in data.columns for col in ["Attendance_Group", "Final_Score"]):
            safe_plotly_chart(
                chart_group_mean_bar(
                    data,
                    group_col="Attendance_Group",
                    title="Rata-rata Final Score Berdasarkan Attendance Group",
                    order=["Low Attendance (<70%)", "Moderate Attendance (70-85%)", "High Attendance (>85%)"],
                ),
                key="academic_attendance_bar",
            )

    if all(col in data.columns for col in ["Attendance", "Final_Score"]):
        safe_plotly_chart(
            chart_scatter_with_trend(
                data,
                x_col="Attendance",
                y_col="Final_Score",
                color_col=risk_col,
                title="Attendance vs Final Score Berdasarkan Risiko",
                labels={"Attendance": "Attendance (%)", "Final_Score": "Final Score"},
                height=540,
            ),
            key="academic_attendance_scatter",
        )


def render_psychological_tab(data: pd.DataFrame, risk_col: str) -> None:
    section_note(
        "Bagian ini menyoroti risiko psikologis. Stress dan anxiety diperlakukan sebagai sinyal penting karena keduanya memiliki hubungan negatif terhadap Final Score."
    )

    col1, col2 = st.columns(2, gap="large")
    with col1:
        if all(col in data.columns for col in ["Exam_Anxiety_Score", "Final_Score"]):
            safe_plotly_chart(
                chart_scatter_with_trend(
                    data,
                    x_col="Exam_Anxiety_Score",
                    y_col="Final_Score",
                    color_col=risk_col,
                    title="Exam Anxiety vs Final Score",
                    labels={"Exam_Anxiety_Score": "Exam Anxiety Score", "Final_Score": "Final Score"},
                    height=520,
                ),
                key="psych_anxiety_scatter",
            )
    with col2:
        if all(col in data.columns for col in ["Stress_Level", "Final_Score"]):
            safe_plotly_chart(
                chart_scatter_with_trend(
                    data,
                    x_col="Stress_Level",
                    y_col="Final_Score",
                    color_col=risk_col,
                    title="Stress Level vs Final Score",
                    labels={"Stress_Level": "Stress Level", "Final_Score": "Final Score"},
                    height=520,
                ),
                key="psych_stress_scatter",
            )

    col3, col4 = st.columns([1.1, 1], gap="large")
    with col3:
        if all(col in data.columns for col in ["Stress_Category", "Anxiety_Category", "Final_Score"]):
            safe_plotly_chart(chart_stress_anxiety_heatmap(data), key="psych_heatmap")
    with col4:
        if all(col in data.columns for col in [risk_col, "Performance_Category"]):
            safe_plotly_chart(chart_risk_performance_stack(data, risk_col), key="psych_stack")


def render_segmentation_tab(data: pd.DataFrame, risk_col: str) -> None:
    section_note(
        "Tab ini digunakan untuk segmentasi mahasiswa. Gunakan definisi risiko di sidebar untuk membedakan segmentasi pasca-evaluasi dan early-warning."
    )

    high_risk_df = data[data[risk_col].astype(str) == "High Risk"].copy() if risk_col in data.columns else pd.DataFrame()
    high_risk_pct = len(high_risk_df) / len(data) * 100 if len(data) else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("High Risk Students", f"{len(high_risk_df):,}", f"{high_risk_pct:.2f}% dari data")
    if len(high_risk_df) > 0 and "Final_Score" in high_risk_df.columns:
        col2.metric("Avg Score High Risk", f"{high_risk_df['Final_Score'].mean():.2f}")
    else:
        col2.metric("Avg Score High Risk", "-")
    if len(high_risk_df) > 0 and "Hours_Studied" in high_risk_df.columns:
        col3.metric("Avg Study Hours High Risk", f"{high_risk_df['Hours_Studied'].mean():.2f}")
    else:
        col3.metric("Avg Study Hours High Risk", "-")

    if len(high_risk_df) > 0:
        section_note(
            f"Prioritas monitoring: terdapat {len(high_risk_df):,} mahasiswa High Risk. Kelompok ini dapat dijadikan target intervensi akademik seperti tutoring, konseling, atau monitoring attendance.",
            kind="danger",
        )

    col4, col5 = st.columns([1.3, 1], gap="large")
    with col4:
        if all(col in data.columns for col in ["Hours_Studied", "Exam_Anxiety_Score", "Attendance", "Final_Score"]):
            safe_plotly_chart(
                chart_scatter_with_trend(
                    data,
                    x_col="Hours_Studied",
                    y_col="Exam_Anxiety_Score",
                    color_col=risk_col,
                    size_col="Attendance",
                    title="Bubble Chart: Study Hours, Anxiety, Attendance, dan Risiko",
                    labels={"Hours_Studied": "Jam Belajar", "Exam_Anxiety_Score": "Exam Anxiety", "Attendance": "Attendance"},
                    height=570,
                    opacity=0.68,
                ),
                key="segmentation_bubble",
            )
    with col5:
        if risk_col in data.columns:
            safe_plotly_chart(chart_risk_summary(data, risk_col), key="segmentation_risk_summary")

    if risk_col in data.columns:
        summary_cols = available_cols(
            data,
            [
                risk_col,
                "Final_Score",
                "Hours_Studied",
                "Attendance",
                "Stress_Level",
                "Exam_Anxiety_Score",
                "Screen_Time",
                "Tutoring_Sessions_Per_Week",
            ],
        )
        numeric_summary_cols = [col for col in summary_cols if col != risk_col]
        if numeric_summary_cols:
            st.markdown("### Profil Rata-rata per Segmen Risiko")
            summary = (
                data.groupby(risk_col, observed=True)[numeric_summary_cols]
                .mean()
                .reindex(RISK_ORDER)
                .round(2)
                .reset_index()
            )
            summary = summary.rename(columns={col: display_label(col) for col in summary.columns})
            st.dataframe(summary, use_container_width=True, hide_index=True)

    st.markdown("### Tabel Mahasiswa High Risk")
    table_cols = available_cols(
        high_risk_df,
        [
            "Student_ID",
            "Final_Score",
            "Performance_Category",
            risk_col,
            "Hours_Studied",
            "Attendance",
            "Stress_Level",
            "Exam_Anxiety_Score",
            "Screen_Time",
            "Tutoring_Sessions_Per_Week",
            "Study_Method",
            "Family_Income_Level",
        ],
    )
    if high_risk_df.empty:
        st.success("Tidak ada mahasiswa High Risk pada filter saat ini.")
    else:
        high_risk_display = high_risk_df[table_cols].sort_values("Final_Score")
        high_risk_display = high_risk_display.rename(columns={col: display_label(col) for col in high_risk_display.columns})
        st.dataframe(high_risk_display, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Download High Risk Students",
            data=make_download_csv(high_risk_df[table_cols]),
            file_name="high_risk_students.csv",
            mime="text/csv",
            use_container_width=True,
        )


def render_category_tab(data: pd.DataFrame) -> None:
    section_note(
        "Tab ini bersifat eksploratif. Pilih satu variabel kategorikal untuk membandingkan distribusi dan rata-rata Final Score antar-kelompok."
    )

    category_options = available_cols(
        data,
        [
            "Study_Method",
            "Diet_Quality",
            "Internet_Quality",
            "Family_Income_Level",
            "Part_Time_Job",
            "Extracurricular",
            "Gender",
            "Study_Hours_Group",
            "Attendance_Group",
            "Sleep_Category",
            "Screen_Time_Group",
        ],
    )
    if not category_options:
        st.warning("Tidak ada kolom kategorikal yang tersedia untuk dibandingkan.")
        return

    col1, col2 = st.columns([1, 1])
    with col1:
        selected_col = st.selectbox(
            "Pilih variabel kategori",
            category_options,
            index=0,
            format_func=display_label,
        )
    with col2:
        visual_mode = st.radio("Mode visual", ["Mean comparison", "Distribution boxplot"], horizontal=True)

    col3, col4 = st.columns([1.1, 1], gap="large")
    with col3:
        if visual_mode == "Mean comparison":
            safe_plotly_chart(
                chart_group_mean_bar(
                    data,
                    group_col=selected_col,
                    title=f"Rata-rata Final Score Berdasarkan {display_label(selected_col)}",
                ),
                key="category_mean_bar",
            )
        else:
            safe_plotly_chart(chart_category_box(data, selected_col), key="category_box")

    with col4:
        if "Performance_Category" in data.columns:
            safe_plotly_chart(chart_category_performance_heatmap(data, selected_col), key="category_perf_heatmap")

    st.markdown("### Ringkasan Statistik per Kategori")
    summary = (
        data.groupby(selected_col, observed=True)
        .agg(
            Jumlah=("Final_Score", "size"),
            Mean_Final_Score=("Final_Score", "mean"),
            Median_Final_Score=("Final_Score", "median"),
            Min_Final_Score=("Final_Score", "min"),
            Max_Final_Score=("Final_Score", "max"),
        )
        .sort_values("Mean_Final_Score", ascending=False)
        .round(2)
        .reset_index()
    )
    summary = summary.rename(columns={col: display_label(col) for col in summary.columns})
    st.dataframe(summary, use_container_width=True, hide_index=True)


def render_methodology_tab(raw_data: pd.DataFrame, data: pd.DataFrame, dataset_path: Optional[Path], risk_mode: str) -> None:
    section_note(
        "Bagian metodologi menunjukkan transparansi proses: sumber data, data profiling, cleaning, outlier detection, statistik deskriptif, dan Master Matrix Tipe Data."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Raw Rows", f"{len(raw_data):,}")
    col2.metric("Clean Rows", f"{len(data):,}")
    col3.metric("Total Columns", f"{data.shape[1]:,}")
    col4.metric("Missing Values", f"{int(data.isna().sum().sum()):,}")

    if dataset_path:
        st.markdown(f"**Dataset path:** `{display_dataset_path(dataset_path)}`")
    st.markdown(f"**Risk mode aktif:** `{display_label(risk_mode)}`")

    with st.expander("1. Data Profiling", expanded=True):
        st.dataframe(profile_table(data), use_container_width=True, hide_index=True)

    with st.expander("2. Statistik Deskriptif Variabel Numerik", expanded=True):
        desc = describe_numeric(data)
        st.dataframe(desc, use_container_width=True, hide_index=True)

    with st.expander("3. Missing Value dan Duplicate", expanded=True):
        missing_summary = pd.DataFrame(
            {
                "Komponen": ["Missing value total", "Duplicate rows", "Duplicate Student_ID"],
                "Jumlah": [
                    int(data.isna().sum().sum()),
                    int(data.duplicated().sum()),
                    int(data["Student_ID"].duplicated().sum()) if "Student_ID" in data.columns else 0,
                ],
            }
        )
        st.dataframe(missing_summary, use_container_width=True, hide_index=True)
        section_note(
            "Keputusan cleaning: missing value numerik diisi median jika ada, kategorikal diisi 'Unknown' jika ada, dan duplicate rows dihapus. Pada dataset yang sudah dibersihkan, missing value dan duplicate tidak ditemukan."
        )

    with st.expander("4. Outlier Detection dengan IQR", expanded=True):
        outlier_df = outlier_summary(data)
        if outlier_df.empty:
            st.info("Tidak ada kolom flag outlier IQR yang tersedia.")
        else:
            st.dataframe(outlier_df, use_container_width=True, hide_index=True)
            fig = px.bar(
                outlier_df,
                x="Variabel",
                y="Jumlah Outlier",
                color="Jumlah Outlier",
                color_continuous_scale="Oranges",
                text=outlier_df["Persentase"].map(lambda x: f"{x:.2f}%"),
                title="Jumlah Outlier IQR per Variabel",
            )
            fig.update_traces(textposition="outside", marker_line_width=0.7, marker_line_color="white")
            fig.update_layout(coloraxis_showscale=False)
            safe_plotly_chart(apply_plot_style(fig, height=500), key="method_outlier_bar")
        section_note(
            "Keputusan analitis: outlier tidak dihapus otomatis karena dapat merepresentasikan sinyal penting, seperti mahasiswa dengan nilai sangat rendah, jam belajar ekstrem, atau anxiety tinggi. Anomali Previous_GPA di atas 4 ditandai dan dicapping menjadi 4 karena skala GPA diasumsikan maksimum 4."
        )

    with st.expander("5. Master Matrix Tipe Data", expanded=True):
        matrix = read_master_matrix()
        st.dataframe(matrix, use_container_width=True, hide_index=True)

    with st.expander("6. Download Dataset", expanded=True):
        st.download_button(
            "⬇️ Download cleaned / filtered dataset",
            data=make_download_csv(data),
            file_name="cleaned_student_performance_from_streamlit.csv",
            mime="text/csv",
            use_container_width=True,
        )


# 11. MAIN APP
def main() -> None:
    inject_css()

    dataset_path = find_dataset_path()
    uploaded_file = None

    if dataset_path is None:
        st.warning("Dataset belum ditemukan otomatis. Silakan upload file CSV.")
        uploaded_file = st.file_uploader("Upload student_performance_finalscore.csv atau cleaned_student_performance.csv", type=["csv"])
        if uploaded_file is None:
            st.stop()
        raw_df = pd.read_csv(uploaded_file)
    else:
        raw_df = load_csv_from_path(str(dataset_path))

    data = prepare_dataset(raw_df)

    required_cols = ["Final_Score", "Hours_Studied", "Exam_Anxiety_Score", "Stress_Level", "Attendance"]
    missing_required = [col for col in required_cols if col not in data.columns]
    if missing_required:
        st.error(f"Kolom penting tidak ditemukan: {', '.join(missing_required)}")
        st.stop()

    filtered_data, risk_col, risk_mode = build_sidebar_filters(data)

    render_header(filtered_data, dataset_path, risk_mode)

    if filtered_data.empty:
        st.warning("Tidak ada data yang cocok dengan kombinasi filter saat ini. Klik reset filter atau ubah rentang filter.")
        st.stop()

    tabs = st.tabs(
        [
            "🏠 Executive Overview",
            "📚 Academic Drivers",
            "🧠 Psychological Risk",
            "🎯 Student Segmentation",
            "🧩 Category Comparison",
            "🧼 Data Quality & Methodology",
        ]
    )

    with tabs[0]:
        render_overview_tab(filtered_data, risk_col)

    with tabs[1]:
        render_academic_tab(filtered_data, risk_col)

    with tabs[2]:
        render_psychological_tab(filtered_data, risk_col)

    with tabs[3]:
        render_segmentation_tab(filtered_data, risk_col)

    with tabs[4]:
        render_category_tab(filtered_data)

    with tabs[5]:
        render_methodology_tab(raw_df, filtered_data, dataset_path, risk_mode)

    st.markdown("---")
    st.caption(
        "Dashboard ini dikembangkan untuk proyek Visualisasi Data. Menghasilkan Insight Melalui Data Storytelling dan Interaktivitas."
    )


if __name__ == "__main__":
    main()
