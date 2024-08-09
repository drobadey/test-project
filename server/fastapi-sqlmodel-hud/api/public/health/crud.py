# health is a health-check endpoint it needs to be fast and just verify that the server is
#   basically up and working (including a db connection)
from fastapi import Depends
from sqlmodel import Session, text

from api.config import settings
from api.database import get_session
from api.public.health.models import Health, Status
from api.utils.logger import logger_config

logger = logger_config(__name__)

# health endpoints that hit the database need to be protected from abuse (DDoS)
# either use firewall rules or set up caching result.
def health_db(db: Session = Depends(get_session)) -> Status:
    try:
        db.exec(text(f"SELECT COUNT(id) FROM client;")).one_or_none()
        return Status.OK
    except Exception as e:
        logger.exception(e)

    return Status.KO

def get_health(db: Session) -> Health:
    db_status = health_db(db=db)
    logger.info("%s.get_health.db_status: %s", __name__, db_status)
    return Health(app_status=Status.OK, db_status=db_status, environment=settings.ENV)

