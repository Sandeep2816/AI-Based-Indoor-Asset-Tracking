import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from ml_positioning import RSSIPositionModel

X=[]
y=[]

with open("data/training_rssi.csv",newline="") as f:
    for row in csv.DictReader(f):
        X.append([row[a] for a in ["A1","A2","A3","A4"]])
        y.append([row["x"],row["y"]])

model=RSSIPositionModel()
model.train(X,y)
model.save()
print("Saved position_model.pkl")
