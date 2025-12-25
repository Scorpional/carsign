#!/bin/sh
set -e

# ensure working directory
cd /app

mkdir -p /app/data /app/uploads

if [ "$DEMO_STATIC" = "1" ]; then
  cd /app/demo
  echo "Starting static demo server on 8000 (DEMO_STATIC=1)"
  exec python -m http.server 8000
else
  # ensure tables exist (no alembic needed for demo)
  python - <<'PYCODE'
from app.database import Base, engine
import app.models  # noqa
Base.metadata.create_all(bind=engine)
print("Tables ensured.")
PYCODE
  python app/init_admin.py
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi
