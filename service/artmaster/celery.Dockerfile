FROM python:3

COPY requirements.txt /artmaster/requirements.txt

WORKDIR /artmaster

RUN pip install -r requirements.txt

COPY . .

WORKDIR /artmaster/artmaster

CMD NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program celery -A app.celery worker --loglevel=INFO