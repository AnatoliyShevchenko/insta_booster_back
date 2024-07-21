FROM python:3.12.3-slim-bullseye

WORKDIR /app

RUN python -m venv /venv

ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .