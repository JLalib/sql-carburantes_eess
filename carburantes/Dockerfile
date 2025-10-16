FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y cron gcc libpq-dev && \
    apt-get clean

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/
COPY .env /app/.env
COPY crontab.txt /etc/cron.d/tarea-diaria

RUN chmod 0644 /etc/cron.d/tarea-diaria && \
    crontab /etc/cron.d/tarea-diaria && \
    touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
