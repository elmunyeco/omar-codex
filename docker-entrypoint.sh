#!/bin/sh
set -eu

cd /app/hhcc

if [ "${USE_SANDBOX_DB:-0}" != "1" ] && [ "${RUN_MIGRATIONS_ON_STARTUP:-1}" != "0" ]; then
  python - <<'PY'
import os
import socket
import time

host = os.environ.get("DB_HOST", "db")
port = int(os.environ.get("DB_PORT", "3306"))
deadline = time.time() + 60

while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            break
    except OSError:
        if time.time() > deadline:
            raise SystemExit(f"DB no disponible en {host}:{port}")
        time.sleep(1)
PY
  python manage.py migrate --noinput
fi

exec "$@"
