"""Generate synthetic labeled RSSI training data for the ML demo."""

import csv
import math
import random
from pathlib import Path

anchors={"A1":(0,0),"A2":(10,0),"A3":(0,8),"A4":(10,8)}
out=Path("data/training_rssi.csv")
out.parent.mkdir(exist_ok=True)

with out.open("w",newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["x","y","A1","A2","A3","A4"])

    for _ in range(2500):
        x=random.uniform(0,10)
        y=random.uniform(0,8)
        values=[]
        for ax,ay in anchors.values():
            d=math.sqrt((x-ax)**2+(y-ay)**2)
            rssi=-45-22*math.log10(max(d,0.5))+random.gauss(0,2.2)
            values.append(round(rssi,2))
        writer.writerow([round(x,3),round(y,3),*values])

print(f"Wrote {out}")
