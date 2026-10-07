"""Publish synthetic RSSI observations for a laptop-only demonstration."""

import json
import math
import random
import time
import paho.mqtt.client as mqtt
from config import ANCHORS, MQTT_HOST, MQTT_PORT

def distance_to_rssi(distance):
    return -45 - 22 * math.log10(max(distance, 0.5))

def run(tag_id="SIM-01", seconds=60):
    client=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_start()

    anchors=list(ANCHORS.items())
    start=time.time()
    t=0.0

    while time.time()-start < seconds:
        x=5 + 4*math.sin(t/8)
        y=4 + 3*math.cos(t/11)

        for anchor_id,(ax,ay) in anchors:
            d=math.sqrt((x-ax)**2+(y-ay)**2)
            rssi=distance_to_rssi(d)+random.gauss(0,2)
            payload={
                "anchor_id":anchor_id,
                "tag_id":tag_id,
                "rssi":round(rssi,1),
                "timestamp":time.time()
            }
            client.publish(f"anchor/{anchor_id}/rssi",json.dumps(payload))

        t+=1
        time.sleep(1)

    client.loop_stop()
    client.disconnect()

if __name__=="__main__":
    run()
