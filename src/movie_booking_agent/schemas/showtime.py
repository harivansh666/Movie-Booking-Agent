from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum
class ShowFormat(str ,Enum):
    TWO_D = "2D"
    THREE_D = "3D"
    IMAX = "IMAX"

class Cinema(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(pattern=r"^cn_\d{3}$")
    name: str = Field(min_length=1)
    city: str = Field(min_length=1)
    address: str = Field(min_length=1)
    amenities: list[str] = Field(default_factory=list)



class Show(BaseModel):
    """A scheduled screening of a movie at a cinema."""

    model_config = ConfigDict(frozen=True)

    id: str = Field(pattern=r"^sh_\d{3}$")
    movie_id: str = Field(pattern=r"^mv_\d{3}$")
    cinema_id: str = Field(pattern=r"^cn_\d{3}$")
    screen: str = Field(min_length=1)
    start_time: datetime
    language: str = Field(min_length=1)
    screen_format: ShowFormat

class ShowSeat(BaseModel):
    