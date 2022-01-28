FROM python:3.9.9-slim

ARG PROXY=""
ENV HTTP_PROXY $PROXY
ENV HTTPS_PROXY $PROXY
ENV http_proxy $PROXY
ENV https_proxy $PROXY

RUN apt-get update && \
    apt-get install -y npm

RUN pip install poetry
WORKDIR /app
COPY ./pyproject.toml .
COPY ./poetry.lock .
RUN poetry config virtualenvs.create false \
    && poetry install
RUN pip list

WORKDIR /app/twitter-rater-ui
COPY ./twitter-rater-ui/package-lock.json ./twitter-rater-ui/package.json ./
RUN npm install && npm cache clean --force
COPY ./twitter-rater-ui ./
RUN npm run build

WORKDIR /app
COPY . /app

CMD ["python", "main.py"]
