FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "--worker-class", "gthread", "-w", "1", "--threads", "8", "-b", "0.0.0.0:5000", "--timeout", "150", "app:app"]
