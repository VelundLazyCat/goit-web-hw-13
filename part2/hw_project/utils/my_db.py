
import configparser
import pathlib
import psycopg2

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)


username = config.get('DB_DEV', 'USER')
password = config.get('DB_DEV', 'PASSWORD')
db_name = config.get('DB_DEV', 'DB_NAME')
host = config.get('DB_DEV', 'HOST')
port = config.get('DB_DEV', 'PORT')

url_to_db = f"postgresql+psycopg2://{username}:{
    password}@{host}:{port}/{db_name}"


engine = create_engine(url_to_db, echo=True, pool_size=5)
Session = sessionmaker(bind=engine)
session = Session()
