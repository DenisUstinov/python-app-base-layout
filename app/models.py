from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pair = Column(String(10), index=True, nullable=False)
    trade_id = Column(Integer, unique=True, nullable=False)
    type = Column(String(4), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    amount = Column(Float)
    ts = Column(BigInteger, index=True, nullable=False)