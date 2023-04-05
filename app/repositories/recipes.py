from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.repositories.base import Repository
from app.tables.recipes import Recipes


async def get_recipes_list():
    query = select(Recipes).options(selectinload(Recipes.ingredients))
    return await Repository.all(query)


async def get_recipe(recipe_id: int):
    query = (
        select(Recipes)
        .where(Recipes.id == recipe_id)
        .options(selectinload(Recipes.ingredients))
    )
    return await Repository.scalar(query)
