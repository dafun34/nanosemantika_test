from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status
from starlette.responses import JSONResponse, Response

from app.repositories.components import (
    delete_components_by_recipe,
    insert_component,
)
from app.repositories.recipes import (
    create_recipe,
    delete_recipe,
    get_recipe,
    get_recipes_list,
    update_recipe,
)
from app.schemas.recipes import (
    RecipeCreateSchema,
    RecipeSchema,
    RecipeUpdateSchema,
)
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

    @router.put(f"/recipes/{{recipe_id}}", response_model=RecipeSchema)
    async def update_recipe(
        self, recipe_id: int, update_data: RecipeUpdateSchema
    ):
        if update_data.ingredients:
            await delete_components_by_recipe(recipe_id)
            for ingredient in update_data.ingredients:
                await insert_component(
                    ingredient.ingredient_id, ingredient.amount, recipe_id
                )
        await update_recipe(recipe_id, update_data)
        recipe = await get_recipe(recipe_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "recipe updated",
                "post": jsonable_encoder(recipe),
            },
        )

    @router.post(
        "/recipes/",
        response_model=RecipeSchema,
        responses={201: {"model": RecipeSchema}},
    )
    async def create_recipe(self, recipe_data: RecipeCreateSchema):
        """Создать рецепт."""
        recipe_id = await create_recipe(recipe_data)
        recipe = await get_recipe(recipe_id)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "recipe created",
                "post": jsonable_encoder(recipe),
            },
        )

    @router.delete(f"/recipes/{{recipe_id}}",
                   responses={204: {"description": "Рецепт удален"}})
    async def delete_recipe(self, recipe_id: int):
        """Удалить рецепт."""
        await delete_recipe(recipe_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
