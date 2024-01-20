import os
import requests

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from .views import WeatherDataView
from .models import City
from dotenv import load_dotenv

load_dotenv()

class ApiViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = WeatherDataView.as_view()
        self.lang_code = "ru_RU"
        City.objects.create(name="Ярославль", latitude="57.63", longitude="39.87")


    def send_request_to_yandex(self):
        latitude = "57.63"
        longitude = "39.87"
        url = f'https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&lang={self.lang_code}'
        headers = {"X-Yandex-API-Key": os.getenv("YANDEX_API_KEY")}
        response = requests.get(url=url, headers=headers).json()
        data = {
                "temp": response["fact"]["temp"],
                "pressure": response["fact"]["pressure_mm"],
                "wind": response["fact"]["wind_speed"],
                "city_name": "Ярославль",
            }
        return data


    def test_correct_answer(self):
        city_name = "Ярославль"
        request = self.factory.get('/api', data={"city_name": city_name, "lang_code": self.lang_code})
        response = self.view(request)
        self.assertEqual(response.data, self.send_request_to_yandex())

    def test_spell_check(self):
        city_name = "Ярославл"
        request = self.factory.get('/api', data={"city_name": city_name, "lang_code": self.lang_code})
        response = self.view(request)
        self.assertEqual(response.data, self.send_request_to_yandex())

    def test_unknown_city(self):
        city_name = "бла бла"
        request = self.factory.get('/api', data={"city_name": city_name, "lang_code": self.lang_code})
        response = self.view(request)
        self.assertEqual(response.data, {'error': 'Could not recognize city name'})

    def test_missing_fields(self):
        request = self.factory.get('/api', data={"lang_code": self.lang_code})
        response = self.view(request)
        self.assertEqual(response.data, {'error': f'Missing city_name field'})



