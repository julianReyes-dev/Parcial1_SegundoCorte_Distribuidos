import aio_pika
import os
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
PROCESSING_QUEUE = "image_processing"

async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(RABBITMQ_URL)

async def get_channel() -> aio_pika.abc.AbstractChannel:
    async with connection_pool.acquire() as connection:
        return await connection.channel()

connection_pool = Pool(get_connection, max_size=2)
channel_pool = Pool(get_channel, max_size=10)

async def send_to_processing_queue(image_id: str):
    async with channel_pool.acquire() as channel:
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=image_id.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=PROCESSING_QUEUE
        )