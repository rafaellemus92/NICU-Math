FROM python:3.11-slim

WORKDIR /app

# System deps (needed by PyMuPDF, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git libglib2.0-0 libgl1 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Build context is ./api
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app

EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]