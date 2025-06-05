from sqlalchemy import Column, JSON, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), nullable=False, unique=True)
    selectors = Column(JSON, nullable=True)
    timeout = Column(Integer, nullable=True)

class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)