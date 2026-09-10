import subprocess
import csv
from datetime import datetime
import os

OUTPUT_FILE = "/home/adarsh/cnproject/data/metrics.csv"

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

file_exists = os.path.isfile(OUTPUT_FILE)

with open(OUTPUT_FILE, "a", newline="") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow([
            "timestamp",
            "min_rtt_ms",
            "avg_rtt_ms",
            "max_rtt_ms",
            "packet_loss_percent"
        ])

    print("Fast metric collection started... Ctrl+C to stop.")

    try:
        while True:
            min_rtt, avg_rtt, max_rtt, loss = collect_ping()
            writer.writerow([
                datetime.now().isoformat(),
                min_rtt,
                avg_rtt,
                max_rtt,
                loss
            ])
            f.flush()
    except KeyboardInterrupt:
        print("\nMetric collection stopped.")