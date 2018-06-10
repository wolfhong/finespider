# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy import Column, String, Text, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from quotespider import settings

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


class Quote(Base):
    __tablename__ = 'quote'

    id = Column(Integer, primary_key=True)
    digest = Column(String(32), nullable=False)
    author = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String(200), nullable=False)
    about = Column(String(100), nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
