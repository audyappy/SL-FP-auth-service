FROM python:3.9-slim

WORKDIR /app

COPY ./src ./src
COPY .env .env
COPY ./data ./data

RUN pip install --no-cache-dir -r src/requirements.txt

# Run app.py when the container launches
CMD ["python", "-m", "src"]
