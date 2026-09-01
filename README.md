# EdgePulse

EdgePulse is a Python-based IoT device health and telemetry platform designed to monitor connected edge devices, evaluate their current health, and identify abnormal operating conditions.

My project simulates the flow of telemetry from edge devices to a backend service, where the data is stored, evaluated, and presented through a lightweight monitoring dashboard.

## Why I Built It

I wanted to connect my Electronics and Telecommunication background with the Python and backend development skills I have been building.

Rather than creating another basic CRUD application, I wanted to build something closer to a real IoT monitoring workflow:

Device → Telemetry → Backend → Database → Health Evaluation → Alerts → User Dashboard

This gives the project a practical connection between embedded systems, IoT concepts, backend development, and data monitoring.

## Features

- Device registration and management
- REST API for telemetry ingestion
- SQLite-based data persistence
- Device health scoring
- Threshold-based alert detection
- Online and offline device status
- Recent telemetry readings
- CSV data export
- Device telemetry simulator
- Responsive monitoring dashboard
- Automated tests

## Technology Stack I used

**Backend**
- Python
- FastAPI
- SQLite

**Frontend**
- HTML
- CSS
- JavaScript

**Testing & Simulation**
- Pytest
- Requests
- Python-based device simulator

## Project Structure

```text
EdgePulse/
├── app/                    # FastAPI backend
├── frontend/               # Dashboard interface
├── simulator/              # Simulated IoT devices
├── tests/                  # Automated tests
├── docs/                   # Project documentation
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore