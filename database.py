#DATABASE CONNECTION SETUP
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


#setting up environment
from dotenv import load_dotenv
import os
load_dotenv()

database_url=os.getenv("DATABASE_URL")
engine=create_engine(database_url)

sessionlocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base()


#fastapi dependency injection
def get_session():
    session=sessionlocal()
    try:
        yield session
    finally:
        session.close()

    


