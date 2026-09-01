from app.main import Telemetry, health_score, find_alerts

def test_normal_reading():
    data=Telemetry(temperature=30,humidity=50,voltage=12,current=2,signal_strength=-60)
    assert health_score(data)==100
    assert find_alerts(data)==[]

def test_high_temperature():
    data=Telemetry(temperature=80,humidity=50,voltage=12,current=2,signal_strength=-60)
    assert health_score(data)<100
    assert any("temperature" in message.lower() for _,message in find_alerts(data))
