# these are database specific models. DIFFERENT from regular pythong models used to
# exchange data over the API.
from datetime import datetime, date

from sqlmodel import Field, SQLModel


class ClientSummaryDBRowReadOnly(SQLModel, table=True):
    __tablename__ = "Client"
    PersonalID: str | None = Field(default=None, primary_key=True)
    FirstName: str | None = None
    MiddleName: str | None = None
    LastName: str | None = None
    NameSuffix: str | None = None
    SocialSecurityNumber: str | None = None
    DateOfBirth: date | None = None
    DateCreated: datetime | None = None
    DateUpdated: datetime | None = None
    DateDeleted: datetime | None = None


class ClientDBRowBase(SQLModel):
    FirstName: str | None = None
    MiddleName: str | None = None
    LastName: str | None = None
    NameSuffix: str | None = None
    NameDataQuality: int | None = None
    SocialSecurityNumber: str | None = None
    SocialSecurityNumberDataQuality: int | None = None
    DateOfBirth: date | None = None
    DateOfBirthDataQuality: int | None = None
    AmIndAKNative: int | None = None
    Asian: int | None = None
    BlackAfAmerican: int | None = None
    HispanicLatinaeo: int | None = None
    MidEastNAfrican: int | None = None
    NativeHIPacific: int | None = None
    White: int | None = None
    RaceNone: int | None = None
    AdditionalRaceEthnicity: str | None = None
    Woman: int | None = None
    Man: int | None = None
    NonBinary: int | None = None
    CulturallySpecific: int | None = None
    Transgender: int | None = None
    Questioning: int | None = None
    DifferentIdentity: int | None = None
    GenderNone: int | None = None
    DifferentIdentityText: str | None = None
    VeteranStatus: int | None = 99
    YearEnteredService: int | None = None
    YearSeparated: int | None = None
    WorldWarII: int | None = None
    KoreanWar: int | None = None
    VietnamWar: int | None = None
    DesertStorm: int | None = None
    AfghanistanOEF: int | None = None
    IraqOIF: int | None = None
    IraqOND: int | None = None
    OtherTheater: int | None = None
    MilitaryBranch: int | None = None
    DischargeStatus: int | None = None

class ClientDBRow(ClientDBRowBase, table=True):
    __tablename__ = "Client"
    # extend_existing required because we're changing our view of the table
    __table_args__ = {'extend_existing': True}
    PersonalID: str | None = Field(default=None, primary_key=True)
    # these are specific to postgresql
    DateCreated: datetime | None = None
    # = Field(sa_column=Column(
    #     TIMESTAMP(timezone=True),
    #     nullable=False,
    #     server_default=text("CURRENT_TIMESTAMP"),
    #     default=None
    # ))
    DateUpdated: datetime | None = None
    #     = Field(sa_column=Column(
    #     TIMESTAMP(timezone=True),
    #     nullable=False,
    #     server_default=text("CURRENT_TIMESTAMP"),
    #     server_onupdate=text("CURRENT_TIMESTAMP"),
    #     default=None
    # ))
    UserID: str | None = None  # foreign key required
    DateDeleted: datetime | None = None
    # ExportID TODO: set to None for now.
    ExportID: str | None = None




# example of relationships
# class Hero(HeroBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     teams: list[Team] = Relationship(back_populates="heroes", link_model=HeroTeamLink)
