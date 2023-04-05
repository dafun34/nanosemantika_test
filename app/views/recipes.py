from typing import List

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.repositories.ingredients import get_ingredients_list
from app.repositories.recipes import get_recipe, get_recipes_list
from app.schemas.recipes import RecipeSchema
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
