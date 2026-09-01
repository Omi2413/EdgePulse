from datetime import datetime, timezone
from pathlib import Path
import csv
import io
import sqlite3
from app.health import evaluate_health
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "edgepulse.db"

app = FastAPI(
    title="EdgePulse API",
    description="IoT device health and telemetry monitoring platform.",
    version="0.1.0",
)

class Telemetry(BaseModel):
    temperature: float = Field(..., ge=-40, le=150)
    humidity: float = Field(..., ge=0, le=100)
    voltage: float = Field(..., ge=0, le=1000)
    current: float = Field(..., ge=0, le=500)
    signal_strength: int = Field(..., ge=-150, le=0)

class Device(BaseModel):
    name: str
    location: str = "Unassigned"

def get_db():
    """Create and return a SQLite database connection."""
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Create EdgePulse database tables if they do not exist."""
    db = get_db()

    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'offline',
            last_seen TEXT
        );

        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            voltage REAL NOT NULL,
            current REAL NOT NULL,
            signal_strength INTEGER NOT NULL,
            health_score INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            severity TEXT NOT NULL,
            message TEXT NOT NULL,
            acknowledged INTEGER NOT NULL DEFAULT 0
        );
        """
    )

    db.commit()
    db.close()

def calculate_health_score(data: Telemetry) -> int:
    """Calculate a simple 0-100 device health score."""
    score = 100

    if data.temperature > 70:
        score -= min(25, int((data.temperature - 70) / 2))

    if data.humidity > 85:
        score -= 10

    if data.voltage > 15 or data.voltage < 4:
        score -= 20

    if data.current > 8:
        score -= min(20, int((data.current - 8) * 3))

    if data.signal_strength < -100:
        score -= 15

    return max(0, min(100, score))

def find_alerts(data: Telemetry):
    """Return threshold-based alerts for a telemetry reading."""
    alerts = []

    if data.temperature > 70:
        alerts.append(
            ("warning", f"High temperature: {data.temperature:.1f} °C")
        )

    if data.voltage > 15 or data.voltage < 4:
        alerts.append(
            ("critical", f"Voltage outside range: {data.voltage:.2f} V")
        )

    if data.current > 8:
        alerts.append(
            ("warning", f"High current: {data.current:.2f} A")
        )

    if data.signal_strength < -100:
        alerts.append(
            ("warning", f"Weak signal: {data.signal_strength} dBm")
        )

    return alerts

@app.on_event("startup")
def startup():
    """Initialize the database when the API starts."""
    init_db()

@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
def dashboard():
    """Serve the EdgePulse monitoring dashboard."""
    return (BASE_DIR / "frontend/index.html").read_text(encoding="utf-8")

@app.get("/api/health", tags=["System"])
def api_health():
    """Return API availability status."""
    return {
        "status": "healthy",
        "service": "EdgePulse API",
        "version": app.version,
    }

@app.get("/api/devices", tags=["Devices"])
def list_devices():
    """Return all registered devices and their latest health score."""
    db = get_db()

    rows = db.execute(
        """
        SELECT
            d.*,
            (
                SELECT health_score
                FROM telemetry t
                WHERE t.device_id = d.id
                ORDER BY t.id DESC
                LIMIT 1
            ) AS health_score
        FROM devices d
        ORDER BY d.id
        """
    ).fetchall()

    db.close()

    return [dict(row) for row in rows]

@app.post("/api/devices", status_code=201, tags=["Devices"])
def add_device(device: Device):
    """Register a new EdgePulse device."""
    db = get_db()

    cursor = db.execute(
        "INSERT INTO devices(name, location) VALUES (?, ?)",
        (device.name, device.location),
    )

    db.commit()

    result = {
        "id": cursor.lastrowid,
        "name": device.name,
        "location": device.location,
        "status": "offline",
        "last_seen": None,
    }
    db.close()
    return result

@app.post("/api/devices/{device_id}/telemetry", tags=["Telemetry"])
def add_telemetry(device_id: int, data: Telemetry):
    """Record telemetry and evaluate device health."""
    db = get_db()

    device = db.execute(
        "SELECT id FROM devices WHERE id = ?",
        (device_id,),
    ).fetchone()

    if not device:
        db.close()
        raise HTTPException(status_code=404, detail="Device not found")

    now = datetime.now(timezone.utc).isoformat()
    score = evaluate_health(
        data.temperature,
        data.voltage,
        data.current,
        data.signal_strength,
    )["score"]

    db.execute(
        """
        INSERT INTO telemetry (
            device_id,
            timestamp,
            temperature,
            humidity,
            voltage,
            current,
            signal_strength,
            health_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            device_id,
            now,
            data.temperature,
            data.humidity,
            data.voltage,
            data.current,
            data.signal_strength,
            score,
        ),
    )

    db.execute(
        """
        UPDATE devices
        SET status = 'online',
            last_seen = ?
        WHERE id = ?
        """,
        (now, device_id),
    )

    for severity, message in find_alerts(data):
        db.execute(
            """
            INSERT INTO alerts (
                device_id,
                timestamp,
                severity,
                message
            )
            VALUES (?, ?, ?, ?)
            """,
            (device_id, now, severity, message),
        )

    db.commit()
    db.close()

    return {
        "device_id": device_id,
        "health_score": score,
    }

@app.get("/api/devices/{device_id}/telemetry", tags=["Telemetry"])
def device_telemetry(
    device_id: int,
    limit: int = Query(30, ge=1, le=500),
):
    """Return recent telemetry readings for a device."""
    db = get_db()

    rows = db.execute(
        """
        SELECT
            timestamp,
            temperature,
            humidity,
            voltage,
            current,
            signal_strength,
            health_score
        FROM telemetry
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (device_id, limit),
    ).fetchall()

    db.close()

    return [dict(row) for row in reversed(rows)]

@app.get("/api/alerts", tags=["Alerts"])
def recent_alerts(
    limit: int = Query(20, ge=1, le=100),
):
    """Return the most recent device alerts."""
    db = get_db()

    rows = db.execute(
        """
        SELECT
            a.*,
            d.name AS device_name
        FROM alerts a
        JOIN devices d ON d.id = a.device_id
        ORDER BY a.id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    db.close()

    return [dict(row) for row in rows]

@app.get("/api/stats", tags=["Statistics"])
def statistics():
    """Return dashboard-level device and health statistics."""
    db = get_db()

    result = {
        "devices": db.execute(
            "SELECT COUNT(*) FROM devices"
        ).fetchone()[0],

        "online": db.execute(
            "SELECT COUNT(*) FROM devices WHERE status = 'online'"
        ).fetchone()[0],

        "alerts": db.execute(
            "SELECT COUNT(*) FROM alerts WHERE acknowledged = 0"
        ).fetchone()[0],

        "average_health": round(
            db.execute(
                """
                SELECT COALESCE(AVG(health_score), 0)
                FROM telemetry
                """
            ).fetchone()[0]
        ),
    }

    db.close()

    return result

@app.get("/api/export", tags=["Export"])
def export_csv():
    """Export all telemetry data as a CSV file."""
    db = get_db()

    rows = db.execute(
        """
        SELECT
            d.name,
            t.timestamp,
            t.temperature,
            t.humidity,
            t.voltage,
            t.current,
            t.signal_strength,
            t.health_score
        FROM telemetry t
        JOIN devices d ON d.id = t.device_id
        ORDER BY t.id
        """
    ).fetchall()

    db.close()

    stream = io.StringIO()
    writer = csv.writer(stream)

    writer.writerow(
        [
            "device",
            "timestamp",
            "temperature",
            "humidity",
            "voltage",
            "current",
            "signal_strength",
            "health_score",
        ]
    )

    writer.writerows(tuple(row) for row in rows)
    stream.seek(0)

    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=edgepulse-telemetry.csv"
        },
    )

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "frontend"),
    name="static",
)