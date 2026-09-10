import subprocess
import time
import joblib
import numpy as np
from datetime import datetime

MODEL_PATH = "/home/adarsh/cnproject/models/predictive_model.pkl"

model = joblib.load(MODEL_PATH)

def get_metrics():
    cmd = ["ping", "-c", "3", "10.0.0.2"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    min_rtt = avg_rtt = max_rtt = loss = 0.0

    for line in result.stdout.split("\n"):
        if "rtt min/avg/max" in line:
            stats = line.split("=")[1].split("/")
            min_rtt = float(stats[0])
            avg_rtt = float(stats[1])
            max_rtt = float(stats[2])

        if "packet loss" in line:
            loss = float(line.split("%")[0].split()[-1])

    return [min_rtt, avg_rtt, max_rtt, loss]


print("Real-time Congestion Predictor Started\n")

while True:
    metrics = get_metrics()
    prediction = model.predict([metrics])[0]

    status = "CONGESTION DETECTED" if prediction == 1 else "Network Normal"

    print(f"[{datetime.now().strftime('%H:%M:%S')}] {status}")

    time.sleep(1)
