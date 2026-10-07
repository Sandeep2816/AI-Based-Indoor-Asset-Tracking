from collections import defaultdict, deque
import math
from config import ANCHORS, RSSI_REFERENCE, PATH_LOSS_EXPONENT

_HISTORY = defaultdict(lambda: deque(maxlen=5))

def smooth_rssi(tag_id, anchor_id, rssi):
    key = (tag_id, anchor_id)
    _HISTORY[key].append(float(rssi))
    return sum(_HISTORY[key]) / len(_HISTORY[key])

def rssi_to_distance(rssi):
    return 10 ** ((RSSI_REFERENCE - rssi) / (10 * PATH_LOSS_EXPONENT))

def estimate_position(observations):
    weighted = []
    for anchor_id, rssi in observations.items():
        if anchor_id not in ANCHORS:
            continue
        distance = max(rssi_to_distance(rssi), 0.05)
        weight = 1.0 / (distance * distance)
        x, y = ANCHORS[anchor_id]
        weighted.append((x, y, weight))

    if not weighted:
        return 0.0, 0.0

    total = sum(item[2] for item in weighted)
    x = sum(item[0] * item[2] for item in weighted) / total
    y = sum(item[1] * item[2] for item in weighted) / total
    return round(x, 2), round(y, 2)
