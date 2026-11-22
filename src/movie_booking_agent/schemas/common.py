# Seat status 
from pydantic import BaseModel, ConfigDict, Field
from typing import Enum, Annotated


PriceInr = Annotated(int, Field(gt=0, description="Amount in whole Indian rupees (INR)."))

SeatLabel = Annotated(str, Field(min_length=2, max_length=3,  pattern=r"^[A-Za-z]\d{1,2}$", description="Seat label such as A1 or B10.",))

class SeatStatus(str, Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    RESERVED = "reserved"

# Seat category 
class SeatCategory(str, Enum):
    REGULAR = "regular"
    PREMIUM = "premium"
    RECLINER = "recliner"

class BookingStatus(str, Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


# Payment Status 
class PaymentStatus(str, Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class ErrorCode(str, Enum):
    NOT_FOUND = "not_found"
    INVALID_INPUT = "invalid_input"
    SEAT_UNAVAILABLE = "seat_unavailable"
    PAYMENT_FAILED = "payment_failed"
    BOOKING_NOT_CANCELLABLE = "booking_not_cancellable"
    INTERNAL_ERROR = "internal_error"

class ErrorInfo(BaseModel):
    model_config = ConfigDict(frozen=True) # frozen = Ek baar Pydantic model ka object create ho gaya, toh uske attributes ki values change nahi kar sakte.
    code: ErrorCode
    message : str = Field(min_length=1)

# sare project ke shared enums aur chhote pydantic types yaha he hai 
# ek he jgah se status/category/error values define hote hain. 