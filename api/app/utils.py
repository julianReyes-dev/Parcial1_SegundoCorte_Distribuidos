import os
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(file: UploadFile, image_id: str) -> str:
    file_ext = file.filename.split(".")[-1]
    file_path = f"{UPLOAD_DIR}/{image_id}.{file_ext}"
    
    with open(file_path, "wb") as f:
        while contents := await file.read(1024 * 1024):  # 1MB chunks
            f.write(contents)
    
    return file_path