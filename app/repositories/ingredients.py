from sqlalchemy import select

from app.repositories.base import Repository
from app.tables.recipes import Ingredient


async def get_ingredients_list():
    query = select(Ingredient)
    return await Repository.all(query)

