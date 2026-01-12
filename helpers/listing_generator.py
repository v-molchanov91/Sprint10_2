import random
from helpers.string_generator import StringGenerator


class ListingGenerator:

    _CATEGORIES = ["Авто", "Книги", "Садоводство", "Хобби", "Технологии"]

    _CITIES = [
        "Москва",
        "Санкт-Петербург",
        "Казань",
        "Нижний Новгород",
        "Екатеринбург",
        "Новосибирск",
    ]

    @staticmethod
    def generate_listing_data(
        name=None,
        category=None,
        condition=None,
        city=None,
        description=None,
        price=None,
    ):
        return {
            "name": name or StringGenerator.alphanumeric(10),
            "category": category or random.choice(ListingGenerator._CATEGORIES),
            "condition": condition or random.choice(["Новый", "Б/У"]),
            "city": city or random.choice(ListingGenerator._CITIES),
            "description": description or StringGenerator.alphanumeric(50),
            "price": price or str(random.randint(100, 100_000)),
        }
