import asyncio
import os
import uuid
from aio_pika import Message, DeliveryMode, ExchangeType
from app.rabbitmq import get_connection, PROCESSING_QUEUE, PROCESSED_EXCHANGE
from app.processors import process_image

async def on_message(message):
    async with message.process():
        image_id = message.body.decode()
        print(f"Processing image: {image_id}")
        
        try:
            # Process the image (resize, watermark, content detection)
            processing_result = await process_image(image_id)
            
            # Publish to processed exchange
            await publish_processed_event(image_id, processing_result)
            
        except Exception as e:
            print(f"Error processing image {image_id}: {str(e)}")
            # In a real scenario, you might want to implement retry logic here

async def publish_processed_event(image_id: str, result: dict):
    connection = await get_connection()
    channel = await connection.channel()
    
    exchange = await channel.declare_exchange(
        PROCESSED_EXCHANGE,
        ExchangeType.FANOUT,
        durable=True
    )
    
    message_body = f"{image_id}|{result['status']}|{result.get('details', '')}"
    
    await exchange.publish(
        Message(
            body=message_body.encode(),
            delivery_mode=DeliveryMode.PERSISTENT
        ),
        routing_key=""
    )
    
    print(f"Published processed event for {image_id}")
    await channel.close()

async def main():
    connection = await get_connection()
    channel = await connection.channel()
    
    # Configure prefetch for load balancing
    await channel.set_qos(prefetch_count=1)
    
    # Declare processing queue
    queue = await channel.declare_queue(
        PROCESSING_QUEUE,
        durable=True
    )
    
    # Start consuming
    await queue.consume(on_message)
    
    print("Worker started. Waiting for messages...")
    await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())