#!/bin/bash

echo "Starting Micromobility Speed Detection System..."
source /home/lrincon/Desktop/micromobility-speed-detection-system/.venv/bin/activate
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
python -m src.main