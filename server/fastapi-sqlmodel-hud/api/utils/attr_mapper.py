# It's very verbose to assign data back and forth. attempt to make data driven.
# Most libraries assume the database schema matches the api schema.
# Grouping the data using "name", "ssn", "vitalStatistics" ends up being
# pretty painful in python specifically because of the nesting.
# It means the mapping fields have to be kept in-sync with the both
# the API schema and the db schema.... including NOT MISSING a field.
import logging

# might be able to use https://docs.sqlalchemy.org/en/20/orm/declarative_config.html ?

from api.public.hmis.dbmodels import ClientDBRow
from api.public.hmis.models import ClientBase, Client
from api.utils.misc import redact_a_ssn

CLIENT_FIELD_MAP = {
    # "PersonalID": "PersonalID",  # should not be included when going from api->db
    "FirstName": "name.FirstName",
    "MiddleName": "name.MiddleName",
    "LastName": "name.LastName",
    "NameSuffix": "name.NameSuffix",
    "NameDataQuality": "name.NameDataQuality",
    "SocialSecurityNumber": "ssn.SocialSecurityNumber", # redacted on read
    "SocialSecurityNumberDataQuality": "ssn.SocialSecurityNumberDataQuality",
    "DateOfBirth": "vitalStatistics.DateOfBirth",
    "DateOfBirthDataQuality": "vitalStatistics.DateOfBirthDataQuality",
    "AmIndAKNative": "RaceAndEthnicity.AmIndAKNative",
    "Asian": "RaceAndEthnicity.Asian",
    "BlackAfAmerican": "RaceAndEthnicity.BlackAfAmerican",
    "HispanicLatinaeo": "RaceAndEthnicity.HispanicLatinaeo",
    "MidEastNAfrican": "RaceAndEthnicity.MidEastNAfrican",
    "NativeHIPacific": "RaceAndEthnicity.NativeHIPacific",
    "White": "RaceAndEthnicity.White",
    "RaceNone": "RaceAndEthnicity.RaceNone",
    "AdditionalRaceEthnicity": "RaceAndEthnicity.AdditionalRaceEthnicity",
    "Woman": "Gender.Woman",
    "Man": "Gender.Man",
    "NonBinary": "Gender.NonBinary",
    "CulturallySpecific": "Gender.CulturallySpecific",
    "Transgender": "Gender.Transgender",
    "Questioning": "Gender.Questioning",
    "DifferentIdentity": "Gender.DifferentIdentity",
    "GenderNone": "Gender.GenderNone",
    "DifferentIdentityText": "Gender.DifferentIdentityText",
    "VeteranStatus": "Veteran.VeteranStatus",
    "YearEnteredService": "Veteran.YearEnteredService",
    "YearSeparated": "Veteran.YearSeparated",
    "WorldWarII": "Veteran.WorldWarII",
    "KoreanWar": "Veteran.KoreanWar",
    "VietnamWar": "Veteran.VietnamWar",
    "DesertStorm": "Veteran.DesertStorm",
    "AfghanistanOEF": "Veteran.AfghanistanOEF",
    "IraqOIF": "Veteran.IraqOIF",
    "IraqOND": "Veteran.IraqOND",
    "OtherTheater": "Veteran.OtherTheater",
    "MilitaryBranch": "Veteran.MilitaryBranch",
    "DischargeStatus": "Veteran.DischargeStatus",
    # fields maintained by the database not used for api -> db
    # "DateCreated": "DateCreated",
    # "DateUpdated": "DateUpdated",
    # "UserID": "UserID",
    # "DateDeleted": "DateDeleted",
    # "ExportID": "ExportID"
}

CLIENT_FIELD_INVERT_MAP = dict((v,k) for k,v in CLIENT_FIELD_MAP.items())

# todo: write unit tests. for these functions
def map_from_api_to_db_client(client_in: ClientBase,
                              opt_client_to_merge_into: ClientDBRow = ClientDBRow()) -> ClientDBRow:
    # Mapping uses ClientTable field name as key and Client model field as value.
    out = opt_client_to_merge_into  # readability

    # we only map over nested
    for k, v in client_in.__dict__.items():
        if hasattr(v, "__dict__"):
            for k2, v2 in v.__dict__.items():
                if hasattr(out, k2):
                    setattr(out, k2, v2)
                else:
                    logging.log(f"missing key {k2} in ClientDBRow")

    return out


def map_from_db_to_api_client(clienttable_in: ClientDBRow, opt_client_to_merge_into: Client = Client()) -> Client:
    # Mapping uses ClientTable field name as key and Client model field as value.
    out = opt_client_to_merge_into  # readability
    for key in CLIENT_FIELD_MAP.keys():
        try:
            parts = CLIENT_FIELD_MAP[key].split('.')
            grouping = parts[0]
            field = parts[1]
            out[grouping][field] = clienttable_in[key]
        except KeyError:
            print(f"mistake with key='{key}' or value for that key")
    # when going from the db back to the api, we include fields that were intentionally omitted like timestamps
    # but fun fact, these should already include in the opt_client_to_merge_into!

    # SSN is not mapped by default, so we can redact on read if needed.
    # since we're writing to the db, no redaction... but validation should have made sure it's complete
    # There might be a future case where it's NOT redacted if the user is an admin
    if opt_client_to_merge_into.ssn.SocialSecurityNumber:
        out.SSN = redact_a_ssn(opt_client_to_merge_into.SSN.SocialSecurityNumber)
    return out
