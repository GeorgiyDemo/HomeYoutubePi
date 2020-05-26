FROM python:3.7.4-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD rq-dashboard -u redis://redis:6379/0
