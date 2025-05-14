import asyncio
import aio_pika
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
PROCESSED_EXCHANGE = "processed_images"

async def on_message(message):
    async with message.process():
        body = message.body.decode()
        print(f"Notification: {body}")

async def main():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    
    exchange = await channel.declare_exchange(
        PROCESSED_EXCHANGE,
        aio_pika.ExchangeType.FANOUT,
        durable=True
    )
    
    queue = await channel.declare_queue(exclusive=True)
    await queue.bind(exchange)
    
    await queue.consume(on_message)
    
    print("Notification service started. Waiting for events...")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())