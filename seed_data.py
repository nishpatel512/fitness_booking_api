import asyncio
from datetime import datetime, timedelta
from app.database import SessionLocal, init_db
from app.models import FitnessClass
from zoneinfo import ZoneInfo
from app.utils import logger

# Asynchronous function to populate initial fitness class data
async def seed():
    # Initialize the database (create tables if not exist)
    await init_db()

    # Start a new async DB session
    async with SessionLocal() as session:
        ist = ZoneInfo("Asia/Kolkata")  # Set timezone to IST
        now = datetime.now(ist)  # Current time in IST

        logger.info("Seeding fitness classes...")

        # Create 3 demo fitness class entries with different instructors and times
        classes = [
            FitnessClass(
                name="Yoga",
                datetime=now + timedelta(days=1),
                instructor="Anita",
                available_slots=1
            ),
            FitnessClass(
                name="Zumba",
                datetime=now + timedelta(days=2),
                instructor="Ravi",
                available_slots=8
            ),
            FitnessClass(
                name="HIIT",
                datetime=now + timedelta(days=3),
                instructor="Sneha",
                available_slots=10
            ),
        ]

        # Add all classes to the session and commit the transaction
        session.add_all(classes)
        await session.commit()

        logger.info("Seeding complete. 3 classes added.")

if __name__ == "__main__":
    asyncio.run(seed())
