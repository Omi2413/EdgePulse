# EdgePulse — Project Overview

## 1. Project Summary

EdgePulse is a Python-based IoT device health and telemetry monitoring platform.

My system simulates edge devices sending telemetry data to a FastAPI backend. The backend validates and processes incoming readings, calculates device health scores, detects abnormal conditions, stores the data in SQLite, and presents the latest device state through a lightweight web dashboard.

The project demonstrates the complete flow:
**Device → Telemetry → REST API → Processing → Database → Alerts → Dashboard**


## 2. Motivation

EdgePulse was developed to connect embedded and IoT concepts with backend software development.

Rather than building only a traditional CRUD application, it focuses on a realistic IoT monitoring workflow where devices continuously produce operational data and the backend converts that data into useful health and alert information.


## 3. Objectives

- Build a practical IoT telemetry backend using Python.
- Implement REST APIs for device and telemetry management.
- Store telemetry and alert data persistently.
- Evaluate device health using health-scoring logic.
- Detect abnormal device conditions using thresholds.
- Provide a simple monitoring dashboard.
- Simulate edge-device telemetry without requiring physical hardware.
- Maintain automated tests for core functionality.
- Develop the project incrementally using Git.


## 4. System Architecture

```text
┌─────────────────────┐
│   Device Simulator  │
│                     │
│     Temperature     │
│      Humidity       │
│      Voltage        │
│      Current        │
│   Signal Strength   │
└──────────┬──────────┘
           │
           │ REST Telemetry
           ▼
┌─────────────────────┐
│   FastAPI Backend   │
│                     │
│     Validation      │
│   Health Scoring    │
│   Alert Detection   │
│  Device Management  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       SQLite        │
│                     │
│       Devices       │
│      Telemetry      │
│       Alerts        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Web Dashboard    │
│                     │
│    Device Status    │
│    Health Scores    │
│       Alerts        │
│  Recent Telemetry   │
└─────────────────────┘
'''


### Architecture Components

- **Edge Devices** – Sensors and controllers generate device telemetry.
- **FastAPI Backend** – Receives telemetry, manages devices, evaluates health, and generates alerts.
- **SQLite Database** – Stores device information and telemetry data.
- **REST API** – Provides structured endpoints for device and telemetry operations.
- **Web Dashboard** – Presents device health, telemetry, alerts, and system status through a browser interface.


## Health Monitoring

EdgePulse evaluates incoming telemetry and generates a device health score based on configured operating conditions.

The monitoring system considers:
- Temperature
- Voltage
- Current
- Signal strength
- Configured operating thresholds


## Dashboard

The EdgePulse dashboard provides an operational overview of connected devices.

It displays:
- Registered devices
- Online/offline status
- Device health
- Open alerts
- Average fleet health
- Recent telemetry
- Recent alerts


## Telemetry

EdgePulse provides a telemetry view for monitoring recent device readings and operating conditions.

The telemetry interface helps visualize device data and identify abnormal operating conditions.


## Alert System

EdgePulse generates alerts when selected telemetry values cross defined thresholds.

Current alert conditions include:
    Condition	Severity
    High temperature	Warning
    Voltage outside range	Critical
    High current	Warning
    Weak signal	Warning

Alerts are stored in the database and displayed in the dashboard.


## REST API

The current API includes endpoints for:
    Health checking.
    Device registration.
    Device listing.
    Telemetry ingestion.
    Telemetry history.
    Recent alerts.
    System statistics.
    CSV telemetry export.


## Technology Stack

Backend:
    Python
    FastAPI
    Pydantic

Database:
    SQLite

Frontend:
    HTML
    CSS
    JavaScript

Testing:
    Pytest
    Simulation
    Python Requests

Development:
    Git
    GitHub
    Visual Studio Code


## Current Project Status

The initial EdgePulse milestone is functional.

The current implementation supports:
    Device registration.
    REST telemetry ingestion.
    Persistent SQLite storage.
    Health scoring.
    Threshold-based alerts.
    Device online status.
    Recent telemetry display.
    CSV export.
    Device simulation.
    Web dashboard.
    Automated testing.