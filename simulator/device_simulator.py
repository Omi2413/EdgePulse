import random
import time
import requests

BASE = "http://127.0.0.1:8000"

def main():
    names = [
        ("Greenhouse Sensor 01", "Greenhouse A"),
        ("Pump Controller 01", "Pump Room"),
        ("Weather Node 01", "North Field")
    ]
    ids = []
    for name, location in names:
        response = requests.post(
            f"{BASE}/api/devices",
            json={"name": name, "location": location}
        )
        if response.status_code == 201:
            ids.append(response.json()["id"])

    while True:
        for device_id in ids:
            data = {
                "temperature": round(random.uniform(28,65),1),
                "humidity": round(random.uniform(35,80),1),
                "voltage": round(random.uniform(10.5,13.2),2),
                "current": round(random.uniform(1,7.5),2),
                "signal_strength": random.randint(-95,-55)
            }
            if random.random() < 0.08:
                data["temperature"] = round(random.uniform(72,88),1)
            requests.post(f"{BASE}/api/devices/{device_id}/telemetry",json=data)
        print("Telemetry sent")
        time.sleep(3)

if __name__ == "__main__":
    main()
