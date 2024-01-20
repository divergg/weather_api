import re
from django.core.management.base import BaseCommand
from ...models import City


class Command(BaseCommand):
    help = 'Add cities to database'

    def handle(self, *args, **options):
        self.run()


    def run(self):
        """Parser of city parameters and saving into the model"""
        pattern = r'([^\s—]+(?:\s[^\s—]+)*)\s—\s(\d+\.\d+),\s(\d+\.\d+)'
        file = "./api/data/cities.txt"
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

