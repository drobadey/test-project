
## FastAPI + SQLModel Boilerplate App
A RestAPI real world app based on SQLModel [documentation example](https://sqlmodel.tiangolo.com/tutorial/), using [FastAPI](https://fastapi.tiangolo.com/) and [SQLModel](https://sqlmodel.tiangolo.com/)

Libraries:
- FastAPI: API endpoints server
  - Build on top of uvicorn server
- SqlModel: database modeling
  - build on top of SQLAlchemy and Pydantic
- Pydantic: data validation
  - email-validator: optional include for Pydantic
- psycopg2: postgresql server driver for python
- unidecode: normalizes letters like `José` to `Jose`
- travern: test api endpoints without needing client
  - uses pytest 

Resource:
 - https://fastapi.tiangolo.com/external-links/

### Quickstart
1. Install dependencies via `pipenv install --dev`
2. Set up database
3. <b>Start the App</b>:
  - Using Python:
    `pipenv run python asgi.py`

  - Using Docker:
    `docker build -t sqlmodel-api:latest . && docker run -p 8080:8080 sqlmodel-api:latest`

4. <b>Use Openapi at</b>: `http://localhost:8080/api/`

5Make api calls to `http://localhost:8080/

### Running Tests:
While your app is running, open another terminal:

Unit tests - no server needed
`pipenv run pytest -v tests/`

API tests - needs server running during tests `pipenv run python asgi.py`
`pipenv run pytest -v tavern_tests/`

> ⚠️ WARNING: API tests are not fully working but provided as a demo

### Set up test database
- Assumes postgres sql.
- Table and field names must be "quoted" so they are
created with the correct case.
- Keys are strings(32) but should be created internally by database.
- Future interation should create `Client` (aka `PersonID`) keys based on [this concept](https://github.com/HUD-Data-Lab/Data.Exchange.and.Interoperability/issues/26) 
- Timestamps should be managed by database (not code)

> ⚠️ TODO: add sql table as a file to this readme

> ⚠️ The field names in the database should match the fieldnames used by the API
>   Otherwise, things get much harder when mapping back and forth.

```sql
CREATE TABLE "Client" (
      "PersonalID" VARCHAR(32) PRIMARY KEY NOT NULL,
      "FirstName" VARCHAR(50),
      "MiddleName" VARCHAR(50),
      "LastName" VARCHAR(50),
      "NameSuffix" VARCHAR(50),
      "NameDataQuality" INT,
      "SocialSecurityNumber" VARCHAR(9),
      "SocialSecurityNumberDataQuality" INT,
      "DateOfBirth" DATE,
      "DateOfBirthDataQuality" INT,
      "AmIndAKNative" INT,
      "Asian" INT,
      "BlackAfAmerican" INT,
      "HispanicLatinaeo" INT,
      "MidEastNAfrican" INT,
      "NativeHIPacific" INT,
      "White" INT,
      "RaceNone" INT,
      "AdditionalRaceEthnicity" VARCHAR(100),
      "Woman" INT,
      "Man" INT,
      "NonBinary" INT,
      "CulturallySpecific" INT,
      "Transgender" INT,
      "Questioning" INT,
      "DifferentIdentity" INT,
      "GenderNone" INT,
      "DifferentIdentityText" VARCHAR(100),
      "VeteranStatus" INT,
      "YearEnteredService" INT,
      "YearSeparated" INT,
      "WorldWarII" INT,
      "KoreanWar" INT,
      "VietnamWar" INT,
      "DesertStorm" INT,
      "AfghanistanOEF" INT,
      "IraqOIF" INT,
      "IraqOND" INT,
      "OtherTheater" INT,
      "MilitaryBranch" INT,
      "DischargeStatus" INT,
      "DateCreated" timestamp,
      "DateUpdated" timestamp,
      "UserID" VARCHAR(32),
      "DateDeleted" timestamp,
      "ExportID" VARCHAR(32)
);


INSERT INTO "Client" ("PersonalID", "FirstName", "MiddleName", "LastName", "NameSuffix", "NameDataQuality", "SocialSecurityNumber", "SocialSecurityNumberDataQuality", "DateOfBirth", "DateOfBirthDataQuality", "AmIndAKNative", "Asian", "BlackAfAmerican", "HispanicLatinaeo", "MidEastNAfrican", "NativeHIPacific", "White", "RaceNone", "AdditionalRaceEthnicity", "Woman", "Man", "NonBinary", "CulturallySpecific", "Transgender", "Questioning", "DifferentIdentity", "GenderNone", "DifferentIdentityText", "VeteranStatus", "YearEnteredService", "YearSeparated", "WorldWarII", "KoreanWar", "VietnamWar", "DesertStorm", "AfghanistanOEF", "IraqOIF", "IraqOND", "OtherTheater", "MilitaryBranch", "DischargeStatus", "DateCreated", "DateUpdated", "UserID", "DateDeleted", "ExportID")
VALUES
    ('1000', 'Client One', NULL, 'TestABC', NULL, '1', '123456789', '1', '1984-01-01', '1', '0', '0', '0', '0', '0', '0', '1', NULL, NULL, '1', '0', '0', '0', '0', '0', '0', NULL, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2001-07-07 21:35:00', '2017-04-10 10:07:10', '49', NULL, '1036'),
    ('1001', 'Client Two', NULL, 'TestAB', NULL, '1', '333333333', '1', '1981-01-01', '1', '0', '0', '0', '1', '0', '0', '1', NULL, NULL, '0', '1', '0', '0', '0', '0', '0', NULL, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2001-04-26 15:10:00', '2020-01-06 14:05:17', '25', NULL, '1036'),
    ('1002', 'Client Three', NULL, 'TestA', NULL, '1', '999999999', '1', '1950-01-01', '1', '0', '0', '0', '0', '0', '0', '1', NULL, NULL, '0', '1', '0', '0', '0', '0', '0', NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '1999-04-01 15:11:00', '2016-08-15 11:20:02', '59', NULL, '1036'),
    ('1003', 'Client Four', NULL, 'TestBCD', NULL, '1', '567890123', '1', '1953-01-01', '1', '0', '0', '0', '0', '0', '0', '1', NULL, NULL, '0', '1', '0', '0', '0', '0', '0', NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2001-03-26 14:12:00', '2016-08-15 11:28:14', '59', NULL, '1036'),
    ('1004', 'Client Five', NULL, 'TestB', NULL, '1', '111111111', '1', '2007-01-01', '1', '0', '0', '1', '0', '0', '0', '0', NULL, NULL, '0', '1', '0', '0', '0', '0', '0', NULL, NULL, '99', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2013-11-11 18:11:52', '2017-04-04 15:21:34', '26', NULL, '1036'),
    ('1005', 'Client Six Deleted', NULL, 'Test Deleted', NULL, '1', '111111111', '1', '2007-01-01', '1', '0', '0', '1', '0', '0', '0', '0', NULL, NULL, '0', '1', '0', '0', '0', '0', '0', NULL, NULL, '99', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2013-11-11 18:11:52', '2017-04-04 15:21:34', '26', '2007-02-02', '1036')
;

```

### Misc Dev Information

This is the commandline used to generate the python models code.
It needs to be installed via a python pip-like tool.

You'll need to customize the `--input` to be a full path to your local copy of the api file.

It will generate a directory from `--output` with two files:  `main.py` and `models.py`

```commandline
fastapi-codegen \
--python-version 3.12 \
--output-model-type pydantic_v2.BaseModel \
--enum-field-as-literal one \
--input hmis-spec-v1.0.yml \
--output latestapi
```

`main` has the endpoints in a very basic format

`models` has the python model

Example of generate model class:

```python
class ClientSummaryResponse(BaseModel):
    query: Optional[Dict[str, Any]] = None
    result: Optional[List[ClientSummary]] = None
    total: Optional[int] = None

```

