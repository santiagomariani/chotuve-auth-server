# base image with python 3
FROM python:3.8.1-slim-buster
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y git

# flask envs
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV APP_SETTINGS=production
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/chotuve-videos-firebase-adminsdk.json

ENTRYPOINT ["sh", "/app/docker-entrypoint-prod.sh"]
