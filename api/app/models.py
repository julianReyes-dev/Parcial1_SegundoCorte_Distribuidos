from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict

class ImageStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ImageMetadata(BaseModel):
    id: str
    original_filename: str
    file_path: str
    status: ImageStatus
    details: Dict = {}
    error: Optional[str] = None