FROM python:3.11-slim
WORKDIR /app
COPY api/requirements-offline.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY api /app/api
ENV NICU_OFFLINE=1
EXPOSE 8000
CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
