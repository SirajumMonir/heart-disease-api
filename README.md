# Heart Disease Prediction API (FastAPI + Docker + Render)

An end-to-end machine learning REST API built with **FastAPI**, containerized using **Docker**, and deployed on **Render**. The service predicts the presence of heart disease based on 13 clinical attributes using a scikit-learn `RandomForestClassifier` trained on the Heart Disease dataset.

> **Disclaimer:** This project is built for educational and deployment demonstration purposes only and should not be used as a medical diagnostic tool.

- **Live Deployment URL (Render):** https://heart-disease-api-vg97.onrender.com
- **Interactive Swagger UI Docs:** https://heart-disease-api-vg97.onrender.com/docs

---

## Project Structure

```text
heart-disease-api/
├── app/
│   ├── __init__.py        # Marks app/ as a Python package
│   ├── main.py            # FastAPI application and endpoints (/health, /info, /predict)
│   └── schemas.py         # Pydantic data models for request/response validation
├── model/
│   └── heart_model.joblib # Serialized RandomForestClassifier model
├── data/
│   └── heart.csv          # Heart Disease dataset (used during training)
├── train.py               # Model training and joblib serialization script
├── requirements.txt       # Python runtime and training dependencies
├── Dockerfile             # Docker image build instructions (Python 3.14-slim)
├── docker-compose.yml     # Multi-container orchestration for local Docker testing
└── README.md              # Comprehensive project documentation
