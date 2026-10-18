FROM python:3.11-slim
WORKDIR /app
COPY requirements-offline.txt /app/
RUN pip install --no-cache-dir -r requirements-offline.txt
COPY *.py /app/
COPY schema.sql /app/
ENV NICU_OFFLINE=1
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
