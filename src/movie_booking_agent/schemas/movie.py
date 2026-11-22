from pydantic import BaseModel, Field
from typing import Enum
from pydantic import BaseModel, ConfigDict, Field
from datetime import date

class Certification(str, Enum):
    U = 'U'
    UA = 'UA'
    A = 'A'

class Movie(BaseModel):
    """A movie that can be discovered and booked."""

    model_config = ConfigDict(frozen=True)

    id: str = Field(pattern=r"^mv_\d{3}$", description="Stable movie ID, e.g. mv_001.")
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    genres: list[str] = Field(min_length=1)
    languages: list[str] = Field(min_length=1)
    duration_minutes: int = Field(gt=0, le=360)
    rating: float = Field(ge=0.0, le=10.0, description="Audience rating out of 10.")
    certification: Certification
    release_date: date
