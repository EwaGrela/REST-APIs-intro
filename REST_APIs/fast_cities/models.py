from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String
from .db import Base
from sqlalchemy.orm import relationship

class Country(Base):
    __tablename__ = 'country'
    country_id = Column(SmallInteger, primary_key=True)
    country = Column(String(50), nullable=False, unique=True)


class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False, unique=True)
    country_id = Column(ForeignKey('country.country_id'), nullable=False, index=True)
    country = relationship('Country')