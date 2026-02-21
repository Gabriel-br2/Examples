from registry import register_sensor

@register_sensor("bmp280_pressure_sensor")
def read_pressure() -> dict:
    
    return {"type": "pressure", "value": 1013.25, "unit": "hPa"}