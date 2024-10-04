# Streamlit Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY app.py .

RUN pip install streamlit pymongo pandas

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
