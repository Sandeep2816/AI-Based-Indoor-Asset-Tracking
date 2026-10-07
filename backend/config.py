import os

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "anchor/+/rssi")

ANCHORS = {
    "A1": (0.0, 0.0),
    "A2": (10.0, 0.0),
    "A3": (0.0, 8.0),
    "A4": (10.0, 8.0),
}

RSSI_REFERENCE = int(os.getenv("RSSI_REFERENCE", "-45"))
PATH_LOSS_EXPONENT = float(os.getenv("PATH_LOSS_EXPONENT", "2.2"))
