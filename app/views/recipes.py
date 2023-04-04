from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.views.base import BaseView

router = InferringRouter()


@cbv(router)
class Recipes(BaseView):
    @router.get("/recipes/")
    async def get_test(self):
        return "recipes"
