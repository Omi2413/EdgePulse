# EdgePulse — Project Overview

## One-line description

**EdgePulse is a Python-based IoT device health monitor that turns simulated sensor telemetry into health scores, alerts, and an operations dashboard.**

## Portfolio description

EdgePulse demonstrates a complete small-scale telemetry workflow: simulated edge devices send sensor readings to a FastAPI backend, the backend validates and evaluates the data, SQLite stores the results, and a JavaScript dashboard presents device health and alert activity.

## Problem

Raw device telemetry is difficult to use when it is viewed only as individual sensor values. An operations view needs to answer simple questions quickly:

- Which devices are reporting?
- Which devices are healthy?
- Has something abnormal happened?
- What were the latest readings?
- Can the collected data be exported for analysis?

EdgePulse turns those raw readings into a compact monitoring workflow.

## Technical highlights

- REST API design with FastAPI
- Pydantic request validation
- SQLite persistence
- Rule-based health scoring
- Threshold-based alert generation
- Simulated multi-device telemetry
- Responsive HTML/CSS/JavaScript dashboard
- CSV data export
- Automated tests

## Current limitation

The prototype currently uses HTTP telemetry and a local simulator. MQTT, WebSocket updates, configurable thresholds, and stronger device heartbeat/offline detection are planned rather than presented as completed functionality.

## Skills demonstrated

**Backend:** Python, FastAPI, REST APIs, validation, SQLite

**IoT:** telemetry modelling, device simulation, threshold monitoring, signal/operating-condition handling

**Frontend:** HTML, CSS, JavaScript, dashboard design

**Engineering practice:** testing, documentation, incremental development, Git workflow

## Resume-style entry

**EdgePulse — IoT Device Health & Telemetry Monitor**  
Built a Python/FastAPI monitoring platform that simulates multiple IoT devices, ingests and stores telemetry in SQLite, calculates device health scores, generates threshold-based alerts, and presents fleet status through a responsive web dashboard.
