# 📡 AI Telemetry Anomaly Investigator

A Streamlit dashboard for ingesting, profiling, visualising, and detecting anomalies in telemetry CSV data — built as a multi-day project toward a full ML-powered anomaly-detection pipeline.

---

## Day 1 — Data Ingestion & Profiling

| Feature | Details |
|---|---|
| CSV Upload | Drag-and-drop via sidebar; size guard, encoding & parse error handling |
| Data Preview | Scrollable table with configurable row count (slider) |
| Dataset Metrics | Total rows, columns, missing values, duplicate rows |
| Data Quality Panel | Per-column missing-value breakdown + duplicate row alert |
| Descriptive Statistics | `min / max / mean / std / percentiles` for all numeric columns |
| Column Summary | Dtype, missing count & %, unique values — shown in sidebar |
| Interactive Line Chart | Multi-signal Plotly chart; configurable X and Y axes |

---

## Day 2 — Statistical Anomaly Detection

| Feature | Details |
|---|---|
| Z-Score Detection | Flags rows where `|z| > threshold` (configurable 1–6, default 3) |
| IQR Detection | Flags rows outside `[Q1 − 1.5×IQR, Q3 + 1.5×IQR]` fence |
| Anomaly Metrics | Cards: total anomalies, anomalous rows, affected columns, method used |
| Anomaly Table | Scrollable results table with `row_index`, `column`, `value`, `method` |
| Signal Viewer | Line chart with red anomaly markers overlaid per signal |
| Download | Export full anomaly table as `anomaly_report.csv` |

---

## Day 3 — ML-Based Anomaly Detection

| Feature | Details |
|---|---|
| Isolation Forest | sklearn `IsolationForest`; configurable contamination (0.01–0.20) |
| DBSCAN | sklearn `DBSCAN` with `StandardScaler`; configurable `eps` and `min_samples` |
| Anomaly Scatter | 2-D scatter with normal (blue) vs anomaly (red) colouring for each method |
| Score Distribution | Histogram of Isolation Forest decision-function scores |
| Method Comparison | Table + bar chart comparing anomaly counts: Z-Score / IQR / IF / DBSCAN |
| Export | Download `anomaly_results.csv` with `row_index, method, anomaly_score, anomaly_label` |

---

## Project Structure

```
AI_Telemetry_Anomaly_Investigator/
│
├── app.py                  # Main Streamlit application (Day 1 + 2 + 3)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── sample_telemetry.csv    # Sample data for quick testing
└── utils/
    ├── __init__.py
    ├── anomaly.py          # Statistical detectors: Z-Score, IQR
    └── ml_anomaly.py       # ML detectors: Isolation Forest, DBSCAN
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

The app opens automatically at **http:// TO BE DECLARED**

---

## Using the Dashboard

1. **Upload** any telemetry CSV via the sidebar file uploader.
2. **Review** the four metric cards for a quick data health snapshot.
3. **Inspect** the Data Quality panel for missing value and duplicate warnings.
4. **Browse** the raw data preview (use the slider for more rows).
5. **Explore** descriptive statistics for all numeric columns.
6. **Plot** signals using the X / Y axis controls in the sidebar.
7. **Detect (statistical)** — choose Z-Score or IQR in the sidebar and review the anomaly table and highlighted chart.
8. **Detect (ML)** — scroll to the *ML Anomaly Detection* section:
   - **Isolation Forest tab**: select columns → adjust contamination → click *Run Isolation Forest*
   - **DBSCAN tab**: select columns → adjust eps / min_samples → click *Run DBSCAN*
9. **Compare** — the *Method Comparison* table and bar chart appear below the ML tabs once methods have been run.
10. **Export** — use the download buttons to save results as CSV.

---

## Sample CSV Format

```
timestamp,cpu_pct,mem_pct,latency_ms,error_rate
2024-01-01 00:00:00,12.4,54.1,23.1,0.001
2024-01-01 00:00:05,15.2,54.3,24.8,0.000
2024-01-01 00:00:10,88.7,79.2,312.4,0.043
```

The `sample_telemetry.csv` included in the project is ready to use.

---

## Tech Stack

- **Python 3.11+**
- **Streamlit** — dashboard framework
- **Pandas** — data loading and profiling
- **Plotly** — interactive visualisation
- **scikit-learn** — Isolation Forest, DBSCAN, StandardScaler
- **NumPy** — numerical operations

---

## Roadmap

| Day | Focus | Status |
|---|---|---|
| Day 1 | Data ingestion, profiling, interactive visualisation | ✅ Done |
| Day 2 | Statistical anomaly detection (Z-Score, IQR) | ✅ Done |
| Day 3 | ML-based detection (Isolation Forest, DBSCAN) | ✅ Done |
| Day 4 | Alerting, export, and reporting | ⬜ Planned |
| Day 5 | LLM-powered investigation assistant | ⬜ Planned |
