from datetime import timedelta
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .models import Token, User
from .auth_helpers import fake_db, ACCESS_TOKEN_EXPIRE_MINUTES, status
from .auth_helpers import Authenticator
from .db import declarative_base, SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
authenticator = Authenticator()

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


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticator.authenticate_user(fake_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authenticator.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(authenticator.get_current_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(authenticator.get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/cities/")
def cities(current_user: Annotated[User, Depends(authenticator.get_current_user)], db: Session = Depends(get_db)):
    client_id = current_user.client_id
    all_cities = crud.get_city(client_id, db).all()
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





