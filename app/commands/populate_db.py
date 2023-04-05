import asyncio

from app.repositories.base import Repository
from app.tables.recipes import Ingredient

ingredients_lst = [
    Ingredient(name='Помидор', measurement_unit='шт'),
    Ingredient(name='Огурец', measurement_unit='шт'),
    Ingredient(name='Майонез', measurement_unit='столовая ложка'),
    Ingredient(name='Болгарский перец', measurement_unit='шт'),
    Ingredient(name='Картофель', measurement_unit='шт'),
    Ingredient(name='Лук', measurement_unit='шт'),
    Ingredient(name='Зеленый лук', measurement_unit='перо'),
    Ingredient(name='Свекла', measurement_unit='шт')
]


async def insert_ingredients(ingredients):
    await Repository.bulk_insert(ingredients)


async def main() -> None:
    """Выполнить команду."""
    await insert_ingredients(ingredients_lst)


if __name__ == "__main__":
    asyncio.run(main())
