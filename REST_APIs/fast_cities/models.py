from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String
from .db import Base
from sqlalchemy.orm import relationship


from datetime import datetime, timedelta, timezone


from pydantic import BaseModel

# Those are not detained in the main database
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    client_id: int
    username: str
    email: str | None = None
    full_name: str | None = None
    active: bool | None = None


class UserInDB(User):
    hashed_password: str

# These are datained in DB

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