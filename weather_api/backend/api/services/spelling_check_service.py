import spacy
from typing import Union
from ..models import City


class SpellCheckerService:
    """Service for spelling check of city name"""

    def __init__(self):
        self.nlp = spacy.load("ru_core_news_sm")
        self.data = []

    def set_up_data(self):
        """Setting up data for spelling check for nlp"""
        cities = City.objects.all()
        self.data = [city.name for city in cities]

    def full_equality_check(self, input_word: str, cities: [City]) -> Union[str, None]:
        """Check whether the input is fully equal to any data"""
        city_names = [city.name for city in cities]
        for name in city_names:
            if input_word.lower() == name.lower():
                return name
        return None

    def similarity_check(self, input_word):
        """Looking for the best match for input word"""
        cities = City.objects.all()
        full_equality = self.full_equality_check(input_word, cities)
        if full_equality:
            return full_equality
        doc = self.nlp(input_word)
        closest_name = None
        highest_similarity = 0
        for city in cities:
            name_doc = self.nlp(city.name)
            similarity = doc.similarity(name_doc)
            if similarity > highest_similarity:
                highest_similarity = similarity
                closest_name = city.name
        if highest_similarity > 0.8:
            return closest_name
        return None