import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile
import uvicorn
import uuid
import json

from YOLO import predict_YOLO

load_dotenv()


if not os.path.exists("uploads"):
    os.makedirs("uploads")

app = FastAPI(title="YOLO API")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict/")
async def predict(file: UploadFile):
    try:
        file_id = str(uuid.uuid4())
        with open(f"uploads/{file_id}.jpg", "wb") as f:
            f.write(file.file.read())

        photo_path = f"uploads/{file_id}.jpg"
        modelYOLO = predict_YOLO(photo_path, file_id)

        with open(f"predictions/{file_id}/{file_id}.json") as f:
            data = json.load(f)

        if not modelYOLO:
            raise HTTPException(status_code=404, detail="No se pudo procesar la imagen")

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
