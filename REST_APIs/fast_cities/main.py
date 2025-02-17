from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session


from . import crud, models, schemas
from .db import declarative_base, SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"sanity_check": "All good"}

@app.get("/cities/")
def cities(db: Session = Depends(get_db)):
    all_cities = crud.get_city(db).all()
    return all_cities

@app.post("/cities/", status_code=201)
def cities(city: schemas.CityBase, db: Session = Depends(get_db)):
    countries = crud.get_country(db).all()
    if not countries:
        raise HTTPException(status_code=404, detail="No countries in DB, cannot post cities")
    country_ids = sorted([country.country_id for country in countries])
    data = {}
    data["city"] = city.city
    data["country_id"] = city.country_id
    data["city_id"] = city.city_id
    if data["country_id"] in country_ids:
        crud.post_city(db, city)
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail="Country does not exist, create country first")

@app.get("/cities/{city}", status_code=200)
def single_city(city:str, db: Session = Depends(get_db)):
    city = crud.get_city_by_city_name(db, city)
    if city:
        return {"city": city}
    else:
        raise HTTPException(status_code=404, detail="City does not exist")

@app.delete("/cities/{city}", status_code=204)
def single_city(city:str, db: Session = Depends(get_db)):
    city = crud.get_city_by_city_name(db, city)
    if city:
        crud.delete_city_by_city_name(db, city)
    else:
        raise HTTPException(status_code=404, detail="City does not exist")

@app.get("/countries/", response_model=List[schemas.Country])
def country(db: Session = Depends(get_db)):
    countries = crud.get_country(db).all()
    return countries

@app.post("/countries/")
def country(country: schemas.CountryBase,  db: Session = Depends(get_db)):
    data = {}
    data["country"] = country.country
    data["country_id"] = country.country_id
    crud.post_country(db, country)





