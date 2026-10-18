FROM python:3.11-slim
WORKDIR /app
COPY ui/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ui/app.py /app/ui/app.py
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
EXPOSE 8501
CMD ["streamlit", "run", "ui/app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
