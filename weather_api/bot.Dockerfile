FROM python:3.11


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /bot

COPY /bot/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY /bot .

CMD python bot.py