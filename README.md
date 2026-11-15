# Heart Disease Prediction API (FastAPI + Docker + Render)

An end-to-end machine learning REST API built with **FastAPI**, containerized using **Docker**, and deployed on **Render**. The service predicts the presence of heart disease based on 13 clinical attributes using a scikit-learn `RandomForestClassifier` trained on the Heart Disease dataset.

> **Disclaimer:** This project is built for educational and deployment demonstration purposes only and should not be used as a medical diagnostic tool.

- **Live Deployment URL (Render):** [https://heart-disease-api-vg97.onrender.com](https://heart-disease-api-vg97.onrender.com/)
- **Interactive Swagger UI Docs:** [https://heart-disease-api-vg97.onrender.com/docs](https://heart-disease-api-vg97.onrender.com/docs)

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
```

---

## API Endpoints

| Method | Endpoint | Description | Sample Response |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Verifies that the API service is running | `{"status": "healthy"}` |
| `GET` | `/info` | Returns the trained model architecture and 13 feature names | `{"model_type": "RandomForestClassifier", "features": [...]}` |
| `POST` | `/predict` | Accepts 13 clinical attributes and predicts heart disease presence | `{"heart_disease": false}` |
| `GET` | `/docs` | Interactive Swagger UI for testing endpoints in the browser | Web Interface |

Invalid inputs (missing fields or wrong data types) automatically return an **HTTP 422 Unprocessable Entity** response with field-level validation details powered by Pydantic.

---

## Input Features (`/predict`)

The `/predict` endpoint validates the following 13 clinical parameters:

- `age`: Age in years (`int`)
- `sex`: Sex (`1` = male, `0` = female) (`int`)
- `cp`: Chest pain type (`0`–`3`) (`int`)
- `trestbps`: Resting blood pressure in mm Hg (`int`)
- `chol`: Serum cholesterol in mg/dl (`int`)
- `fbs`: Fasting blood sugar > 120 mg/dl (`1` = true, `0` = false) (`int`)
- `restecg`: Resting electrocardiographic results (`0`–`2`) (`int`)
- `thalach`: Maximum heart rate achieved (`int`)
- `exang`: Exercise-induced angina (`1` = yes, `0` = no) (`int`)
- `oldpeak`: ST depression induced by exercise relative to rest (`float`)
- `slope`: Slope of the peak exercise ST segment (`0`–`2`) (`int`)
- `ca`: Number of major vessels colored by fluoroscopy (`0`–`3`) (`int`)
- `thal`: Thalassemia blood disorder status (`0`–`3`) (`int`)

---

## 1. Model Training

The pre-trained `model/heart_model.joblib` file is already committed to this repository so the Docker container can run out of the box. To retrain the model locally:

```bash
pip install -r requirements.txt
python train.py
```

- `train.py` reads `data/heart.csv` (or falls back to synthetic clinical data if the CSV is absent), splits the data into 80% train and 20% test sets, trains a `RandomForestClassifier(n_estimators=100, random_state=42)`, and serializes the artifact to `model/heart_model.joblib`.

---

## 2. Running Locally (Without Docker)

Start the FastAPI development server using Uvicorn:

```bash
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` in your browser to interact with the Swagger UI.

---

## 3. Running Locally with Docker

Build and start the containerized application using Docker Compose:

```bash
docker-compose build
docker-compose up
```

Or run directly with Docker CLI:

```bash
docker build -t heart-disease-api .
docker run -p 8000:8000 heart-disease-api
```

Access the Swagger UI at `http://localhost:8000/docs`. Press `Ctrl + C` to stop the container.

---

## 4. Testing the Live API

You can test the live Render deployment directly from your terminal:

### Using cURL (Linux/macOS/Git Bash)
```bash
# 1. Health Check
curl [https://heart-disease-api-vg97.onrender.com/health](https://heart-disease-api-vg97.onrender.com/health)

# 2. Model Info
curl [https://heart-disease-api-vg97.onrender.com/info](https://heart-disease-api-vg97.onrender.com/info)

# 3. Predict Heart Disease
curl -X POST [https://heart-disease-api-vg97.onrender.com/predict](https://heart-disease-api-vg97.onrender.com/predict) \
  -H "Content-Type: application/json" \
  -d '{"age": 52, "sex": 1, "cp": 0, "trestbps": 125, "chol": 212, "fbs": 0, "restecg": 1, "thalach": 168, "exang": 0, "oldpeak": 1.0, "slope": 2, "ca": 2, "thal": 3}'
```

### Using PowerShell (Windows)
```powershell
$body = '{"age": 52, "sex": 1, "cp": 0, "trestbps": 125, "chol": 212, "fbs": 0, "restecg": 1, "thalach": 168, "exang": 0, "oldpeak": 1.0, "slope": 2, "ca": 2, "thal": 3}'
Invoke-RestMethod -Method Post -Uri "[https://heart-disease-api-vg97.onrender.com/predict](https://heart-disease-api-vg97.onrender.com/predict)" -ContentType "application/json" -Body $body
```

**Expected Output:**
```json
{
  "heart_disease": false
}
```

---

## 5. Deployment on Render (Docker)

1. Push the repository (including `model/heart_model.joblib` and `Dockerfile`) to GitHub.
2. On [Render](https://render.com), select **New + > Web Service** and connect the GitHub repository.
3. Configure the service:
   - **Language / Environment:** `Docker`
   - **Branch:** `main`
   - **Instance Type:** `Free`
4. Click **Deploy Web Service**. Render automatically injects the `$PORT` environment variable, which the `Dockerfile` entry command binds to (`--port ${PORT:-8000}`).

> **Note:** On Render's free tier, inactive web services spin down after ~15 minutes of inactivity. The first request after an idle period may take 30–50 seconds while the container wakes up.

---

## Issues Faced & Troubleshooting Log

During development, containerization, and deployment, the following real-world issues were encountered and resolved:

1. **`scikit-learn` Source Build Failure on Python 3.14 (`meson-python` / Cython error):**
   - **Issue:** Pinning older package versions (`scikit-learn==1.5.2`) on a local Windows environment running **Python 3.14** caused `pip` to fall back to building from source (`pyproject.toml`), failing due to missing Cython/Meson build wheels.
   - **Fix:** Removed rigid legacy version pins in `requirements.txt` so `pip` could install pre-built binary wheels (`scikit-learn 1.9.1`, `fastapi 0.137.1`) cleanly.
2. **Python / `scikit-learn` Version Alignment Between Local & Docker:**
   - **Issue:** Serialized `joblib` models can throw version mismatch warnings or unpickling errors if trained on Python 3.14 locally and loaded inside a Python 3.11 container.
   - **Fix:** Updated the `Dockerfile` base image to `FROM python:3.14-slim` so the containerized runtime matches the exact Python and `scikit-learn` environment used to generate `model/heart_model.joblib`.
3. **Windows PATH Issue with `uvicorn` CLI:**
   - **Issue:** Running `uvicorn app.main:app --reload` directly in PowerShell triggered a `CommandNotFoundException` because user-level `Scripts` directories were not added to the system `PATH`.
   - **Fix:** Executed Uvicorn as a Python module via `python -m uvicorn app.main:app --reload`.
4. **Remote Repository Rejection on Initial Push (`! [rejected] main -> main (fetch first)`):**
   - **Issue:** Initializing the GitHub repository with a default file created an unrelated commit history on `main`, rejecting the initial local push.
   - **Fix:** Synchronized the clean local project history to the remote `main` branch using `git push -u origin main --force`.
5. **Dynamic Port Binding on Render:**
   - **Issue:** Cloud container platforms like Render assign a dynamic port via the `$PORT` environment variable rather than strictly routing to port `8000`.
   - **Fix:** Configured the `Dockerfile` `CMD` using shell expansion (`uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`) so it defaults to `8000` locally while seamlessly binding to Render's assigned port in production.
