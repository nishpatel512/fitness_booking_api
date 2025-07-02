from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment or use default SQLite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./booking.db")

# Determine environment (dev/prod) for controlling logging
ENV = os.getenv("ENV", "dev")

# Enable SQL query logging if not in production
echo = ENV != "prod"

# Create an asynchronous SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=echo)

# Create an async session factory bound to the engine
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Base class for declaring models using SQLAlchemy ORM
Base = declarative_base()

# Function to initialize the database (creates tables if they don't exist)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
