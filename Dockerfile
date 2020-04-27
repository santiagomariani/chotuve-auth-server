# base image with python 3
FROM python:3

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# flask envs
ENV FLASK_APP=api.py
ENV FLASK_ENV=development

ENTRYPOINT ["sh", "/app/docker-entrypoint-prod.sh"]
