from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Base schema for a fitness class used for input/output operations
class FitnessClassBase(BaseModel):
    name: str = Field(..., min_length=1)  # Name must be at least 1 character
    datetime: datetime  # Date and time of the class (in ISO 8601 format)
    instructor: str = Field(..., min_length=1)  # Instructor name must be provided
    available_slots: int = Field(..., ge=0)  # Slots must be 0 or more

# Response schema used when returning a fitness class from the API
class FitnessClassResponse(FitnessClassBase):
    id: int  # Unique identifier of the class

    class Config:
        orm_mode = True  # Enables ORM model parsing with SQLAlchemy objects

# Schema for incoming booking requests (API POST /book)
class BookingRequest(BaseModel):
    class_id: int  # ID of the class to be booked
    client_name: str = Field(..., min_length=1)  # Name of the person booking
    client_email: EmailStr  # Validated email address of the client

# Response schema used when returning a booking from the API
class BookingResponse(BaseModel):
    id: int  # Unique identifier of the booking
    class_id: int  # ID of the associated class
    client_name: str = Field(..., min_length=1)  # Name of the person who booked
    client_email: EmailStr  # Email of the person who booked

    class Config:
        orm_mode = True  # Enables ORM model parsing with SQLAlchemy objects
