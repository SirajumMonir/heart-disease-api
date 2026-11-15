import joblib
import pandas as pd
from fastapi import FastAPI
from app.schemas import HeartDiseaseInput, PredictionOutput

app = FastAPI(
    title="Heart Disease Prediction API",
    description="FastAPI service for predicting heart disease presence",
    version="1.0.0"
)

MODEL_PATH = "model/heart_model.joblib"
model = joblib.load(MODEL_PATH)

FEATURES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/info")
def model_info():
    return {
        "model_type": type(model).__name__,
        "features": FEATURES
    }

@app.post("/predict", response_model=PredictionOutput)
def predict(data: HeartDiseaseInput):
    input_df = pd.DataFrame([data.model_dump()])
    prediction = model.predict(input_df)[0]
    return {"heart_disease": bool(prediction == 1)}