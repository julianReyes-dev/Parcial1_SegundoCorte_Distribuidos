import os
import time
import random
from PIL import Image, ImageDraw, ImageFont
from typing import Dict

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

async def process_image(image_id: str) -> Dict:
    # Simulate processing time
    await asyncio.sleep(random.uniform(1, 3))
    
    try:
        # Find the original file
        original_path = None
        for ext in ['jpg', 'jpeg', 'png', 'gif']:
            path = f"{UPLOAD_DIR}/{image_id}.{ext}"
            if os.path.exists(path):
                original_path = path
                break
        
        if not original_path:
            raise FileNotFoundError("Original image not found")
        
        # Open image
        img = Image.open(original_path)
        
        # 1. Resize
        img.thumbnail((800, 800))
        
        # 2. Add watermark
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((10, 10), "SAMPLE WATERMARK", (255, 255, 255), font=font)
        
        # 3. Content detection (simulated)
        content_tags = detect_content_simulated(img)
        
        # Save processed image
        processed_path = f"{PROCESSED_DIR}/{image_id}.jpg"
        img.save(processed_path, "JPEG")
        
        return {
            "status": "completed",
            "details": {
                "size": img.size,
                "content_tags": content_tags,
                "processed_path": processed_path
            }
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

def detect_content_simulated(img) -> list:
    # Simulate content detection
    tags = []
    if random.random() > 0.7:
        tags.append("nature")
    if random.random() > 0.7:
        tags.append("people")
    if random.random() > 0.7:
        tags.append("urban")
    return tags if tags else ["general"]