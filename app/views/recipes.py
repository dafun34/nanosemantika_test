from typing import List

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status
from starlette.responses import JSONResponse

from app.repositories.ingredients import get_ingredients_list
from app.repositories.recipes import (
    create_recipe,
    get_recipe,
    get_recipes_list,
)
from app.schemas.recipes import RecipeCreateSchema, RecipeSchema
from app.views.base import BaseView

router = InferringRouter()


@cbv(router)
class Recipes(BaseView):
    @router.get("/recipes/", response_model=List[RecipeSchema])
    async def get_recipes_list(self) -> List[RecipeSchema]:
        """Получить список рецептов."""
        return await get_recipes_list()

    @router.get(f"/recipes/{{recipe_id}}", response_model=RecipeSchema)
    async def get_recipe(self, recipe_id: int):
        """Получить рецепт по id."""
        return await get_recipe(recipe_id)

    @router.post(
        "/recipes/",
        response_model=RecipeSchema,
        responses={201: {"model": RecipeSchema}},
    )
    async def create_recipe(self, recipe_data: RecipeCreateSchema):
        recipe_id = await create_recipe(recipe_data)
        recipe = await get_recipe(recipe_id)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "recipe created",
                "post": jsonable_encoder(recipe),
            },
        )
