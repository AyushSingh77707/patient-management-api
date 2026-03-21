#DATABASE CONNECTION SETUP
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

database_url="postgresql://postgres:04122033@localhost:5432/projectdb"
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

    


