from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.core.container import Container
from app.brain_agriculture.api.v1.routes import brain_agriculture_router


def create_app():
    app = FastAPI(
        title="Userv API",
        docs_url="/api/docs/swagger",
        redoc_url="/api/docs/redoc",
        openapi_url="/api/docs",
        version="1.0.0",
    )

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        response = await call_next(request)
        return response

    @app.on_event("startup")
    async def startup():
        container = Container()
        app.container = container
        await container.init_resources()

    @app.on_event("shutdown")
    async def shutdown():
        await app.container.shutdown_resources()

    app.include_router(brain_agriculture_router, prefix="/api/v1", tags=["Brain_Agriculture"])

    origins = [
        "*"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health-check/", status_code=200, include_in_schema=False)
    async def health_check():
        return

    return app


app = create_app()
