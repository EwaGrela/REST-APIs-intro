from flask import (
    Blueprint,
    request,
    jsonify,
    make_response
)

from flask_sqlalchemy import SQLAlchemy
from .models import City, Country
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import collate
from datetime import datetime
import os

from cities.db import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///instance/cities.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Session = sessionmaker(bind=engine)
session = Session()

class DBInterface:

    def _find_all_cities(self):
        return session.query(City).order_by(City.city)


    def get_city(self):
        country_name = request.args.get('country_name')
        per_page = request.args.get('per_page')
        page = request.args.get('page')
        all_cities = self._find_all_cities()
        if country_name is None:
            if per_page is None and page is None:
                cities = all_cities.all()
            elif per_page is not None and page is None:
                cities = all_cities.limit(int(per_page)).all()
            elif per_page is not None and page is not None:
                cities = all_cities.limit(int(per_page)).offset((int(page) - 1) * int(per_page)).all()
        else:
            country = session.query(Country)
            my_country = country.filter(Country.country == country_name).one()
            country_id = my_country.country_id
            country_cities = all_cities.filter(City.country_id == country_id)
            if per_page is None and page is None:
                cities = country_cities.all()
            elif per_page is not None and page is None:
                cities = country_cities.limit(int(per_page)).all()
            elif per_page is not None and page is not None:
                cities = country_cities.limit(int(per_page)).offset((int(page) - 1) * int(per_page)).all()
        c = [city.city for city in cities]
        return jsonify(c)

    def post_city(self):
        data = request.get_json()
        cities = self._find_all_cities().all()
        countries = session.query(Country).all()
        country_ids = sorted([country.country_id for country in countries])
        city_ids = sorted([city.city_id for city in cities])
        last = self._find_all_cities().filter(City.city_id == city_ids[-1]).one().city_id
        if data["country_id"] in country_ids:
            new_city = City(city_id=(last + 1), city=data["city_name"], country_id=data["country_id"],
                            last_update=datetime.utcnow())
            session.add(new_city)
            session.commit()
            new_city = {"country_id": new_city.country_id, "city_name": new_city.city, "city_id": new_city.city_id}
            new_city = jsonify(new_city)
            return make_response(new_city, 201)
        else:
            err = {"error": "Invalid country_id"}
            err = jsonify(err)
            return make_response(err, 400)
    
    def get_city_by_name(self, city_name):
        all_cities = self._find_all_cities()
        city_found = all_cities.filter(City.city == city_name).one_or_none()
        if city_found:
            city = {"city": city_found.city, "country": city_found.country.country}
            return jsonify(city)
        else:
            err = {"error": "No such city"}
            return make_response(err, 404)
        
    def delete_city_with_name(self, city_name):
        all_cities = self._find_all_cities()
        city_to_delete = all_cities.filter(City.city == city_name).one_or_none()
        if city_to_delete:
            deleted_city = {"city": city_to_delete.city, "country": city_to_delete.country.country}
            session.delete(city_to_delete)
            session.commit()
            return make_response(deleted_city, 204)
        else:
            err = {"error": "No such city"}
            make_response(err, 404)
        


interface = DBInterface()

bp = Blueprint('app', __name__, url_prefix='/cities_app')

@bp.route("/")
def home():
    return "This actually works"


@bp.route("/cities", methods=["GET", "POST"])
def all_cities():
    if request.method == "GET":
        return interface.get_city()
    elif request.method == "POST":
        return interface.post_city()

@bp.route("cities/<city_name>", methods=["GET", "DELETE"])
def single_city(city_name):
    if request.method == "GET":
        return interface.get_city_by_name(city_name)
    elif request.method == "DELETE":
        return interface.delete_city_with_name(city_name)




