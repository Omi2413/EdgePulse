# EdgePulse

## Device Health & Telemetry Monitoring Platform

EdgePulse is a lightweight device monitoring platform built with **FastAPI, SQLite, HTML, CSS, and JavaScript**.

It collects telemetry from connected edge devices, evaluates device health, detects abnormal operating conditions, generates alerts, and presents the latest device state through a web dashboard.

## Features

- Device registration and management
- Real-time-style device health dashboard
- REST API for telemetry ingestion
- Automatic device health-score calculation
- Threshold-based alert generation
- Device online/offline status
- Recent telemetry visualization
- Recent alerts panel
- CSV telemetry export

## Architecture

```text
                    ┌───────────────────────┐
                    │     Edge Devices      │
                    │ Sensors / Controllers │
                    └──────────┬────────────┘
                               │
                               │ Telemetry
                               ▼
                    ┌───────────────────────┐
                    │     FastAPI API       │
                    │                       │
                    │   Device Management   │
                    │  Telemetry Ingestion  │
                    │   Health Evaluation   │
                    │   Alert Generation    │
                    └──────────┬────────────┘
                               │
                         ┌─────┴─────┐
                         ▼           ▼
                  ┌────────────┐ ┌────────────┐
                  │  SQLite DB │ │  REST API  │
                  └────────────┘ └──────┬─────┘
                                        │
                                        ▼
                              ┌──────────────────┐
                              │   Web Dashboard  │
                              │    HTML/CSS/JS   │
                              └──────────────────┘
```

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Omi2413/EdgePulse.git
cd EdgePulse
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the application
```bash
uvicorn app.main:app --reload
```

Open:
```text
http://127.0.0.1:8000/
```

API documentation:
```text
http://127.0.0.1:8000/docs
```

## Dashboard Preview

![EdgePulse Dashboard](docs/dashboard.png)

## Telemetry Details

![EdgePulse Telemetry](docs/telemetry.png)
