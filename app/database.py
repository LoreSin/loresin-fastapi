from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# postgresql+psycopg2://headmaster:master@192.168.0.3:5432/academy?client_encoding=utf8'
# SQLALCHEMY_DATABASE_URL = \
#     "postgresql://headmaster:master@192.168.0.3:5432/article"
# SQLALCHEMY_DATABASE_URL = \
#     "postgresql://postgres:secret@192.168.0.3:5432/fastapi"

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}_test".format(
    settings.database_username,
    settings.database_password,
    settings.database_hostname,
    settings.database_port,
    settings.database_name,
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL  # , connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
