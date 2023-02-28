FROM python:alpine

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    addgroup -S grom && adduser -S grom -G grom

USER grom
CMD ["python", "./src/main.py"]