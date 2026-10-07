# AI-Based Indoor Asset Tracking System

A final-year engineering project for real-time indoor asset localization using BLE, ESP32 anchors, MQTT, RSSI signal processing, a Flask backend, SQLite history, geofencing, and an ML-ready positioning pipeline.

## What problem does it solve?

GPS is unreliable inside buildings. The system estimates where tagged assets are by comparing Bluetooth Low Energy signal strength observed by multiple fixed anchors.

## Architecture

    BLE Asset Tags
          |
          v
    ESP32 BLE Anchors
          |
          v
    MQTT Broker (Mosquitto)
          |
          v
    Flask Backend
       /       \
      v         v
 RSSI Model   SQLite
      |
      v
 Live Socket.IO Dashboard

## Features

- BLE asset tags and ESP32 anchors
- MQTT telemetry
- RSSI smoothing
- Weighted-centroid baseline positioning
- ML-ready Random Forest positioning model
- SQLite observation and position history
- REST APIs for assets, history, and geofences
- Real-time browser dashboard
- Rectangular geofencing
- Laptop-only synthetic movement simulator
- Synthetic training-data generator for ML experiments
- Clear separation between firmware, backend, dashboard, data, and tools

## Technology Stack

ESP32, Arduino, BLE, MQTT/Mosquitto, Python, Flask, Flask-SocketIO, SQLite, NumPy, scikit-learn, HTML, CSS, JavaScript.

## Repository Structure

    backend/
      app.py
      config.py
      database.py
      geofence.py
      ml_positioning.py
      mqtt_client.py
      positioning.py
      simulator.py
    dashboard/
      index.html
      style.css
      app.js
    firmware/
      anchor/esp32_anchor.ino
      tag/ble_tag.ino
    data/
      sample_rssi.csv
      training_rssi.csv
    docs/
      system_architecture.md
      final_year_methodology.md
    tools/
      generate_training_data.py
      train_model.py

## Quick Start

### 1. Install Python dependencies

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

For ML experiments:

    pip install -r backend/requirements-ml.txt

### 2. Start Mosquitto

Run a local MQTT broker on port 1883.

### 3. Start the backend

    python backend/app.py

Open:

    http://localhost:5000

### 4. Run without hardware

With Mosquitto running:

    python backend/simulator.py

The simulator creates a moving virtual asset and publishes RSSI values from four virtual observations. This makes the dashboard demonstrable without four ESP32 boards.

## ML Experiment

Generate a larger synthetic training dataset:

    python tools/generate_training_data.py

Train the Random Forest model:

    python tools/train_model.py

The model learns:

    RSSI(A1, A2, A3, A4) -> (x, y)

For the final academic evaluation, replace synthetic data with measurements collected at known coordinates on the actual floor.

## API

### Current assets

    GET /api/assets

### Position history

    GET /api/history

### Geofence state

    GET /api/geofences

## Positioning

The current live system uses a weighted RSSI centroid as a robust baseline. RSSI is smoothed using a short moving window before distance weighting.

The repository also contains an ML-ready Random Forest regression implementation. Keeping the deterministic baseline and ML model separate makes it possible to compare accuracy objectively.

## Final-Year Evaluation

Recommended experiment:

1. Mark a grid of known floor coordinates.
2. Record RSSI from every anchor at each point.
3. Split measurements into training and testing sets.
4. Train the Random Forest model.
5. Compare predicted coordinates with ground truth.
6. Report MAE and RMSE in metres.
7. Compare ML performance against the weighted-centroid baseline.
8. Test the effect of obstacles, people, and anchor count.

## Limitations

RSSI is sensitive to walls, human bodies, antenna orientation, multipath propagation, and radio interference. Therefore, the position is an estimate. Real deployment requires calibration and site-specific training data.

## Security

No real Wi-Fi passwords, MQTT credentials, API keys, or private configuration are committed. Keep deployment credentials in environment variables or a local configuration file excluded by .gitignore.

## Future Scope

- Real floor-plan calibration
- RSSI fingerprint database
- Kalman/particle filtering
- Multi-floor tracking
- Asset battery monitoring
- Historical movement analytics
- Advanced geofencing and alerts
- MQTT TLS and authentication
- Role-based user authentication
- Mobile/PWA client

## Author

Sandeep Sahoo
B.Tech Electronics and Computer Engineering
