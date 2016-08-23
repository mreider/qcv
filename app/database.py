import datetime
from sqlalchemy import create_engine, Integer, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import SETTINGS


class Database:
    '''
        DB interface
    '''

    def __init__(self):
        self.start_engine()

    def start_engine(self):

        # CONNECT
        self.engine = create_engine('mysql+mysqldb://'+SETTINGS['DB_USER_NAME']+':'+SETTINGS['DB_USER_NAME']+'@'+
                                    SETTINGS['DB_HOST']+'/'+SETTINGS['DB_NAME'], echo=False)
        self.connection = self.engine.connect()  # http://mapfish.org/doc/tutorials/sqlalchemy.html
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def get(self,model,key):
        return self.session.query(model).get(key)

    def connection_close(self):
        self.connection.close()

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = 'user_profile'
    user_id = Column(Integer,primary_key=True)
    created = Column(DateTime,default=datetime.datetime.utcnow)