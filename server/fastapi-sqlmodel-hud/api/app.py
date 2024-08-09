from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from api.config import Settings
from api.database import create_db_and_tables
from api.public import api as public_api
from api.utils.logger import logger_config
from api.utils.mock_data_generator import create_mock_client

logger = logger_config(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # using sqlmodel (sqlalchemy) to create tables is tricky because API fields to sql field mapping
    # create_db_and_tables()
    # create_mock_client()

    logger.info("startup: triggered")

    yield

    logger.info("shutdown: triggered")


def create_app(settings: Settings):
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/api",
        description=settings.DESCRIPTION,
        lifespan=lifespan,  # initial setup databases.
        servers=[{'url': 'https://example.com/hmis'}],
    )

    app.include_router(public_api)

    # this will automatically map data validation errors to responses
    # it looks like:
    '''
    {
        "detail": [
            {
                "type": "date_from_datetime_inexact",
                "loc": [
                    "body",
                    "DateOfBirth"
                ],
                "msg": "Datetimes provided to dates should have zero time - e.g. be exact dates",
                "input": "1981"
            }
        ],
        "body": {
            "DateOfBirth": "1981",
            "offset": 0,
            "limit": 10
        }
    }
    '''

    # todo: make the output match what the API expects by customizing the json inside of jsonable_encoder()
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )

    @app.exception_handler(PermissionError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # this error is a bit generic INTENTIONALLY. Giving details about why access was forbidden can be exploited
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder({"detail": "402 Unauthorized",
                                      "body": "Forbidden - Request is successfully understood but the user is not authorized to use or access this resource"}),
        )

    return app
