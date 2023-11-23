FROM python:3.11.4-buster as base

ENV PATH="/root/.local/bin:$PATH"
ENV PORT=80
EXPOSE $PORT

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app/todo_app
COPY pyproject.toml poetry.lock /app/todo_app/

FROM base as production

RUN poetry install --without dev
COPY todo_app todo_app

ENTRYPOINT poetry run gunicorn --bind 0.0.0.0:$PORT "todo_app.app:create_app()"

FROM base as development

RUN poetry config virtualenvs.create false --local && poetry install
ENTRYPOINT poetry run flask run --host=0.0.0.0 --port=$PORT

FROM base as debug

RUN poetry config virtualenvs.create false --local && poetry install
ENTRYPOINT tail -f /dev/null