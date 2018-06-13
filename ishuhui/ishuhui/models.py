from __future__ import unicode_literals
from sqlalchemy import Column, String, Text, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ishuhui import settings

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


class Chapter(Base):
    __tablename__ = 't_chapter'

    id = Column(Integer, primary_key=True)
    cartoon = Column(String(100), nullable=False)
    chapter = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    url = Column(String(256), nullable=False)
    images = Column(Text, nullable=False)


class Book(Base):
    __tablename__ = 't_book'

    id = Column(Integer, primary_key=True)
    cartoon = Column(String(100), nullable=False)
    url = Column(String(256), nullable=False)
    chapter_count = Column(Integer, nullable=False, default=0)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
