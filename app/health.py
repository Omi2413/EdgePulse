def evaluate_health(
    temperature: float,
    voltage: float,
    current: float,
    signal: float,
) -> dict:
    """
    Evaluate the health of an edge device from its latest telemetry.

    Returns a health percentage and a list of detected conditions.
    """

    score = 100
    conditions = []

    if temperature >= 80:
        score -= 30
        conditions.append("High temperature")
    elif temperature >= 65:
        score -= 15
        conditions.append("Elevated temperature")

    if voltage < 9:
        score -= 20
        conditions.append("Low voltage")
    elif voltage > 14:
        score -= 20
        conditions.append("High voltage")

    if current >= 8:
        score -= 25
        conditions.append("High current")
    elif current >= 6:
        score -= 10
        conditions.append("Elevated current")

    if signal < -85:
        score -= 15
        conditions.append("Weak signal")
    elif signal < -70:
        score -= 5
        conditions.append("Reduced signal")

    score = max(0, min(100, score))

    if score >= 80:
        status = "Healthy"
    elif score >= 50:
        status = "Warning"
    else:
        status = "Critical"

    return {
        "score": score,
        "status": status,
        "conditions": conditions,
    }