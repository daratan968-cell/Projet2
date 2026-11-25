from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

try:
    if settings.database_url.startswith("postgresql"):
        engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 2},
        )
        with engine.connect() as conn:
            pass
    else:
        engine = create_engine(settings.database_url)
except (SQLAlchemyError, OSError):
    # Резервный SQLite, если контейнер PostgreSQL временно остановлен
    engine = create_engine(
        "sqlite:///./quizai.db",
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
