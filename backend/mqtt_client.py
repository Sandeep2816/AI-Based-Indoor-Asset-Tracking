import json
import threading
import time
import paho.mqtt.client as mqtt
from config import MQTT_HOST, MQTT_PORT, MQTT_TOPIC
from positioning import estimate_position, smooth_rssi

_latest = {}
_lock = threading.Lock()
_on_update = None

def set_update_callback(callback):
    global _on_update
    _on_update = callback

def get_latest():
    with _lock:
        return json.loads(json.dumps(_latest))

def _handle_message(payload):
    try:
        data = json.loads(payload)
        anchor_id = str(data["anchor_id"])
        tag_id = str(data["tag_id"])
        rssi = float(data["rssi"])
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return

    filtered = smooth_rssi(tag_id, anchor_id, rssi)

    with _lock:
        tag = _latest.setdefault(
            tag_id,
            {"tag_id": tag_id, "anchors": {}, "position": {"x": 0, "y": 0}}
        )
        tag["anchors"][anchor_id] = round(filtered, 1)
        x, y = estimate_position(tag["anchors"])
        tag["position"] = {"x": x, "y": y}
        tag["last_seen"] = time.time()

    if _on_update:
        _on_update(tag)

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"MQTT connected: {reason_code}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    _handle_message(msg.payload.decode("utf-8"))

def start_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    thread = threading.Thread(target=client.loop_forever, daemon=True)
    thread.start()
    return client
