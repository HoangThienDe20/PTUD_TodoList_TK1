from fastapi import FastAPI

from app.core.config import settings
from app.routers import auth_router, todos_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/")
    async def root() -> dict[str, str]:
        return {"message": "Xin chao tu FastAPI Hello To-Do"}

    app.include_router(auth_router, prefix=settings.API_V1_STR)
    app.include_router(todos_router, prefix=settings.API_V1_STR)
    return app


app = create_app()
