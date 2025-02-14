FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Ensure the Flask app runs on all interfaces (0.0.0.0)
CMD ["python", "app.py"]
