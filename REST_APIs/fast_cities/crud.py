from sqlalchemy.orm import Session

from .models import City, Country
from .schemas import CityBase, CountryBase


def get_city(db: Session):
    return db.query(City)

def get_city_by_city_name(db: Session, city:str):
    city = db.query(City).filter(City.city == city).one_or_none()
    return city

def delete_city_by_city_name(db: Session, city: CityBase):
    db.delete(city)
    db.commit()


def post_city(db: Session, city: CityBase):
    country = db.query(Country).filter(Country.country == city.country).first()
    new_city = City(city=city.city, country=country, city_id=city.city_id, country_id=city.country_id)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city

def get_country(db: Session):
    return db.query(Country)

def post_country(db: Session, country: CountryBase):
    new_country = Country(country=country.country, country_id=country.country_id)
    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country
