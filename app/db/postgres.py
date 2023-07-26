import psycopg2  # Pastikan telah menginstal driver psycopg2

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, isolation_level="AUTOCOMMIT", pool_pre_ping=True,
                       connect_args={
                           "keepalives": 1,
                           "keepalives_idle": 30,
                           "keepalives_interval": 10,
                           "keepalives_count": 5,
                       })

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


Base = declarative_base()
