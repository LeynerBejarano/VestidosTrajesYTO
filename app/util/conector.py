import logging
from sqlalchemy import create_engine
from config import DATABASE_PATH

engine = create_engine(DATABASE_PATH)
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)