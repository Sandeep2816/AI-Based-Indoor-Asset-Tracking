from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO
from database import history, init_db
from geofence import check_geofences
from mqtt_client import get_latest, set_update_callback, start_mqtt

app = Flask(__name__, static_folder="../dashboard")
socketio = SocketIO(app, cors_allowed_origins="*")
init_db()

@app.get("/")
def index():
    return send_from_directory("../dashboard", "index.html")

@app.get("/api/assets")
def assets():
    return jsonify(list(get_latest().values()))

@app.get("/api/history")
def position_history():
    return jsonify(history())

@app.get("/api/geofences")
def geofences():
    result=[]
    for asset in get_latest().values():
        x=asset["position"]["x"]
        y=asset["position"]["y"]
        result.append({"tag_id":asset["tag_id"],"position":{"x":x,"y":y},"zones":check_geofences(x,y)})
    return jsonify(result)

def broadcast_update(asset):
    asset["geofences"]=check_geofences(asset["position"]["x"],asset["position"]["y"])
    socketio.emit("asset_update", asset)

if __name__ == "__main__":
    set_update_callback(broadcast_update)
    try:
        start_mqtt()
        print("MQTT listener started.")
    except Exception as exc:
        print(f"MQTT unavailable: {exc}")
        print("Start Mosquitto and restart the application.")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
