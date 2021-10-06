# syntax=docker/dockerfile:1

FROM python:3.8.12-bullseye

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

# EXPOSE 9001

CMD [ "python3", "app.py" ]

