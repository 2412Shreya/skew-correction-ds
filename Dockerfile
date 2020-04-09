FROM python:3.7-slim-buster
MAINTAINER zeotap
RUN apt-get clean && apt-get update && apt-get install -y cron
COPY . /skew-correction-prod
COPY weights-cron /etc/cron.d/weights-cron
RUN chmod 0644 /etc/cron.d/weights-cron
RUN crontab /etc/cron.d/weights-cron
RUN touch /var/log/weights-cron.log
WORKDIR /skew-correction-prod/Docker_Container
RUN pip install -r requirement.txt
CMD cron && python3 -u consumer/main.py