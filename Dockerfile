FROM python:3.11.4-buster as base

RUN apt-get update

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

RUN poetry install
ENTRYPOINT [ "/bin/bash", "-c", "poetry run flask run --host=0.0.0.0 --port=$PORT" ]

FROM base as debug

ENTRYPOINT [ "tail", "-f", "/dev/null" ]

FROM base as test

RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
    apt-get install ./chrome.deb -y &&\  
    rm ./chrome.deb 

RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/bin/chromedriver

RUN poetry install
COPY pytest.ini /app/todo_app/
COPY tests tests
COPY tests_e2e tests_e2e

ENTRYPOINT [ "poetry", "run", "ptw", "--poll", "todo_app" ]