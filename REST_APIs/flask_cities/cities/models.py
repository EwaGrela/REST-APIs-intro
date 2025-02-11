from sqlalchemy import (CheckConstraint, Column, DateTime, ForeignKey,
                        Index, Integer, LargeBinary, Numeric, SmallInteger, String, Table, Text, text)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata



class Country(Base):
    __tablename__ = 'country'

    country_id = Column(SmallInteger, primary_key=True)
    country = Column(String(50), nullable=False)
    last_update = Column(DateTime, nullable=False)


class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    country_id = Column(ForeignKey('country.country_id'), nullable=False, index=True)
    last_update = Column(DateTime, nullable=False)
    country = relationship('Country')

