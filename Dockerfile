FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /app/uploads /app/data

# Copy start script and make executable
RUN chmod +x /app/start.sh

EXPOSE 8000

# Default start command; can switch to static demo via DEMO_STATIC=1
CMD ["sh", "/app/start.sh"]
