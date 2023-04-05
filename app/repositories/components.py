from sqlalchemy import delete, insert, select

from app.db import async_session
from app.repositories.base import Repository
from app.tables.recipes import Component, recipe_component


async def insert_component(ingredient_id, amount, recipe_id):
    component_create_query = (
        insert(Component)
        .values(
            ingredient_id=ingredient_id, amount=amount, recipe_id=recipe_id
        )
        .returning(Component.id)
    )
    component_id = (await Repository.insert(component_create_query)).scalar()
    recipe_component_query = insert(recipe_component).values(
        recipe_id=recipe_id, component_id=component_id
    )
    await Repository.insert(recipe_component_query)


async def delete_components_by_recipe(recipe_id):
    query = delete(Component).where(
        Component.recipe_id == recipe_id
    )
    await Repository.delete(query)
