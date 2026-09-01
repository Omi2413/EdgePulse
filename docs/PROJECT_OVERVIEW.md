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
│   Device Status     │
│   Health Scores     │
│       Alerts        │
│  Recent Telemetry   │
└─────────────────────┘

## 5. System Architecture

--FastAPI Backend
Registering devices.
Receiving telemetry.
Validating incoming data.
Calculating health scores.
Detecting threshold violations.
Updating device status.
Returning telemetry history.
Returning recent alerts.
Providing system statistics.
Exporting telemetry as CSV.
SQLite Database

--SQLite provides storage for:
Registered devices.
Telemetry readings.
Generated alerts.


Device Simulator:
The simulator acts as a virtual edge device.

It generates telemetry readings and sends them to the backend at regular intervals. This allows the complete system to be demonstrated without requiring physical IoT hardware.

Web Dashboard:
The dashboard provides a simple monitoring interface showing:

Registered devices.
Online devices.
Open alerts.
Average health.
Device health scores.
Recent alerts.
Recent telemetry readings.


## 6. Health Monitoring

Each telemetry reading is evaluated using a basic health-scoring model.

The initial score is: 100

The score is reduced when abnormal operating conditions are detected, including:

High temperature.
High humidity.
Voltage outside the expected range.
High current.
Weak signal strength.

The resulting score is stored with the telemetry record and displayed on the dashboard.

## 7. Alert System

EdgePulse generates alerts when selected telemetry values cross defined thresholds.

Current alert conditions include:
Condition	Severity
High temperature	Warning
Voltage outside range	Critical
High current	Warning
Weak signal	Warning

Alerts are stored in the database and displayed in the dashboard.

## 8. REST API

The current API includes endpoints for:
Health checking.
Device registration.
Device listing.
Telemetry ingestion.
Telemetry history.
Recent alerts.
System statistics.
CSV telemetry export.


## 9. Technology Stack

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


## 10. Current Project Status

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

The project is intentionally being developed in small milestones so that each stage remains understandable, testable, and demonstrable.