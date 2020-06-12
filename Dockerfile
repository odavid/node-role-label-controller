FROM python:3.7-slim AS build

RUN pip3 install poetry

COPY poetry.lock poetry.toml pyproject.toml ./
RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-dev

FROM python:3.7-slim

COPY --from=build /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages

WORKDIR /code

COPY node_role_label_controller ./node_role_label_controller

CMD ["python3", "-m", "kopf", "run", "node_role_label_controller/main.py"]