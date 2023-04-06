"""Модуль представлений для работы с рецептами."""
from typing import List, Union

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
from app.schemas.responses import BaseResponseModel
from app.views.base import BaseView

router = InferringRouter()

PREFIX = "recipes"


@cbv(router)
class Recipes(BaseView):
    """Представление для работы с рецептами."""

    @router.get(f"/{PREFIX}/", response_model=List[RecipeSchema])
    async def get_recipes_list(self) -> List[RecipeSchema]:
        """Получить список рецептов."""
        return await get_recipes_list()

    @router.get(
        f"/{PREFIX}/{{recipe_id}}",
        response_model=RecipeSchema,
        responses={
            200: {"model": RecipeSchema},
            404: {"model": BaseResponseModel},
        },
    )
    async def get_recipe(
        self, recipe_id: int
    ) -> Union[RecipeSchema, JSONResponse]:
        """Получить рецепт по id."""
        recipe = await get_recipe(recipe_id)
        if recipe:
            return recipe
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "recipe not found"},
        )

    @router.put(
        f"/{PREFIX}/{{recipe_id}}",
        response_model=RecipeSchema,
        responses={
            200: {"model": RecipeSchema},
            404: {"model": BaseResponseModel},
        },
    )
    async def update_recipe(
        self, recipe_id: int, update_data: RecipeUpdateSchema
    ) -> JSONResponse:
        """Обновить рецепт."""
        recipe = await get_recipe(recipe_id)
        if not recipe:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "recipe not found"},
            )
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
        f"/{PREFIX}/",
        response_model=RecipeSchema,
        responses={201: {"model": RecipeSchema}},
    )
    async def create_recipe(
        self, recipe_data: RecipeCreateSchema
    ) -> JSONResponse:
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

    @router.delete(
        f"/{PREFIX}/{{recipe_id}}", response_model=BaseResponseModel
    )
    async def delete_recipe(self, recipe_id: int) -> Response:
        """Удалить рецепт."""
        await delete_recipe(recipe_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
