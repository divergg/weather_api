# Weather API and Telegram Bot

# General description

This project consists of 2 parts: API service for receiving weather data (backend folder) and telegram bot on the frontend (bot folder)
Currently bot allows to send requests only in Russian, however API can send responses on multiple languages depending on the language code.
Backend consists of a single get endpoint and bot sends request to this endpoint.

# General structure
Backend of a project is implemented with the use of Django-Rest Framework and PostgreSQL.
Frontend is built on aiogram.
Backend is followed by the tests

# Bot description
Example of the bot execution in Russian
![pic1](https://github.com/divergg/weather_api/blob/master/weather_api/bot_example.png)

Bot understands commands 'start', and 'Узнать погоду' (Get weather data)
Any additional commands are responded with a fallback

![pic2](https://github.com/divergg/weather_api/blob/master/weather_api/fallback.png)

The main part of the logic is executet on the backend

# API description
Api has two endpoints:

http://django:8000/api/ - receives get requests with the parameters &city_name: str and &lang_code: str

http://django:8000/docs/ - swagger docs
![pic3](https://github.com/divergg/weather_api/blob/master/weather_api/swagger_docs.png)

# Backend integration
Api in integrated with the Yandex weather service. Integration in implemented in the backend/api/services/yandex_integration_service.py

# Text recognition service
In order to avoid negative influence of minimal spelling errors in the names of cities an opened source nlp model is implemented. However, further testing is required.
Regular expressions are used for the most common mistakes.
Service is presented in backend/api/services/spelling_check_service.py
Example of request with error
![pic4](https://github.com/divergg/weather_api/blob/master/weather_api/spelling_error.png)


# Database

Database consists of a single model City with fields name, latitude, longitude, last_requested_at, last_temperature, last_wind and last_pressure.

When the new requests to the same city is handled a check of last_requested_at field is implemented. If the last request was handlend less than 30 mins ago, the saved data is returned. Otherwise the request to yandex API is implemented and the new data will be stored. 

Initial population of database with data is handlend by management command python manage.py add_cities
New cities with coordinates should be added to the backend/api/data/cities.txt

# Deployment

1) git clone

2) Create file .env, and set up the following variables:
   TELEGRAM_TOKEN - BOT father token
   YANDEX_API_KEY - personal key for yandex weather api
   API_HOST - host where backend is running (default should be "backend")

4) Launch docker (docker compose up)
5) Tests can be launched separately using python manage.py test
   
