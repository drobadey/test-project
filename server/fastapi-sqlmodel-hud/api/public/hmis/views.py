# Views are endpoints
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from starlette import status

from api.database import get_session
from api.public.hmis.crud import create_client_row, read_client_row, update_client_row, read_client_summary_rows, \
    delete_soft_client_row

from api.public.hmis.models import Client, ClientBase, ClientSummary, ClientSummaryQuery
from api.utils.attr_mapper import map_from_api_to_db_client, map_from_db_to_api_client
from api.utils.logger import logger_config
from api.utils.misc import redact_a_ssn

# This might be cool to use.
# https://stackademic.com/blog/fastapi-role-base-access-control-with-jwt-9fa2922a088c
# But if it fails, throw a PermissionError since there's a handler in app.py
# But a decorator for checking permissions would be easier.

router = APIRouter()
logger = logger_config(__name__)

# todo: add security https://fastapi.tiangolo.com/reference/dependencies/#security

TOO_MANY_RESULTS = 2000



# takes a ClientBase and returns a Client
@router.post('/client', response_model=Client, tags=['Client'])
def create_a_client(client: ClientBase, db: Session = Depends(get_session)) -> Client:
    # this is done automatically, but if we needed to do it by hand, this is how
    # client_valid = ClientBase.model_validate(client)

    # now we manually map all the fields. Not great, we could make the db schema more closely match the API schema
    # BUT the nested data in Client would probably mean more tables and joins.
    client_row = map_from_api_to_db_client(client)

    result_row = create_client_row(client_base=client_row, db=db)
    result = map_from_db_to_api_client(result_row)
    return result


@router.get("/clients/{client_id}", response_model=Client, tags=['Client'])
def read_client(client_id: str, db: Session = Depends(get_session)) -> Client:
    client = read_client_row(client_id=client_id, db=db)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client not found with id: {client_id}",
        )
    result = map_from_db_to_api_client(client)
    return result


@router.post("/clientsummary", response_model=list[ClientSummary])
def read_all_clients(
        querydata: ClientSummaryQuery,  # in body as json
        db: Session = Depends(get_session)):
    # the body is json and this is a post because it contains PII

    # todo: if NO query params are passed in then fail.

    # todo: fail if too many rows *could* be returned so someone can't read whole db.
    #  we'll need a specific count(*) query to get this since the query below has a "limit"
    # if len(results) > TOO_MANY_RESULTS:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"Query was too generic and return more than {TOO_MANY_RESULTS}. Narrow your search and try again.",
    #     )

    # todo: ssnum_suffix probably has a specific format as a string in the db, normalize it.
    results = read_client_summary_rows(db=db,
                                       offset=querydata.offset,
                                       limit=querydata.limit,
                                       firstname=querydata.FirstName,
                                       lastname=querydata.LastName,
                                       namesuffix=querydata.NameSuffix,
                                       dob=querydata.DateOfBirth,
                                       ssnum_suffix=querydata.SocialSecurityNumber)

    # todo: redact SSN in all rows (probably based on permissions of user from jwt)
    for row in results:
        row.SocialSecurityNumber = redact_a_ssn(row.SocialSecurityNumber)

    # NOTE: this assumes the database schema results EXACTLY match the expected json response (response_model above)
    # So if the DB has "SSN" and the API has "SocialSecurityNumber" then this will fail unless you remap
    # the fields.
    return results


@router.put("/clients/{client_id}", response_model=Client, tags=['Client'])
def update_client(client_id: str, client: ClientBase, db: Session = Depends(get_session)) -> Client:
    # verify the fields passed in
    client_verified = ClientBase.model_validate(client)

    # merge in fields since only changed data may be passed in.
    # to merge in, we must first fetch the existing data in the table.
    # this is NOT an extra fetch since we need to verify the id exists in the table.
    client_starting = read_client_row(client_id, db)
    if not client_starting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client not found with id: {client_verified.PersonalID}",
        )

    # this takes our verified fields and merges them into the existing row (client_starting)
    client_to_update = map_from_api_to_db_client(client_verified, client_starting)

    # The DateLastModified should be maintained by the database, otherwise do it here.
    # TODO: the UserId should be updated to be this user on modify? This is where an audit table would be handy.
    # client_to_update.UserID = get_user_id_from_oauth()
    update_client_row(client=client_to_update, db=db)

    # now map it BACK to the API
    return map_from_db_to_api_client(client_to_update)


# Notice: there is no response_model since
@router.delete("/clients/{client_id}", tags=['Client'])
def delete_client(client_id: str, db: Session = Depends(get_session)):

    client = delete_soft_client_row(client_id=client_id, db=db)
    if not client:
        # todo: maybe include the UserId of the person doing the action from the jwt
        logger.info("Delete client failed. PersonID not found %s", client_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client not found with id: {client_id}",
        )

    # todo return should be as per API
    return {"ok": True}
