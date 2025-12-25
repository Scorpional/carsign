FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /app/uploads /app/data

EXPOSE 8000

# Default start command baked in (Zeabur 可不用额外设置)
CMD ["sh", "-c", "mkdir -p /app/data /app/uploads && python app/init_admin.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
