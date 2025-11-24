from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cloudinary
import cloudinary.uploader
import json
from pathlib import Path

# ============ CONFIG CLOUDINARY ============
cloudinary.config(
    cloud_name="dnd427uub",
    api_key="456318294928817",
    api_secret="NH5awUrt2NriqWmgPZKk4To1gZY",
    secure=True
)

# ============ INICIALIZAR FASTAPI ============
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ============ ARCHIVO JSON DE CONTENIDO ============
BASE_DIR = Path(__file__).resolve().parent
CONTENT_PATH = BASE_DIR / "content.json"

def load_content():
    if CONTENT_PATH.exists():
        with open(CONTENT_PATH, "r") as f:
            return json.load(f)
    return {}

def save_content(data):
    with open(CONTENT_PATH, "w") as f:
        json.dump(data, f, indent=4)

# ============ ENDPOINT: OBTENER CONTENIDO ============
@app.get("/content")
def get_content():
    return load_content()

# ============ ENDPOINT: SUBIR IMAGEN ============
@app.post("/upload-image")
async def upload_image(section: str = Form(...), file: UploadFile = File(...)):

    if not file:
        raise HTTPException(400, "No file uploaded")

    # Subir a Cloudinary
    upload = cloudinary.uploader.upload(file.file)
    url = upload.get("secure_url")

    # Guardar en el JSON
    data = load_content()

    if section not in data:
        data[section] = []

    data[section].append(url)
    save_content(data)

    return {"message": "ok", "url": url}