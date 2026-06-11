"""
utils/anomaly.py — Anomaly detection for AI Telemetry Anomaly Investigator (Day 2).

Public API
----------
detect_zscore_anomalies(df, columns, threshold) -> pd.DataFrame
detect_iqr_anomalies(df, columns)               -> pd.DataFrame
build_anomaly_table(df, columns, method, **kw)  -> pd.DataFrame
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# ── Z-Score detection ─────────────────────────────────────────────────────────

def detect_zscore_anomalies(
    df: pd.DataFrame,
    columns: list[str],
    threshold: float = 3.0,
) -> pd.DataFrame:
    """
    Return a long-format DataFrame of anomalous observations using Z-Score.

    Parameters
    ----------
    df        : source DataFrame
    columns   : numeric columns to inspect
    threshold : flag rows where abs(z-score) > threshold (default 3.0)

    Returns
    -------
    DataFrame with columns [row_index, column, value, method]
    Empty DataFrame (correct schema) if no anomalies are found.
    """
    records: list[dict] = []

    for col in columns:
        series = df[col].dropna()

        # Constant-value columns have std == 0 → z-scores are undefined
        if series.std(ddof=0) == 0:
            continue

        z_scores = (series - series.mean()) / series.std(ddof=0)
        anomalous_idx = z_scores[z_scores.abs() > threshold].index

        for idx in anomalous_idx:
            records.append(
                {
                    "row_index": int(idx),
                    "column": col,
                    "value": df.at[idx, col],
                    "method": "Z-Score",
                }
            )

    return _to_anomaly_df(records)


# ── IQR detection ─────────────────────────────────────────────────────────────

def detect_iqr_anomalies(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Return a long-format DataFrame of anomalous observations using IQR fencing.

    Fence formula:
        Q1 = 25th percentile
        Q3 = 75th percentile
        IQR = Q3 − Q1
        lower = Q1 − 1.5 × IQR
        upper = Q3 + 1.5 × IQR

    Values outside [lower, upper] are flagged as anomalies.

    Returns
    -------
    DataFrame with columns [row_index, column, value, method]
    Empty DataFrame (correct schema) if no anomalies are found.
    """
    records: list[dict] = []

    for col in columns:
        series = df[col].dropna()

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        # Zero-IQR (constant or near-constant column) → no meaningful fence
        if iqr == 0:
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        anomalous_idx = series[(series < lower) | (series > upper)].index

        for idx in anomalous_idx:
            records.append(
                {
                    "row_index": int(idx),
                    "column": col,
                    "value": df.at[idx, col],
                    "method": "IQR",
                }
            )

    return _to_anomaly_df(records)


# ── Unified builder ───────────────────────────────────────────────────────────

def build_anomaly_table(
    df: pd.DataFrame,
    columns: list[str],
    method: str,
    threshold: float = 3.0,
) -> pd.DataFrame:
    """
    Dispatch to the correct detector and return the anomaly table.

    Parameters
    ----------
    df        : source DataFrame
    columns   : numeric columns to inspect
    method    : "Z-Score" | "IQR"
    threshold : used only for Z-Score

    Returns
    -------
    DataFrame with columns [row_index, column, value, method]
    """
    if not columns:
        return _to_anomaly_df([])

    if method == "Z-Score":
        return detect_zscore_anomalies(df, columns, threshold)
    elif method == "IQR":
        return detect_iqr_anomalies(df, columns)
    else:
        raise ValueError(f"Unknown method: {method!r}. Choose 'Z-Score' or 'IQR'.")


# ── Internal helpers ──────────────────────────────────────────────────────────

def _to_anomaly_df(records: list[dict]) -> pd.DataFrame:
    """Guarantee a consistent schema even when the record list is empty."""
    if records:
        return pd.DataFrame(records)[["row_index", "column", "value", "method"]]
    return pd.DataFrame(columns=["row_index", "column", "value", "method"])
