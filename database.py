from sqlalchemy import create_engine # Used to create a connection to our Database
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib.parse

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

safe_password = urllib.parse.quote_plus(MYSQL_PASSWORD)

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{safe_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

##Connection
engine = create_engine(DATABASE_URL, echo = True)

##Session
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

##Base 
Base = declarative_base() # Where SQLalchemy model will be inherited.
