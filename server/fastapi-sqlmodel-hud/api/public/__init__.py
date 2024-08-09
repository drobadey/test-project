from fastapi import APIRouter, Depends

from api.public.health import views as health
from api.public.hmis import views as hmis

api = APIRouter()


api.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)

api.include_router(
    hmis.router,
    prefix="/hmis",
    tags=["HMIS"],
    # todo: oauth would be imported this way
    # dependencies=[Depends(authent)],
)
