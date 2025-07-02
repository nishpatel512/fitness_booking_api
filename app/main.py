import os
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from zoneinfo import ZoneInfo

# Import database session and initialization function
from .database import SessionLocal, init_db

# Import schemas for request/response validation
from .schemas import FitnessClassResponse, BookingRequest, BookingResponse

# Import business logic and utilities
from . import crud, utils
from .utils import logger

# Default timezone for classes, configurable via environment variable
default_timezone = os.getenv("TIMEZONE", "Asia/Kolkata")

# Initialize FastAPI application
app = FastAPI()

# Startup event to initialize database
@app.on_event("startup")
async def on_startup():
    logger.info("Starting application and initializing DB.")
    await init_db()

# Dependency to get database session
async def get_db():
    async with SessionLocal() as session:
        yield session

# Endpoint to list all available fitness classes with timezone conversion
@app.get("/classes", response_model=List[FitnessClassResponse])
async def list_classes(
    tz: str = Query(default="Asia/Kolkata", description="Target timezone, e.g. UTC, America/New_York"),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"GET /classes called with tz={tz}")
    
    # Validate the timezone string
    try:
        target_tz = ZoneInfo(tz)
    except Exception:
        logger.warning(f"Invalid timezone received: {tz}")
        raise HTTPException(status_code=400, detail="Invalid timezone")

    # Retrieve all classes from the database
    classes = await crud.get_all_classes(db)

    # Convert class datetime to the requested timezone
    for c in classes:
        c.datetime = utils.convert_timezone(c.datetime, tz)

    logger.info(f"Returning {len(classes)} classes after timezone conversion")
    return classes

# Endpoint to book a slot in a fitness class
@app.post("/book", response_model=BookingResponse)
async def book_class(booking: BookingRequest, db: AsyncSession = Depends(get_db)):
    logger.info(f"POST /book called with booking: {booking}")
    try:
        # Attempt to create a booking in the specified class
        result = await crud.create_booking(db, **booking.dict())
        logger.info(f"Booking successful for client: {booking.client_email} for class_id: {booking.class_id}")
        return result
    except ValueError as ve:
        # Raise 400 error if booking fails (e.g., class not found or overbooked)
        logger.error(f"Booking failed: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

# Endpoint to fetch bookings by client email
@app.get("/bookings", response_model=List[BookingResponse])
async def get_bookings(email: str = Query(...), db: AsyncSession = Depends(get_db)):
    logger.info(f"GET /bookings called for email: {email}")
    
    # Fetch all bookings associated with the given email
    bookings = await crud.get_bookings_by_email(db, email)
    logger.info(f"Returning {len(bookings)} bookings for {email}")
    return bookings
