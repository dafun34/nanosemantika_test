"""Репозиторий для работы с рецептами."""
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import selectinload

from app.repositories.base import Repository
from app.repositories.components import insert_component
from app.schemas.recipes import RecipeCreateSchema, RecipeUpdateSchema
from app.tables.recipes import Recipes


async def get_recipes_list() -> list:
    """Получить список рецептов."""
    query = select(Recipes).options(selectinload(Recipes.ingredients))
    return await Repository.all(query)


async def get_recipe(recipe_id: int) -> tuple:
    """Получить рецепт по id."""
    query = (
        select(Recipes)
        .where(Recipes.id == recipe_id)
        .options(selectinload(Recipes.ingredients))
    )
    return await Repository.scalar(query)


async def create_recipe(recipe_data: RecipeCreateSchema) -> int:
    """Создать рецепт и вернуть его id."""
    recipe_create_query = (
        insert(Recipes)
        .values(
            name=recipe_data.name,
            description=recipe_data.description,
            cooking_time=recipe_data.cooking_time,
        )
        .returning(Recipes.id)
    )
    recipe_id = (await Repository.insert(recipe_create_query)).scalar()
    for ingredient in recipe_data.ingredients:
        await insert_component(
            ingredient.ingredient_id, ingredient.amount, recipe_id
        )
    return recipe_id


async def update_recipe(
    recipe_id: int, update_data: RecipeUpdateSchema
) -> None:
    """Обновить рецепт."""
    if not update_data.dict(exclude_unset=True, exclude={"ingredients"}):
        return
    update_query = (
        update(Recipes)
        .where(Recipes.id == recipe_id)
        .values(
            **update_data.dict(exclude_unset=True, exclude={"ingredients"})
        )
    )
    await Repository.update(update_query)


async def delete_recipe(recipe_id: int) -> None:
    """Удалить рецепт."""
    query = delete(Recipes).where(Recipes.id == recipe_id)
    await Repository.delete(query)
