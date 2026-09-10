import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load dataset
df = pd.read_csv("/home/adarsh/cnproject/data/metrics.csv")

# Define congestion rule
df["congestion_now"] = ((df["packet_loss_percent"] > 2) | 
                        (df["avg_rtt_ms"] > 80)).astype(int)




# Features
X = df[["min_rtt_ms", "avg_rtt_ms", "max_rtt_ms", "packet_loss_percent"]]
y = df["congestion_now"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "/home/adarsh/cnproject/models/predictive_model.pkl")
print("\nPredictive model saved.")
