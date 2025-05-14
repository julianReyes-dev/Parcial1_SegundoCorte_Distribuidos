import os
import uuid
from fastapi import FastAPI, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Optional
from .models import ImageStatus, ImageMetadata
from .rabbitmq import send_to_processing_queue
from .utils import save_upload_file

app = FastAPI()

image_db: Dict[str, ImageMetadata] = {}

class UploadResponse(BaseModel):
    image_id: str
    status: str
    message: str

class StatusResponse(BaseModel):
    image_id: str
    status: str
    details: Optional[dict]
    error: Optional[str]

@app.post("/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile):
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed"
        )

    image_id = str(uuid.uuid4())
    
    file_path = await save_upload_file(file, image_id)
    
    # Revisar metadata!
    image_db[image_id] = ImageMetadata(
        id=image_id,
        original_filename=file.filename,
        file_path=file_path,
        status=ImageStatus.UPLOADED,
        details={}
    )
    
    await send_to_processing_queue(image_id)
    
    return UploadResponse(
        image_id=image_id,
        status="uploaded",
        message="Image uploaded successfully and queued for processing"
    )

@app.get("/status/{image_id}", response_model=StatusResponse)
async def get_status(image_id: str):
    if image_id not in image_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    metadata = image_db[image_id]
    
    return StatusResponse(
        image_id=image_id,
        status=metadata.status.value,
        details=metadata.details,
        error=metadata.error
    )