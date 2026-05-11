FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src src/

COPY ./app.py .

COPY ./config config/

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]