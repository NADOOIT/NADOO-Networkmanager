from pydantic import BaseModel, Field, EmailStr, ValidationError


class PresentationSlideData(BaseModel):
    Folientitel: str = Field(..., min_length=1, max_length=100)
    Firmenname: str = Field(..., min_length=1, max_length=100)
    Unternehmensbranche: str = Field(..., min_length=1, max_length=100)
    Vorname: str = Field(..., min_length=1, max_length=50)
    Nachname: str = Field(..., min_length=1, max_length=50)
    Kontaktdaten: str = Field(..., min_length=1, max_length=100)  # Assuming this can be any string; adjust if needed
    Naechster_vortrag: str = Field(..., min_length=1, max_length=50)  # Assuming this is a string; adjust if needed


def validate_presentation_data(data: dict) -> PresentationSlideData:
    return PresentationSlideData(**data)
