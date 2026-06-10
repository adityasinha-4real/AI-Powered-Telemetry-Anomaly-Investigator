"""
AI Telemetry Anomaly Investigator — Day 1
Streamlit dashboard for ingesting, profiling, and visualising telemetry CSV data.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ── Page config (must be the very first Streamlit call) ──────────────────────
st.set_page_config(
    page_title="AI Telemetry Anomaly Investigator",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Constants ────────────────────────────────────────────────────────────────
SESSION_KEY_DF = "dataframe"
SESSION_KEY_FILENAME = "filename"
MAX_UPLOAD_MB = 100
CHART_PALETTE = [
    "#3b82f6", "#f59e0b", "#10b981", "#ef4444",
    "#8b5cf6", "#06b6d4", "#f97316", "#ec4899",
]


# ── Styling ──────────────────────────────────────────────────────────────────
def inject_css() -> None:
    """Inject custom CSS. Called once inside main() to keep module import clean."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@300;400;500;600;700&display=swap');

        /* ── Global ── */
        html, body, .stApp, .stMarkdown, .stDataFrame, button, input, select, textarea {
            font-family: 'Inter', sans-serif !important;
        }

        /* ── App background ── */
        .stApp {
            background: #f0f4f8 !important;
        }

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background: #1e2a3a !important;
            border-right: 1px solid #2d3d52;
        }
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] small {
            color: #b8c8d8 !important;
        }
        section[data-testid="stSidebar"] .sidebar-heading {
            color: #ffffff !important;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin: 1.2rem 0 0.5rem 0;
            padding-bottom: 0.35rem;
            border-bottom: 1px solid #2d3d52;
        }
        /* Sidebar title */
        section[data-testid="stSidebar"] h2 {
            color: #ffffff !important;
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em;
        }
        /* Sidebar upload area */
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
            background: #253447 !important;
            border: 1.5px dashed #3d5268 !important;
            border-radius: 8px !important;
        }
        /* Sidebar selectbox / multiselect */
        section[data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: #253447 !important;
            border-color: #3d5268 !important;
            color: #e2eaf2 !important;
        }
        /* Sidebar dataframe */
        section[data-testid="stSidebar"] [data-testid="stDataFrame"] {
            border: 1px solid #2d3d52 !important;
            border-radius: 6px !important;
        }
        /* Sidebar hr */
        section[data-testid="stSidebar"] hr {
            border-color: #2d3d52 !important;
        }

        /* ── Main canvas ── */
        .main .block-container {
            background: #f0f4f8;
            padding: 2.25rem 2.75rem 3.5rem;
            max-width: 1340px;
        }

        /* ── Page title ── */
        .page-title {
            font-size: 1.65rem;
            font-weight: 700;
            color: #0f1f2e;
            margin-bottom: 0.15rem;
            letter-spacing: -0.02em;
        }
        .page-subtitle {
            font-size: 0.88rem;
            color: #5a7184;
            margin-bottom: 2rem;
            font-weight: 400;
        }
        .page-subtitle b {
            color: #1e6fbf;
            font-weight: 600;
        }

        /* ── Section labels ── */
        .section-label {
            font-size: 0.67rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #5a7184;
            margin-bottom: 0.9rem;
            padding-bottom: 0.45rem;
            border-bottom: 2px solid #dde4ed;
        }

        /* ── Metric cards ── */
        div[data-testid="metric-container"] {
            background: #ffffff;
            border: 1px solid #dde4ed;
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            box-shadow: 0 2px 8px rgba(15, 31, 46, 0.06);
            transition: box-shadow 0.2s ease;
        }
        div[data-testid="metric-container"]:hover {
            box-shadow: 0 4px 16px rgba(15, 31, 46, 0.10);
        }
        div[data-testid="metric-container"] label {
            font-size: 0.71rem !important;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            color: #5a7184 !important;
            font-weight: 600;
        }
        div[data-testid="stMetricValue"] {
            font-family: 'IBM Plex Mono', monospace !important;
            font-size: 2.1rem !important;
            color: #0f1f2e !important;
            font-weight: 600 !important;
            letter-spacing: -0.02em;
        }
        div[data-testid="stMetricDelta"] { display: none !important; }

        /* ── Quality badges ── */
        .badge-ok {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: #f0faf4;
            border: 1px solid #a7dfbc;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            font-size: 0.85rem;
            color: #1a6638;
            margin-bottom: 0.45rem;
            width: 100%;
            font-weight: 500;
        }
        .badge-warn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: #fffaf0;
            border: 1px solid #f5c97a;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            font-size: 0.85rem;
            color: #7a4500;
            margin-bottom: 0.45rem;
            width: 100%;
            font-weight: 500;
        }
        .badge-warn b, .badge-ok b { font-weight: 700; }

        /* ── Data tables ── */
        div[data-testid="stDataFrame"] {
            background: #ffffff;
            border: 1px solid #dde4ed !important;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 1px 4px rgba(15,31,46,0.05);
        }

        /* ── Slider ── */
        div[data-testid="stSlider"] > div > div > div {
            background: #1e6fbf !important;
        }

        /* ── Divider ── */
        hr {
            border-color: #dde4ed !important;
            margin: 1.5rem 0 !important;
        }

        /* ── Empty state card ── */
        .empty-card {
            background: #ffffff;
            border: 2px dashed #c4d0dc;
            border-radius: 14px;
            padding: 3.5rem 2rem;
            text-align: center;
            margin-top: 1.5rem;
        }
        .empty-card .empty-icon { font-size: 2.8rem; margin-bottom: 0.9rem; }
        .empty-card h3 {
            color: #0f1f2e;
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .empty-card p {
            font-size: 0.9rem;
            line-height: 1.7;
            max-width: 500px;
            margin: 0 auto;
            color: #5a7184;
        }

        /* ── Streamlit default overrides ── */
        .stInfo, .stSuccess, .stWarning, .stError {
            border-radius: 8px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── Data loading ─────────────────────────────────────────────────────────────
def load_csv(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Parse an uploaded CSV file into a DataFrame.

    Returns None and surfaces a user-visible error on any failure.
    Enforces a file-size cap before attempting to read into memory.
    """
    # File-size guard — check before reading into memory
    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > MAX_UPLOAD_MB:
        st.error(
            f"File is {size_mb:.1f} MB — the limit is {MAX_UPLOAD_MB} MB. "
            "Consider sampling your data before uploading."
        )
        return None

    try:
        df = pd.read_csv(uploaded_file)
    except pd.errors.EmptyDataError:
        st.error("The CSV file is completely empty (no rows or columns).")
        return None
    except pd.errors.ParserError as exc:
        st.error(f"Could not parse the CSV — check the file format. Detail: {exc}")
        return None
    except UnicodeDecodeError:
        st.error(
            "Could not decode the file as UTF-8. "
            "Re-save your CSV with UTF-8 encoding and try again."
        )
        return None
    except Exception as exc:
        st.error(f"Unexpected error reading file: {exc}")
        return None

    if df.empty:
        st.error("The CSV has columns but no data rows. Upload a non-empty file.")
        return None

    return df


# ── Data profiling ────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def compute_profile(df: pd.DataFrame) -> dict:
    """
    Compute all profiling metrics once and cache by DataFrame identity.
    Returns a dict consumed by every render function — avoids repeated scans.
    """
    missing_per_col: pd.Series = df.isnull().sum()
    total_missing = int(missing_per_col.sum())
    duplicate_rows = int(df.duplicated().sum())
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # Per-column summary for the sidebar table
    col_summary = pd.DataFrame(
        [
            {
                "Column": col,
                "Dtype": str(df[col].dtype),
                "Missing": int(missing_per_col[col]),
                "Missing %": (
                    round(int(missing_per_col[col]) / len(df) * 100, 1) if len(df) else 0.0
                ),
                "Unique": df[col].nunique(),
            }
            for col in df.columns
        ]
    )

    # Descriptive stats for numeric columns (computed once)
    desc_stats = df[numeric_cols].describe().T if numeric_cols else pd.DataFrame()

    return {
        "total_rows": len(df),
        "total_cols": len(df.columns),
        "total_missing": total_missing,
        "duplicate_rows": duplicate_rows,
        "missing_per_col": missing_per_col,
        "numeric_cols": numeric_cols,
        "col_summary": col_summary,
        "desc_stats": desc_stats,
    }


# ── Chart builder ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def build_line_chart(
    df: pd.DataFrame,
    y_columns: tuple[str, ...],  # tuple (not list) so it's hashable for cache
    x_column: Optional[str],
) -> go.Figure:
    """
    Build a Plotly multi-trace line chart.
    x_column=None uses the DataFrame row index as the x-axis.
    Accepts y_columns as a tuple for cache-key stability.
    """
    fig = go.Figure()
    x_values = df[x_column] if x_column else df.index

    for i, col in enumerate(y_columns):
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=df[col],
                mode="lines",
                name=col,
                line=dict(color=CHART_PALETTE[i % len(CHART_PALETTE)], width=1.8),
                hovertemplate=(
                    f"<b>{col}</b><br>"
                    "x: %{x}<br>"
                    "value: %{y:.4f}"
                    "<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#fafbfc",
        font=dict(family="Inter, sans-serif", size=12, color="#334155"),
        margin=dict(l=16, r=16, t=48, b=16),
        height=440,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=12, color="#334155"),
            bgcolor="rgba(255,255,255,0)",
        ),
        xaxis=dict(
            title=dict(text=x_column if x_column else "Row Index", font=dict(size=12, color="#5a7184")),
            showgrid=True,
            gridcolor="#edf0f4",
            gridwidth=1,
            linecolor="#dde4ed",
            linewidth=1,
            tickfont=dict(size=11, color="#5a7184"),
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#edf0f4",
            gridwidth=1,
            linecolor="#dde4ed",
            linewidth=1,
            tickfont=dict(size=11, color="#5a7184"),
            zeroline=False,
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#dde4ed",
            font=dict(size=12, color="#0f1f2e"),
        ),
    )

    return fig


# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar(profile: Optional[dict], all_cols: list[str]) -> tuple:
    """
    Render sidebar controls.
    Returns (uploaded_file, x_column, selected_y_columns).
    Decoupled from DataFrame loading — returns the raw file object only.
    """
    st.sidebar.markdown("## 📡 Telemetry Investigator")
    st.sidebar.markdown("---")

    st.sidebar.markdown('<p class="sidebar-heading">Data Source</p>', unsafe_allow_html=True)
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV",
        type=["csv"],
        label_visibility="collapsed",
        help=(
            f"Upload a telemetry CSV (max {MAX_UPLOAD_MB} MB). "
            "Sensor logs, system metrics, model outputs — any tabular data works."
        ),
    )

    x_column: Optional[str] = None
    selected_y_columns: list[str] = []

    if profile is not None:
        numeric_cols = profile["numeric_cols"]

        st.sidebar.markdown('<p class="sidebar-heading">Chart Controls</p>', unsafe_allow_html=True)

        raw_x = st.sidebar.selectbox(
            "X-Axis",
            options=["(row index)"] + all_cols,
            help="Choose a timestamp or sequential column for the x-axis.",
        )
        x_column = None if raw_x == "(row index)" else raw_x

        if numeric_cols:
            selected_y_columns = st.sidebar.multiselect(
                "Y-Axis signals",
                options=numeric_cols,
                default=numeric_cols[:min(3, len(numeric_cols))],
                help="Select one or more numeric columns to overlay on the chart.",
            )
        else:
            st.sidebar.caption("No numeric columns detected in this dataset.")

        st.sidebar.markdown("---")
        st.sidebar.markdown('<p class="sidebar-heading">Column Summary</p>', unsafe_allow_html=True)
        st.sidebar.dataframe(
            profile["col_summary"],
            use_container_width=True,
            hide_index=True,
        )

    return uploaded_file, x_column, selected_y_columns


# ── Main page render functions ────────────────────────────────────────────────
def render_header(filename: Optional[str]) -> None:
    """Page title and contextual subtitle."""
    st.markdown('<div class="page-title">AI Telemetry Anomaly Investigator</div>', unsafe_allow_html=True)
    subtitle = (
        f"Day 1 — Data Ingestion &amp; Profiling &nbsp;·&nbsp; <b>{filename}</b>"
        if filename
        else "Day 1 — Data Ingestion &amp; Profiling &nbsp;·&nbsp; Upload a CSV to begin."
    )
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def render_metrics(profile: dict) -> None:
    """Four KPI cards — all values sourced from the cached profile dict."""
    st.markdown('<div class="section-label">Dataset Overview</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Rows", f"{profile['total_rows']:,}")
    with c2:
        st.metric("Total Columns", f"{profile['total_cols']:,}")
    with c3:
        st.metric("Missing Values", f"{profile['total_missing']:,}")
    with c4:
        st.metric("Duplicate Rows", f"{profile['duplicate_rows']:,}")


def render_data_quality(profile: dict) -> None:
    """Missing value and duplicate row diagnostics using pre-computed profile."""
    st.markdown('<div class="section-label">Data Quality</div>', unsafe_allow_html=True)

    col_missing, col_dupes = st.columns(2)

    with col_missing:
        st.caption("Missing Values")
        cols_with_missing = profile["missing_per_col"][profile["missing_per_col"] > 0]
        if cols_with_missing.empty:
            st.markdown(
                '<span class="badge-ok">✓ &nbsp;<b>No missing values</b></span>',
                unsafe_allow_html=True,
            )
        else:
            total_rows = profile["total_rows"]
            for col, count in cols_with_missing.items():
                pct = count / total_rows * 100
                st.markdown(
                    f'<span class="badge-warn">⚠ &nbsp;<b>{col}</b> — {count:,} missing ({pct:.1f}%)</span>',
                    unsafe_allow_html=True,
                )

    with col_dupes:
        st.caption("Duplicate Rows")
        dupe_count = profile["duplicate_rows"]
        if dupe_count == 0:
            st.markdown(
                '<span class="badge-ok">✓ &nbsp;<b>No duplicate rows</b></span>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<span class="badge-warn">⚠ &nbsp;<b>{dupe_count:,} duplicate row(s)</b> — '
                f"consider deduplication before modelling.</span>",
                unsafe_allow_html=True,
            )


def render_data_preview(df: pd.DataFrame, total_rows: int) -> None:
    """Scrollable data preview with a row-count slider."""
    st.markdown('<div class="section-label">Data Preview</div>', unsafe_allow_html=True)

    max_preview = min(200, total_rows)
    n_rows = st.slider(
        "Rows to preview",
        min_value=5,
        max_value=max_preview,
        value=min(20, max_preview),
        step=5,
    )
    st.dataframe(df.head(n_rows), use_container_width=True, height=320)


def render_descriptive_stats(profile: dict) -> None:
    """Transposed .describe() sourced from the cached profile."""
    if profile["desc_stats"].empty:
        return

    st.markdown('<div class="section-label">Descriptive Statistics</div>', unsafe_allow_html=True)
    st.dataframe(
        profile["desc_stats"].style.format("{:.4f}"),
        use_container_width=True,
    )


def render_chart(
    df: pd.DataFrame,
    x_column: Optional[str],
    selected_y_columns: list[str],
) -> None:
    """Interactive Plotly line chart. y_columns converted to tuple for cache stability."""
    st.markdown('<div class="section-label">Signal Viewer</div>', unsafe_allow_html=True)

    if not selected_y_columns:
        st.info("Select at least one numeric signal from the sidebar to display the chart.")
        return

    fig = build_line_chart(df, tuple(selected_y_columns), x_column)
    st.plotly_chart(fig, use_container_width=True)


def render_empty_state() -> None:
    """Onboarding card shown before any file is uploaded."""
    st.markdown(
        """
        <div class="empty-card">
            <div class="empty-icon">📂</div>
            <h3>No data loaded yet</h3>
            <p>
                Upload a CSV file using the sidebar to begin profiling your telemetry.
                The dashboard will surface row &amp; column counts, missing value diagnostics,
                duplicate detection, descriptive statistics, and an interactive signal chart.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    inject_css()

    # Initialise session state
    if SESSION_KEY_DF not in st.session_state:
        st.session_state[SESSION_KEY_DF] = None
    if SESSION_KEY_FILENAME not in st.session_state:
        st.session_state[SESSION_KEY_FILENAME] = None

    # Retrieve current state
    df: Optional[pd.DataFrame] = st.session_state[SESSION_KEY_DF]
    profile: Optional[dict] = compute_profile(df) if df is not None else None

    # Sidebar (needs profile + col list for controls)
    all_cols = df.columns.tolist() if df is not None else []
    uploaded_file, x_column, selected_y_columns = render_sidebar(profile, all_cols)

    # Handle new upload — update session state, invalidate cached profile
    if uploaded_file is not None:
        new_df = load_csv(uploaded_file)
        if new_df is not None:
            st.session_state[SESSION_KEY_DF] = new_df
            st.session_state[SESSION_KEY_FILENAME] = uploaded_file.name
            df = new_df
            profile = compute_profile(df)

    render_header(st.session_state[SESSION_KEY_FILENAME])

    if df is None or profile is None:
        render_empty_state()
        return

    render_metrics(profile)
    st.divider()
    render_data_quality(profile)
    st.divider()
    render_data_preview(df, profile["total_rows"])
    st.divider()
    render_descriptive_stats(profile)
    st.divider()
    render_chart(df, x_column, selected_y_columns)


if __name__ == "__main__":
    main()