from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import storage   # Example using GCP
import joblib
import os

app = FastAPI()

ARTIFACT_BUCKET = os.environ.get("ARTIFACT_BUCKET", "my-bucket")
MODEL_KEY = "artifacts/current/model.joblib"
MODEL_PATH = os.path.expanduser("~/models/model.joblib")


def download_model():
    """Tải file model.joblib từ cloud storage về máy khi server khởi động."""
    if not os.path.exists(os.path.dirname(MODEL_PATH)):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Bỏ qua nếu đang chạy test hoặc local chưa có GCP credentials đầy đủ (trừ khi trên server)
    try:
        client = storage.Client()
        bucket = client.bucket(ARTIFACT_BUCKET)
        blob = bucket.blob(MODEL_KEY)
        blob.download_to_filename(MODEL_PATH)
        print("Tải model thành công.")
    except Exception as e:
        print(f"Bỏ qua tải model hoặc có lỗi: {e}")

download_model()
try:
    model = joblib.load(MODEL_PATH)
except:
    model = None


class ScoreRequest(BaseModel):
    features: list[float]


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/score")
def score(req: ScoreRequest):
    if len(req.features) != 10:
        raise HTTPException(status_code=400, detail="Expected 10 features (adult income)")
    
    if model is None:
         raise HTTPException(status_code=500, detail="Model not loaded")

    prediction = int(model.predict([req.features])[0])
    label = "thu_nhap_thap" if prediction == 0 else "thu_nhap_cao"
    
    return {"prediction": prediction, "label": label}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
