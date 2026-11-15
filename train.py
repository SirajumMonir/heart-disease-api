import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

os.makedirs("model", exist_ok=True)

FEATURES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]

data_path = "data/heart.csv"

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    X = df[FEATURES]
    y = df["target"]
else:
    # Fallback synthetic data if CSV isn't downloaded yet
    np.random.seed(42)
    X = pd.DataFrame(np.random.randint(0, 100, size=(200, len(FEATURES))), columns=FEATURES)
    y = np.random.randint(0, 2, size=200)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "model/heart_model.joblib")
print("Model saved successfully to model/heart_model.joblib")