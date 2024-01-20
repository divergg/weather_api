import os
import requests
import logging
from typing import Union
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger()
STREAM_HANDLER = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s]\t%(levelname)2s:\t%(message)s")
STREAM_HANDLER.setFormatter(
    formatter
)
FILE_HANDLER = logging.FileHandler('./api/logs/yandex_api.log')
FILE_HANDLER.setFormatter(formatter)
logger.addHandler(STREAM_HANDLER)
logger.addHandler(FILE_HANDLER)
logger.setLevel("DEBUG")


class YandexIntegrationService:

    """Service for Yandex weather API"""

    def send_data_from_yandex_weather(self,
                                      latitude: str,
                                      longitude: str,
                                      lang_code: str = None) -> Union[dict, None]:
        """Sending data from yandex weather API, raises Exception if connection is failed"""
        if not lang_code:
            lang_code = "en_US"
        url = f'https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&lang={lang_code}'
        headers = {"X-Yandex-API-Key": os.getenv("YANDEX_API_KEY")}
        try:
            response = requests.get(url=url, headers=headers)
            if response.status_code < 400:
                logger.debug(f'Got response from API - {response.json()}')
                return response.json()
            raise requests.exceptions.ConnectionError
        except Exception as e:
            logger.error(e, exc_info=True)


    def get_data_from_yandex_api(self,
                                 request_params: dict) -> dict:
        """Receiving data from yandex API"""
        latitude = request_params.get("latitude")
        longitude = request_params.get("longitude")
        lang_code = request_params.get("lang_code", None)
        try:
            if not longitude or not latitude:
                raise Exception("Location coordinates are not provided")
            response = self.send_data_from_yandex_weather(latitude, longitude, lang_code)
            data = {
                "temp": response["fact"]["temp"],
                "pressure": response["fact"]["pressure_mm"],
                "wind": response["fact"]["wind_speed"]
            }
            return data
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"error": "Exception in yandex API. Check API logs"}

