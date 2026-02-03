FROM python:3.13-alpine

WORKDIR /app

COPY config/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "5002", "--proxy-headers"]