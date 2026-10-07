# AI-Based Indoor Asset Tracking System

A real-time indoor asset tracking prototype using ESP32 BLE tags, ESP32 anchors, MQTT, RSSI-based positioning, Flask, and a browser dashboard.

## Architecture

BLE Asset Tags -> ESP32 Anchors -> MQTT Broker -> Flask Backend -> RSSI Positioning -> Live Web Dashboard

## Features

- BLE scanning from ESP32 anchors
- MQTT telemetry using anchor/{anchor_id}/rssi
- RSSI smoothing
- Weighted-centroid position estimation
- Flask REST API
- Socket.IO live updates
- Browser floor-map visualization
- Hardware-independent sample data for development
- Modular firmware, backend, frontend, and documentation

## Technology Stack

ESP32, Arduino, Bluetooth Low Energy, MQTT/Mosquitto, Python, Flask, Flask-SocketIO, NumPy, HTML, CSS, JavaScript.

## Repository Structure

    backend/
      app.py
      mqtt_client.py
      positioning.py
      config.py
    dashboard/
      index.html
      style.css
      app.js
    firmware/
      anchor/esp32_anchor.ino
      tag/ble_tag.ino
    data/sample_rssi.csv
    docs/system_architecture.md
    requirements.txt

## Running the Backend

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python backend/app.py

Open http://localhost:5000

Run a local Mosquitto MQTT broker on port 1883 before starting the application.

## MQTT Payload

    {
      "anchor_id": "A1",
      "tag_id": "TAG-01",
      "rssi": -61,
      "timestamp": 1720000000
    }

## Positioning

The prototype converts RSSI into an approximate distance using a log-distance path-loss model and then uses a weighted centroid.

x = sum(weight * anchor_x) / sum(weight)
y = sum(weight * anchor_y) / sum(weight)

This is intentionally a lightweight prototype. A production system could use calibrated path-loss parameters, trilateration, Kalman filtering, particle filtering, fingerprinting, or machine learning.

## Hardware

- 3 or more ESP32 development boards as anchors
- 1 or more BLE-capable ESP32 tags
- Wi-Fi network
- Laptop or Raspberry Pi running Mosquitto and Flask

## Security

No real credentials are stored in this repository. Configure Wi-Fi and MQTT credentials locally. For deployment, use environment variables, authenticated MQTT, and TLS.

## Future Scope

- ML-based RSSI fingerprinting
- Kalman or particle filtering
- Multi-floor tracking
- Asset battery monitoring
- Historical movement database
- Geofencing and alerts
- User authentication and role-based access
- MQTT TLS
- Mobile/PWA client

## Author

Sandeep Sahoo
B.Tech Electronics and Computer Engineering
