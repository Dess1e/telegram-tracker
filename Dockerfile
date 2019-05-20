FROM python:alpine3.7
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install -r requirements.txt
COPY . /app
RUN pip3 install -r requirements.txt
ENTRYPOINT python src/main.py

