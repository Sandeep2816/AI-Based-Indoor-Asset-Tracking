"""Simple rectangular geofence engine."""

GEOFENCES = {
    "restricted_zone": {"x1": 7.0, "y1": 5.0, "x2": 10.0, "y2": 8.0},
    "storage_zone": {"x1": 0.0, "y1": 0.0, "x2": 4.0, "y2": 3.0},
}

def check_geofences(x, y):
    events=[]
    for name, zone in GEOFENCES.items():
        inside=(zone["x1"] <= x <= zone["x2"] and
                zone["y1"] <= y <= zone["y2"])
        events.append({"zone":name,"inside":inside})
    return events
