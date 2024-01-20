import re
from ..models import City


def city_parser(file):
    """Parser of city parameters and saving into the model"""
    pattern = r'(\w+)\s-\s(\d+\.\d+),\s(\d+\.\d+)'
    with open(file) as f:
        data = f.read()
        matches = re.findall(pattern, data)

        for match in matches:
            print("City:", match[0], "Latitude:", match[1], "Longitude:", match[2])
            if not City.objects.filter(name=match[0]):
                City.objects.create(
                    name=match[0],
                    latitude=match[1],
                    longitude=match[2]
                )
