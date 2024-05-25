import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class Connection:
    def __enter__(self):
        self.session.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def __init__(self):
        self.__engine = create_engine(Connection.get_connection_string())
        self.session = Session(self.__engine)

    @staticmethod
    def get_connection_string(self):
        host = os.environ.get('DB_HOST')
        port = os.environ.get('DB_PORT')
        database = os.environ.get('DB_NAME')
        username = os.environ.get('DB_USERNAME')
        password = os.environ.get('DB_PASSWORD')

        connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
        print(connection_string)
        return connection_string

    def connect(self):
        return self.__engine.connect()
