from registry import register_sensor

@register_sensor("ds18b20_temp_sensor")
def read_temperature() -> dict:
    """Simulates reading from a temperature sensor."""
    
    return {"type": "temperature", "value": 24.5, "unit": "C"}

@register_sensor("dht22_temp_sensor")
def read_dht22() -> dict:
    
    return {"type": "temperature", "value": 25.1, "unit": "C"}