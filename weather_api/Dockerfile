FROM python:3.11


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY /backend/requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN python3 -m spacy download ru_core_news_sm

COPY /backend .

EXPOSE 8000

CMD python manage.py makemigrations
CMD python manage.py migrate
CMD python manage.py add_cities
CMD python manage.py runserver 0.0.0.0:8000