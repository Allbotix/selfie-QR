from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

app = FastAPI()

# Allow all CORS (frontend JS can access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve index.html at home
@app.get("/")
def home():
    return FileResponse("index.html")

# Handle upload
@app.post("/upload")
async def upload_file(selfie: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, selfie.filename)
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(selfie.file, f)

    # Return the path that frontend can use to generate QR code
    # Using absolute URL if deployed or relative path
    return JSONResponse({"message": "File uploaded", "url": f"/{file_path}"})

# Serve uploaded files
@app.get("/uploads/{filename}")
def get_uploaded_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse({"error": "File not found"}, status_code=404)
