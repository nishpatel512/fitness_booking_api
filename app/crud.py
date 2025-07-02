from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import FitnessClass, Booking
from .utils import logger

# Fetch all fitness classes from the database
async def get_all_classes(db: AsyncSession):
    logger.info("Fetching all fitness classes from the database.")
    result = await db.execute(select(FitnessClass))  # Asynchronously execute SELECT query
    classes = result.scalars().all()  # Extract all FitnessClass objects from result
    logger.info(f"Fetched {len(classes)} classes.")
    return classes

# Create a booking for a given class ID and client details
async def create_booking(db: AsyncSession, class_id: int, client_name: str, client_email: str):
    logger.info(f"Attempting to create booking for class_id={class_id}, client_email={client_email}")

    # Fetch the class from DB to check for existence and availability
    result = await db.execute(select(FitnessClass).filter(FitnessClass.id == class_id))
    fitness_class = result.scalar_one_or_none()

    if not fitness_class:
        logger.warning(f"Booking failed: Class ID {class_id} not found.")
        raise ValueError("Class not found")

    if fitness_class.available_slots <= 0:
        logger.warning(f"Booking failed: No available slots for class ID {class_id}.")
        raise ValueError("No slots available")

    # Create new booking record and decrement available slots
    booking = Booking(class_id=class_id, client_name=client_name, client_email=client_email)
    fitness_class.available_slots -= 1

    db.add(booking)  # Add booking to session
    logger.info(f"Booking created. Slots remaining for class_id={class_id}: {fitness_class.available_slots}")
    await db.commit()  # Commit transaction
    await db.refresh(booking)  # Refresh booking to get updated data from DB

    return booking

# Retrieve all bookings made by a given email
async def get_bookings_by_email(db: AsyncSession, email: str):
    logger.info(f"Fetching bookings for email: {email}")
    result = await db.execute(select(Booking).filter(Booking.client_email == email))
    bookings = result.scalars().all()  # Extract all bookings from result
    logger.info(f"Found {len(bookings)} bookings for {email}")
    return bookings
