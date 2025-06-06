from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings



# If Render (or your prod environment) has provided DATABASE_URL,
# use that entire string. Otherwise, build from the individual pieces.
if settings.DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL


else:
    # fall back to local .env fields (localhost, etc.) for dev

    # Creating an SQL conection string
    SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# This dependency creates the session to our database on request
def get_db():
    db = SessionLocal()
    try:
        yield db
    
    finally:
        db.close()
