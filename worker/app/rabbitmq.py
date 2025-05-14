import aio_pika
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
PROCESSING_QUEUE = "image_processing"
PROCESSED_EXCHANGE = "processed_images"

async def get_connection() -> aio_pika.abc.AbstractRobustConnection:
    return await aio_pika.connect_robust(RABBITMQ_URL)