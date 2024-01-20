from drf_yasg.utils import swagger_auto_schema
from rest_framework import views
from rest_framework.response import Response
from drf_yasg import openapi
from .utils.request_fields_check import handle_errors
from .services.weather_data_service import WeatherDataService
from .logger import logger



class WeatherDataView(views.APIView):
    """Api view for weather data"""

    ALLOWED_FIELDS = [
        "city_name",
        "lang_code"
    ]

    @swagger_auto_schema(
        operation_description="Endpoint for getting weather data",
        manual_parameters=[
            openapi.Parameter(
                'city_name', openapi.IN_QUERY,
                description="Name of the city",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'lang_code', openapi.IN_QUERY,
                description="Language code of the request",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request):

        data = request.query_params

        # Handle possible errors
        errors = handle_errors(data, self.ALLOWED_FIELDS)
        if errors:
            logger.error(errors.data["error"])
            return errors

        city_name = data["city_name"]
        lang_code = data["lang_code"]

        try:
            city = WeatherDataService().get_city(city_name=city_name)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response({"error": "Could not recognize city name"})

        data = WeatherDataService().get_city_weather_data(city=city, lang_code=lang_code)
        return Response(data)
