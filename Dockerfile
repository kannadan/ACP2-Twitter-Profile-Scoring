FROM python:3.9

RUN pip install poetry
WORKDIR /app
COPY ./pyproject.toml .
COPY ./poetry.lock .
RUN poetry config virtualenvs.create false \
    && poetry install
RUN pip list
COPY . /app

CMD ["python", "main.py"]
