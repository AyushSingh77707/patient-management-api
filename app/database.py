from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

engine=create_engine(settings.DATABASE_URL)

sessionlocal=Session(bind=engine)

Base=declarative_base()


#fastapi dependency injection
def get_session():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()

    


