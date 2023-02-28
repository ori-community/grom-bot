FROM python:alpine

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

CMD ["python", "./src/main.py"]