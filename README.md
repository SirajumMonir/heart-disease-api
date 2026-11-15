# Heart Disease Prediction API (FastAPI + Docker)

A machine learning API built with FastAPI and Dockerized for deployment on Render.

## Endpoints
- `GET /health` - Health check
- `GET /info` - Model metadata and feature list
- `POST /predict` - Predict heart disease presence (`true`/`false`)

## Run Locally with Docker
```bash
docker-compose build
docker-compose up