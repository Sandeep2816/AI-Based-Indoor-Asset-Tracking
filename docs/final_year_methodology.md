# Final-Year Project Methodology

## Problem

GPS performs poorly indoors. The system estimates the position of tagged assets using BLE signal strength observed by fixed ESP32 anchors.

## Proposed pipeline

1. BLE tag advertises an identifier.
2. Anchors scan BLE advertisements.
3. Each anchor measures RSSI.
4. Anchors publish observations using MQTT.
5. Flask receives and validates observations.
6. RSSI values are smoothed.
7. The system estimates position.
8. Position and observations are stored in SQLite.
9. Geofences are evaluated.
10. Socket.IO broadcasts updates to the dashboard.

## Positioning approaches

### Baseline

Weighted RSSI centroid provides a simple deterministic baseline.

### ML model

A Random Forest regression model can learn the mapping:

RSSI(A1,A2,A3,A4) -> (x,y)

For an academic evaluation, collect labeled samples across a floor grid and compare MAE/RMSE against the baseline.

## Evaluation plan

Measure:

- Mean Absolute Error in metres
- Root Mean Squared Error
- Update latency
- Position stability
- Accuracy with different numbers of anchors
- Performance with human movement and obstacles

## Important limitation

Synthetic training data is for demonstration only. A real final-year evaluation should train and test using measurements collected from the actual deployment environment.
