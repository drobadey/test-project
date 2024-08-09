from sqlmodel import Session

from api.database import engine
from api.public.hmis.dbmodels import ClientDBRow
from api.utils.logger import logger_config

logger = logger_config(__name__)

def create_mock_client():
    with Session(engine) as session:
        client1 = ClientDBRow(firstName="John", lastName="Doe", email="test@example.com")

        session.add(client1)
        # session.add(client2)
        session.commit()

        session.refresh(client1)
        # session.refresh(client2)

        logger.info("=========== MOCK DATA CREATED ===========")
        logger.info("client1 %s", client1)
        logger.info("===========================================")
