#!/bin/bash
export PYTHONPATH=/app
exec uvicorn backend.main:app --host 0.0.0.0 --port $PORT
