FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p /app/uploads && mkdir -p /app/processed

ENV PYTHONPATH=/app

CMD ["python", "app/main.py"]