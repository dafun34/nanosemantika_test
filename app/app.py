import uvicorn
from fastapi import FastAPI, APIRouter
from app.config import settings
from app.views import recipes


def init_app() -> FastAPI:
    """Инициализация приложения."""
    app = FastAPI()
    main_router = APIRouter()
    main_router.include_router(recipes.router)
    app.include_router(main_router)
    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run(
        app, host=settings.APP_HOST, port=settings.APP_PORT, reload=True
    )
