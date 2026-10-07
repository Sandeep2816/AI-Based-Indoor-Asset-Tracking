# System Architecture

## Edge Layer

BLE tags advertise an identifier. ESP32 anchors scan nearby advertisements and record RSSI.

## Transport Layer

Anchors publish observations to anchor/{anchor_id}/rssi using MQTT. MQTT decouples the hardware layer from the backend and supports multiple anchors.

## Processing Layer

The Flask backend receives MQTT messages, smooths RSSI samples, converts RSSI into approximate distance weights, and estimates the asset position using a weighted centroid.

## Presentation Layer

The REST endpoint GET /api/assets exposes current assets. Socket.IO sends real-time asset updates to the browser dashboard.

## Scaling Path

ESP32 Anchors -> MQTT Cluster -> Message Processing -> Database -> Positioning Service -> REST/WebSocket API -> Web/Mobile Clients

The positioning service can later be replaced by RSSI fingerprinting or an ML model without changing the dashboard protocol.
