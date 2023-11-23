FROM python:3.11.4-buster

ENV PATH="/root/.local/bin:$PATH"
ENV PORT=80
EXPOSE $PORT

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /opt/todo/app
COPY todo_app todo_app
COPY pyproject.toml .
RUN poetry install --without dev

ENTRYPOINT poetry run gunicorn --bind 0.0.0.0:$PORT "todo_app.app:create_app()"