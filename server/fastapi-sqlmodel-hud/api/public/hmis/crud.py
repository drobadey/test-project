# CRUD (Create Read Update Delete) database operations.
import uuid

from fastapi import HTTPException
from sqlmodel import Session, select, col, func

from api.public.hmis.dbmodels import ClientDBRow, ClientSummaryDBRowReadOnly, ClientDBRowBase


def create_client_row(client_base: ClientDBRowBase, db: Session) -> ClientDBRow:
    # may be issues using thie approach
    # client.PersonalID = create_hash_id(client.FirstName, client.LastName, client.SocialSecurityNumber, f"{client.DateOfBirth}")
    client = ClientDBRow(ClientDBRowBase=client_base)
    client.PersonalID = uuid.uuid4().hex
    client.DateCreated = func.now()
    client.DateUpdated = func.now()
    client.DateDeleted = None


    # todo: grab the userid from the auth token.
    #  this could be done at higher level code, but it is probably safer to have it here?
    # client_row.UserID = jwt.userid
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


# def read_heroes(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
#     heroes = db.exec(select(Hero).offset(offset).limit(limit)).all()
#     return heroes


# todo: add query paramaters to function
def read_client_summary_rows(
        db: Session, # first because the rest are "default parameters"
        offset: int = 0,
        limit: int = 20,
        firstname: str | None = None,
        lastname: str | None = None,
        namesuffix: str | None = None,
        dob: str | None = None,
        ssnum_suffix: str | None = None,
):
    # See https://sqlmodel.tiangolo.com/tutorial/where/
    statement = (select(ClientSummaryDBRowReadOnly).
                 where(col(ClientSummaryDBRowReadOnly.DateDeleted).is_(None)))

    # this will AND each condition.
    # Note the order_by's also matter the sequence they are added.
    # So, if you want to change the SORT ORDER, you'll need to change the order of the if's below
    if lastname:
        #istartswith is case insensitive matching
        statement = statement.where(col(ClientSummaryDBRowReadOnly.LastName).istartswith(lastname))
        statement = statement.order_by(col(ClientSummaryDBRowReadOnly.LastName))
    if firstname:
        statement = statement.where(col(ClientSummaryDBRowReadOnly.FirstName).istartswith(firstname))
        statement = statement.order_by(col(ClientSummaryDBRowReadOnly.FirstName))
    if namesuffix:
        statement = statement.where(col(ClientSummaryDBRowReadOnly.NameSuffix).istartswith(namesuffix))
        statement = statement.order_by(col(ClientSummaryDBRowReadOnly.NameSuffix))
    ## todo: DateOfBirth is hard. The query is going to need to cast to a string then do istartswith
    ##   or some kind of `date_part('year', mydate) == year`
    # if dob:
    #     statement = statement.where(col(ClientSummaryDBRowReadOnly.DateOfBirth).istartswith(dob))
    #     statement = statement.order_by(col(ClientSummaryDBRowReadOnly.DateOfBirth))
    if ssnum_suffix:
        statement = statement.where(col(ClientSummaryDBRowReadOnly.SocialSecurityNumber).iendswith(ssnum_suffix))
        statement = statement.order_by(col(ClientSummaryDBRowReadOnly.DateOfBirth))

    # finally set the offset and limit
    statement = statement.offset(offset).limit(limit)
    results = db.exec(statement).all()
    return results


def read_client_row(client_id: str, db: Session) -> ClientDBRow:
    statement = select(ClientDBRow).where(col(ClientDBRow.PersonalID) == client_id)
    statement = statement.where(col(ClientSummaryDBRowReadOnly.DateDeleted).is_(None))
    return db.exec(statement).one_or_none()


def update_client_row(client: ClientDBRow, db: Session) -> ClientDBRow:
    # this makes sure the record is not deleted before updating.
    if not read_client_row(client.PersonalID, db):
        # putting http exceptions in the db layer feels yucky, it could throw and the endpoint could catch?
        # todo: move up to crud layer
        raise HTTPException(404, detail=f"Client not found PersonalID={client.PersonalID}")

    # update the last mode
    client.DateLastModified = func.now()
    # todo: grab the userid from the auth token
    # client.UserID = jwt.userid
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def delete_soft_client_row(client_id: str, db: Session):
    # another delete would update the delete timestamp, not ideal
    client = read_client_row(client_id, db)
    if not client:
        # putting http exceptions in the db layer feels yucky, it could throw and the endpoint could catch?
        return None

    # flag deleted
    client.DateDeleted = func.now()
    # technically it was modified, but there's not much point in setting both to the same value?
    # client.DateLastModified = func.now()

    # todo: grab the userid from the JWT auth token
    # client.UserID = jwt.userid
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

