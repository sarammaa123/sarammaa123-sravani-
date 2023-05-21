from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from settings import Base, engine
#The code also imports Base and engine from the settings module. 
# Base is an instance of the SQLAlchemy declarative base, which is used to define the structure of database tables. engine is an instance of the SQLAlchemy engine, 
# which is used to connect to a database and perform database operations

class Users(Base):
    __tablename__ = 'users1'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), index=True)
    password = Column(String(255), index=True)
    email = Column(String(50), index=True)
    phone_number = Column(String(15), index=True)
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    create_date = Column(DateTime, default=datetime.now())
    update_date = Column(DateTime)
    token = Column(String(255), index=True)
    token_date = Column(DateTime)

#Overall, this class definition provides a blueprint for creating,
#  querying, and modifying user data in the users1 table of the database.
class UserAuth(Base):
    __tablename__ = 'user_auth'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True, unique=True)
    name = Column(String(255), index=True)
    pho_no = Column(Integer)
    #On the other hand, the UserAuth table seems to be focused specifically on user authentication data, with columns for email address, name, and phone number. It does not have columns for storing sensitive data like passwords or tokens, and is likely used for tracking authentication-related
    #  information such as login attempts, 
    # session management, or user preferences.
  


Base.metadata.create_all(bind=engine)
# creates all the tables defined in the SQLAlchemy ORM models, by issuing the appropriate 
# SQL statements to the database engine specified by engine.