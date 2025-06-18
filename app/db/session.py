from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from .base import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

database_url = os.getenv("DB_URL")

engine = create_async_engine(database_url, echo=False)

Session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    async with Session() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            await db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        try:
            await conn.execute(text("SELECT 1"))
            logger.info("Database connection established successfully.")
        except Exception as e:
            logger.error(f"Error establishing database connection: {e}")
            raise e
        
        try:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully.")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise e

    yield

    await engine.dispose()
