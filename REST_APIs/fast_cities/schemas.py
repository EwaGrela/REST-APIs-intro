from pydantic import BaseModel, Field


class CityBase(BaseModel):
    city_id: int
    city: str
    country_id: int
    country: str
    class Config:
        orm_mode = True


class City(CityBase):
    city_id: int
    city: str
    country_id: int
    country: str
    class Config:
        orm_mode = True


class CountryBase(BaseModel):
    country_id: int
    country: str
    class Config:
        orm_mode = True


class Country(CountryBase):
    country_id: int
    country: str
    class Config:
        orm_mode = True