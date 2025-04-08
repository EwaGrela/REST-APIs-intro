import json
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .main import app, get_db
from .models import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
      yield c


@pytest.fixture(scope="module")
def test_user():
    return {"username": "ewa_trojanowska", "password": "secret"}


@pytest.fixture(scope="module")
def test_user_401():
    return {"username": "ewa_grela", "password": "secret"}


@pytest.fixture(scope="module")
def cities_to_post():
    return [
    {"city": "Warsaw", "country_id": 1, "city_id": 1, "country": "Poland"},
    {"city": "Krakow", "country_id": 1, "city_id": 2, "country": "Poland"},
    {"city": "Wroclaw", "country_id": 1, "city_id": 3, "country": "Poland"},
    {"city": "Gdansk", "country_id": 1, "city_id": 4, "country": "Poland"},
    {"city": "Sopot", "country_id": 1, "city_id": 5, "country": "Poland"},
    {"city": "Gdynia", "country_id": 1, "city_id": 6, "country": "Poland"},
    {"city": "Zamosc", "country_id": 1, "city_id": 7, "country": "Poland"},
    {"city": "Bialystok", "country_id": 1, "city_id": 8, "country": "Poland"},
    {"city": "Poznan", "country_id": 1, "city_id": 9, "country": "Poland"},
    {"city": "Gniezno", "country_id": 1, "city_id": 10, "country": "Poland"},
]

@pytest.fixture(scope="module")
def city_names():
    return ["Warsaw", "Krakow", "Wroclaw", "Gdansk", "Sopot", "Gdynia", "Zamosc", "Bialystok", "Poznan", "Gniezno"]

def _basic_helper(client, test_user):
    # authenticate yourself
    token_response = client.post("/token", data=test_user)
    token = token_response.json()["access_token"]
    # post a country and add it into the database
    client.post("/countries", headers={"Authorization": f"Bearer {token}"}, json={"country" : "Poland", "country_id": 1})
    return token

def _helper_method(client, test_user, cities_to_post):
    # authenticate yourself
    token_response = client.post("/token", data=test_user)
    token = token_response.json()["access_token"]
    # post a country and add it into the database
    client.post("/countries", headers={"Authorization": f"Bearer {token}"}, json={"country" : "Poland", "country_id": 1})
    # once the country is succesfully posted, post cities
    for city in cities_to_post:
        client.post("/cities", headers={"Authorization": f"Bearer {token}"}, json=city)
    return token


# GENERAL TESTS
def test_login(client, test_user):
  response = client.post("/token", data=test_user)
  assert response.status_code == 200
  token = response.json()["access_token"]
  assert token is not None


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"sanity_check": "All good"}

def test_get_cities_initial(client, test_db):
    response = client.get("/cities")
    assert response.status_code == 200
    assert response.json() == []

def test_get_countries(client, test_db):
    response = client.get("/countries")
    assert response.status_code == 200
    assert response.json() == []

def test_post_country(client, test_db, test_user):
    # authenticate yourself
    token_response = client.post("/token", data=test_user)
    token = token_response.json().get("access_token")
    # post a country and add it into the database
    response_post = client.post("/countries", headers={"Authorization": f"Bearer {token}"}, json={"country" : "Poland", "country_id": 1})
    assert response_post.status_code == 201
    # check if the country was succesfully added to the database
    response_get = client.get("/countries")
    assert response_get.status_code == 200
    assert response_get.json() == [{"country" : "Poland", "country_id": 1}]

def test_post_cities(client, test_db, test_user, cities_to_post):
    # authenticate yourself
    token_response = client.post("/token", data=test_user)
    token = token_response.json()["access_token"]
    # post a country and add it into the database
    response_post_country = client.post("/countries", headers={"Authorization": f"Bearer {token}"}, json={"country" : "Poland", "country_id": 1})
    assert response_post_country.status_code == 201
    # check if the country was succesfully added to the database
    response_get_countries = client.get("/countries")
    assert response_get_countries.status_code == 200
    assert response_get_countries.json() == [{"country" : "Poland", "country_id": 1}]
    # post cities and check if response is correct
    for city in cities_to_post:
        response = client.post("/cities", headers={"Authorization": f"Bearer {token}"}, json=city)
        assert response.status_code == 201

def test_get_cities(client, test_db, test_user, cities_to_post):
    _helper_method(client, test_user, cities_to_post)
    response_get_cities = client.get("/cities")
    assert response_get_cities.status_code == 200
    assert response_get_cities.json() == [
        {"country_id": 1, "city_id": 1, "city": "Warsaw"},
        {"country_id": 1, "city_id": 2, "city": "Krakow"},
        {"country_id": 1, "city_id": 3, "city": "Wroclaw"},
        {"country_id": 1, "city_id": 4, "city": "Gdansk"},
        {"country_id": 1, "city_id": 5, "city": "Sopot"},
        {"country_id": 1, "city_id": 6, "city": "Gdynia"},
        {"country_id": 1, "city_id": 7, "city": "Zamosc"},
        {"country_id": 1, "city_id": 8, "city": "Bialystok"},
        {"country_id": 1, "city_id": 9, "city": "Poznan"},
        {"country_id": 1, "city_id": 10, "city": "Gniezno"},
    ]

def test_get_city(client, test_db, test_user, cities_to_post, city_names):
    _helper_method(client, test_user, cities_to_post)
    for city_name in city_names:
        response_get_city = client.get(f"/cities/{city_name}")
        assert response_get_city.status_code == 200


def test_delete_city(client, test_db, test_user, cities_to_post, city_names):
    token = _helper_method(client, test_user, cities_to_post)
    response_delete_city = client.delete(f"/cities/Bialystok", headers={"Authorization": f"Bearer {token}"})
    assert response_delete_city.status_code == 204
    # check the cities and their number in the database, find out that deleted city is no longer there
    response_get_cities2 = client.get("/cities")
    assert response_get_cities2.status_code == 200
    assert {"country_id": 1, "city_id": 8, "city": "Bialystok"} not in response_get_cities2.json()


def test_put_city(client, test_db, test_user, cities_to_post):
    token = _helper_method(client, test_user, cities_to_post)
    # now modify one of the cities
    response_put_city = client.put(f"/cities/Bialystok?new_city_name=New Bialystok", headers={"Authorization": f"Bearer {token}"})
    assert response_put_city.status_code == 200
    # check if the change persisted
    response_get_cities2 = client.get("/cities")
    assert response_get_cities2.status_code == 200
    assert len(response_get_cities2.json()) == 10
    assert {"country_id": 1, "city_id": 8, "city": "Bialystok"} not in response_get_cities2.json()
    assert {"country_id": 1, "city_id": 8, "city": "New Bialystok"} in response_get_cities2.json()

# TESTS WITH PARAMATERIZATION
@pytest.mark.parametrize("city_name,expected_response_code", [("Warsaw", 200), ("Gdansk", 200), ("Emerald City", 404)])
def test_get_city_parameterized(client, test_db, test_user, cities_to_post, city_name, expected_response_code):
    _helper_method(client, test_user, cities_to_post)
    response_get_city = client.get(f"/cities/{city_name}")
    assert response_get_city.status_code == expected_response_code


@pytest.mark.parametrize("per_page,page,expected", [(3, 1, [{"country_id": 1, "city_id": 1, "city": "Warsaw"},
        {"country_id": 1, "city_id": 2, "city": "Krakow"},
        {"country_id": 1, "city_id": 3, "city": "Wroclaw"}]),
        (3, 2, [{"country_id": 1, "city_id": 4, "city": "Gdansk"},
        {"country_id": 1, "city_id": 5, "city": "Sopot"},
        {"country_id": 1, "city_id": 6, "city": "Gdynia"}]),
        (6, 1, [{"country_id": 1, "city_id": 1, "city": "Warsaw"},
        {"country_id": 1, "city_id": 2, "city": "Krakow"},
        {"country_id": 1, "city_id": 3, "city": "Wroclaw"},
        {"country_id": 1, "city_id": 4, "city": "Gdansk"},
        {"country_id": 1, "city_id": 5, "city": "Sopot"},
        {"country_id": 1, "city_id": 6, "city": "Gdynia"}]),
        (6, 2, [{"country_id": 1, "city_id": 7, "city": "Zamosc"},
        {"country_id": 1, "city_id": 8, "city": "Bialystok"},
        {"country_id": 1, "city_id": 9, "city": "Poznan"},
        {"country_id": 1, "city_id": 10, "city": "Gniezno"}]),
        (3, 5, [])
        ])

def test_get_cities_paginated(client, test_db, test_user, cities_to_post, per_page, page, expected):
    _helper_method(client, test_user, cities_to_post)
    # check if all cities are there in the database
    response_get_cities = client.get(f"/cities/?per_page={per_page}&page={page}")
    assert response_get_cities.status_code == 200
    assert response_get_cities.json() == expected

# TESTS ERRORS
def test_get_city_404(client, test_db, test_user, cities_to_post, city_names):
    _helper_method(client, test_user, cities_to_post)
    response_get_city = client.get(f"/cities/Sosnowiec")
    assert response_get_city.status_code == 404

def test_post_cities_404(client, test_db, test_user, cities_to_post):
    # authenticate yourself
    token_response = client.post("/token", data=test_user)
    token = token_response.json()["access_token"]
    # post cities and check if response is correct
    for city in cities_to_post:
        response = client.post("/cities", headers={"Authorization": f"Bearer {token}"}, json=city)
        assert response.status_code == 404

def test_post_cities_400(client, test_db, test_user):
    # authenticate yourself
    token = _basic_helper(client, test_user)
    # post cities and check if response is correct
    response = client.post("/cities", headers={"Authorization": f"Bearer {token}"}, json={"city": "London", "country_id": 2, "city_id": 1, "country": "United Kingdom"})
    assert response.status_code == 400

def test_delete_city_404(client, test_db, test_user, cities_to_post):
    token = _helper_method(client, test_user, cities_to_post)
    # delete one of the cities
    response_delete_city = client.delete(f"/cities/Emerald City", headers={"Authorization": f"Bearer {token}"})
    assert response_delete_city.status_code == 404

def test_put_city_404(client, test_db, test_user, cities_to_post):
    token = _helper_method(client, test_user, cities_to_post)
    response_put_city = client.put(f"/cities/Emerald City?new_city_name=New Emerald City", headers={"Authorization": f"Bearer {token}"})
    assert response_put_city.status_code == 404

def test_login_401(client, test_db, test_user_401):
    token_response = client.post("/token", data=test_user_401)
    token_response.status_code == 401

def test_post_countries_401(client, test_db, test_user_401, cities_to_post):
    # authenticate yourself
    token_response = client.post("/token", data=test_user_401)
    token = token_response.json().get("access_token")
    # post cities and check if response is correct
    for city in cities_to_post:
        response = client.post("/countries", headers={"Authorization": f"Bearer {token}"}, json={"country" : "Poland", "country_id": 1})
        assert response.status_code == 401

