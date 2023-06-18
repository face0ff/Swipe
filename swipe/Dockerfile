# syntax=docker/dockerfile:1
FROM python:3.9

WORKDIR /swipe/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get -y install gcc python3-dev musl-dev
# copy project
COPY . .
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y make
