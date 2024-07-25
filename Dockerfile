FROM python:3.11-alpine

WORKDIR /telegram-personal-finance-bot

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt .

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk add --no-cache sqlite

COPY *.py ./
COPY db/createdb.sql ./

ENTRYPOINT ["python", "main.py"]

