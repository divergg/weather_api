import datetime
from .yandex_integration_service import YandexIntegrationService
from .spelling_check_service import SpellCheckerService
from ..logger import logger
from ..models import City


class WeatherDataService:

    def get_city(self, city_name: str):
        """Recognition of city name"""
        logger.debug(f'Requested city is {city_name}')
        city_name = SpellCheckerService().similarity_check(input_word=city_name)
        logger.debug(f'Recognized city is {city_name}')
        if city_name is None:
            raise Exception(f'City {city_name} not found in database')
        city = City.objects.filter(name=city_name).first()
        return city

    def get_city_weather_data(self, city: City, lang_code: str = None) -> dict:
        """Receiving city weather data"""
        params = {
            "latitude": city.latitude,
            "longitude": city.longitude,
            "lang_code": lang_code
        }
        update_time = city.last_requested_at
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        delta = 30
        if update_time:
            if (now - update_time).total_seconds() < delta * 60:
                data = {
                    "temp": city.last_temperature,
                    "pressure": city.last_pressure,
                    "wind": city.last_wind,
                }
            else:
                data = YandexIntegrationService().get_data_from_yandex_api(request_params=params)
        else:
            data = YandexIntegrationService().get_data_from_yandex_api(request_params=params)
            error = data.get("error", None)
            if not error:
                city.last_temperature = data["temp"]
                city.last_wind = data["wind"]
                city.last_pressure = data["pressure"]
                city.last_requested_at = datetime.datetime.now(tz=datetime.timezone.utc)
                city.save()
        data.update({"city_name": city.name})
        return data


