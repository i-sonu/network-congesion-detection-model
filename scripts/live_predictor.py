import subprocess
import pandas as pd
import joblib
from datetime import datetime

model = joblib.load("/home/adarsh/cnproject/models/predictive_model.pkl")

def collect_ping():
    cmd = ["ping", "-c", "1", "10.0.0.2"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    min_rtt = avg_rtt = max_rtt = None
    loss = None

    for line in result.stdout.split("\n"):
        if "packet loss" in line:
            loss = float(line.split("%")[0].split()[-1])
        if "rtt min/avg/max" in line:
            stats = line.split("=")[1].split("/")
            min_rtt = float(stats[0])
            avg_rtt = float(stats[1])
            max_rtt = float(stats[2])

    return min_rtt, avg_rtt, max_rtt, loss

print("Live congestion prediction started...\n")

while True:
    min_rtt, avg_rtt, max_rtt, loss = collect_ping()

    if min_rtt is None:
        continue

    sample = pd.DataFrame([{
        "min_rtt_ms": min_rtt,
        "avg_rtt_ms": avg_rtt,
        "max_rtt_ms": max_rtt,
        "packet_loss_percent": loss
    }])

    prediction = model.predict(sample)[0]

    timestamp = datetime.now().strftime("%H:%M:%S")

    if prediction == 1:
        print(f"[{timestamp}] ⚠ FUTURE CONGESTION PREDICTED")
    else:
        print(f"[{timestamp}] Network Normal")
