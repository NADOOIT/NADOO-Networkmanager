from pydantic import BaseModel, Field, EmailStr, ValidationError


class UserData(BaseModel):
    vorname: str = Field(..., min_length=1, max_length=50)
    nachname: str = Field(..., min_length=1, max_length=50)
    firmenname: str = Field(None, min_length=1, max_length=100)
    unternehmensbranche: str = Field(None, min_length=1, max_length=100)
    telefonnummer: str = Field(None, min_length=1, max_length=20)
    email: EmailStr = Field(...)
    webseite: str = Field(None, min_length=1, max_length=100)
    chapter: str = Field(None, min_length=1, max_length=100)
    mitgliedsstatus: str = Field(None, min_length=1, max_length=100)


def validate_user_data(data: dict) -> UserData:
    return UserData(**data)
