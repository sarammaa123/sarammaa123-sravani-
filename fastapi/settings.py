from sqlalchemy import create_engine
#create_engine is a function from the sqlalchemy
#  module that creates an engine object that connects to the database. 
# It takes a database URL as its argument.
from sqlalchemy.orm import sessionmaker
#sessionmaker is a class from the sqlalchemy.orm module that creates a factory for sessions. 
# It takes an engine object as its argument.
from sqlalchemy.ext.declarative import declarative_base
#declarative_base is a function from the sqlalchemy.ext.declarative module that creates a base class for declarative class definitions. 
# It provides a convenient way to define SQLAlchemy models in object-oriented style
import logging
#tracking and logging messages from the application.
# from service import logger
# from service import logger

#initializes a database engine using SQLAlchemy 
# to connect to a MySQL database hosted locally. 
# It also sets up a sessionmaker to create a session with the database engine. The declarative_base function is used to create a base class that all ORM classes will inherit from.

#It also sets up some constants like SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, and REFRESH_TOKEN_EXPIRE_MINUTES 
# to be used for JWT encoding and decoding.

#Finally, it creates a logger instance using the Python logging module, sets the logging level to INFO, adds a file handler to write logs to a file, and formats the log messages with a timestamp, severity level, and message





engine = create_engine('mysql+pymysql://root:{password}@localhost:3306/{schema}')
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
print('connected')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET_KEY = 'lemoncode21'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_MINUTES = 45
#ALGORITHM is the hashing algorithm used for creating the authentication token.
#


# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler(filename="/Users/sravanisarikonda/Desktop/fastapi/logs/fast_api_logger.log")
handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
