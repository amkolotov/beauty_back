FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app
RUN mkdir logs staticfiles media

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
