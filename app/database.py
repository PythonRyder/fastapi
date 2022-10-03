#Communicating with database

#copying from fastapi ORM database link


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from time import time
import psycopg2
from psycopg2.extras import RealDictCursor

"""
SQLALCHEMY_DATABSE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

"""
PASSWORD = "PythonRyder"

SQLALCHEMY_DATABSE_URL = 'postgresql://postgres:PythonRyder@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
 
Base = declarative_base()  #all models will be of this base class

# Dependency    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='PythonRyder',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesful")
#         break
#     except Exception as error:
#         print("Some Error",error)
#         time.sleep(3)
