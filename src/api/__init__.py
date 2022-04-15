import sqlalchemy as sa
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import src.api.protocols
from src.api import users, protocols
from src.database import DatabaseSettings, create_database_url
from src.user.service import UserService
from src.core.errors import (
    NotFoundError,
    DatabaseError,
)


def get_application() -> FastAPI:
    application = FastAPI(
        title='GitHub Repo Stats',
        description='Сервис сбора статистических данных о популярности репозиториев на GitHub.',
        version='1.0.0'
    )

    application.include_router(users.router)

    engine = sa.create_engine(
        create_database_url(),
        future=True
    )

    user_service = UserService(engine)
    application.dependency_overrides[protocols.UserServiceProtocol] = lambda: user_service
    return application


app = get_application()


@app.exception_handler(NotFoundError)
def not_found(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"message": "Not Found"})

@app.exception_handler(DatabaseError)
def database(request: Request, exc: DatabaseError):
    return JSONResponse(status_code=400, content={"message": "Error database"})
