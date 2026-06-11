# 📡 AI Telemetry Anomaly Investigator

A Streamlit-based dashboard for ingesting, profiling, and visualising telemetry CSV data — built as a multi-day project toward a full anomaly-detection pipeline.

---

## Day 1 — Data Ingestion & Profiling

**What's included:**

| Feature | Details |
|---|---|
| CSV Upload | Drag-and-drop via sidebar; robust error handling |
| Data Preview | Scrollable table with configurable row count |
| Dataset Metrics | Total rows, columns, missing values, duplicate rows |
| Data Quality Panel | Per-column missing-value breakdown + duplicate alert |
| Descriptive Statistics | `min / max / mean / std / percentiles` for all numeric columns |
| Column Summary | Dtype, missing count & %, unique values — shown in sidebar |
| Interactive Line Chart | Multi-signal Plotly chart; configurable X and Y axes |

---

## Project Structure

```
AI_Telemetry_Anomaly_Investigator/
│
├── data/                  # Drop sample CSV files here
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## Quickstart

### 1 — Clone / copy the project

```bash
cd AI_Telemetry_Anomaly_Investigator
```

### 2 — Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Run the app

```bash
streamlit run app.py
```

The app opens automatically at **//**

---

## Using the Dashboard

1. **Upload** any telemetry CSV using the sidebar file uploader.
2. **Review** the four metric cards at the top for a quick data health snapshot.
3. **Inspect** the Data Quality panel for missing value and duplicate row warnings.
4. **Browse** the raw data preview (use the slider to show more rows).
5. **Explore** descriptive statistics for all numeric columns.
6. **Plot** signals by selecting X-axis and Y-axis columns in the sidebar.

---

## Sample CSV Format

The app accepts any CSV. A minimal telemetry example:

```
timestamp,cpu_pct,mem_pct,latency_ms,error_rate
2024-01-01 00:00:00,12.4,54.1,23.1,0.001
2024-01-01 00:00:05,15.2,54.3,24.8,0.000
2024-01-01 00:00:10,88.7,79.2,312.4,0.043
```

Drop sample files into the `data/` folder for easy access.

---

## Tech Stack

- **Python 3.11+**
- **Streamlit** — dashboard framework
- **Pandas** — data loading and profiling
- **Plotly** — interactive visualisation

---

## Roadmap

| Day | Focus |
|---|---|
| 1 | Data ingestion, profiling, interactive visualisation |
| 2 | Statistical anomaly detection (Z-score, IQR) |
| 3 | ML-based detection (Isolation Forest, DBSCAN) |
| 4 | Alerting, export, and reporting |
| 5 | LLM-powered investigation assistant |
