from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# SQLAlchemy model representing a fitness class
class FitnessClass(Base):
    __tablename__ = "classes"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for the class
    name = Column(String, nullable=False)  # Name of the class (e.g., Yoga)
    datetime = Column(DateTime, nullable=False)  # Date and time when the class is scheduled
    instructor = Column(String, nullable=False)  # Instructor for the class
    available_slots = Column(Integer, default=0)  # Number of available slots for booking

    # Relationship to access bookings associated with this class
    bookings = relationship("Booking", back_populates="fitness_class")

# SQLAlchemy model representing a booking for a class
class Booking(Base):
    __tablename__ = "bookings"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for the booking
    class_id = Column(Integer, ForeignKey("classes.id"))  # Foreign key to the class being booked
    client_name = Column(String, nullable=False)  # Name of the person making the booking
    client_email = Column(String, nullable=False)  # Email of the person making the booking

    # Relationship to reference the associated fitness class
    fitness_class = relationship("FitnessClass", back_populates="bookings")
