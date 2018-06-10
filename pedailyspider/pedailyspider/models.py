from __future__ import unicode_literals
from sqlalchemy import Column, String, Date, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pedailyspider import settings

db_config = settings.DATABASES['default']
engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8mb4'.format(**{
    'user': db_config['user'],
    'password': db_config['password'],
    'host': db_config['host'],
    'port': db_config['port'],
    'dbname': db_config['dbname'],
}), encoding='utf8')


class SessionContext():

    def __init__(self):
        self.session = sessionmaker(bind=engine)()

    def close(self):
        if self.session:
            self.session.close()
            self.session = None

    def __enter__(self):
        return self.session

    def __exit__(self, exc_value, exc_type, exc_traceback):
        self.close()


Base = declarative_base()


class INVModel(Base):
    __tablename__ = 't_inv'

    id = Column(Integer, primary_key=True)
    date_str = Column(String(32), nullable=False)
    date = Column(Date, nullable=False)
    company = Column(String(100), nullable=False)
    company_url = Column(String(256), nullable=False)
    category = Column(String(32), nullable=False)  # industry
    money_stage = Column(String(32), nullable=False)  # A/B/C/pre-A/...
    money_spans = Column(String(32), nullable=False)
    investors = Column(String(256), nullable=False)
    about = Column(String(256), nullable=False)


class IPOModel(Base):
    __tablename__ = 't_ipo'

    id = Column(Integer, primary_key=True)
    date_str = Column(String(32), nullable=False)
    date = Column(Date, nullable=False)
    company = Column(String(100), nullable=False)
    company_url = Column(String(256), nullable=False)
    category = Column(String(32), nullable=False)  # industry
    money_spans = Column(String(32), nullable=False)
    place = Column(String(32), nullable=False)
    place_url = Column(String(256), nullable=False)
    about = Column(String(256), nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
