import contextlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from conf.config import settings
from logger.logger import build_logger
from logging import Logger

logger = build_logger("datasource", "INFO")

class DatabaseSessionManager:
    def __init__(self, logger: Logger, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )
        self._logger = logger

    @contextlib.asynccontextmanager
    async def session(self):
        self._logger.info("Creating a new database session")
        if self._session_maker is None:
            raise Exception("Database session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError as e:
            self._logger.error(f"Database operation failed: {e}")
            await session.rollback()
            raise e
        finally:
            await session.close()

sessionmanager = DatabaseSessionManager(logger, settings.DB_URL)

async def get_db():
    async with sessionmanager.session() as session:
        yield session
