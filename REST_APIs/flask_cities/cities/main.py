from flask import (
    Blueprint,
    Flask,
    g,
    redirect,
    render_template,
    request,
    url_for,
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

bp = Blueprint('app', __name__, url_prefix='/cities_app')

@bp.route("/")
def home():
    return "This actually works"


@bp.route("/cities", methods=["GET", "POST"])
def all_cities():
    if request.method == "GET":
        return get_city()
    elif request.method == "POST":
        return post_city()


def get_city():
    country_name = request.args.get('country_name')
    per_page = request.args.get('per_page')
    page = request.args.get('page')
    all_cities = session.query(City).order_by(City.city)
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


def post_city():
    data = request.get_json()
    cities = session.query(City).all()
    countries = session.query(Country).all()
    country_ids = sorted([country.country_id for country in countries])
    city_ids = sorted([city.city_id for city in cities])
    last = session.query(City).filter(City.city_id == city_ids[-1]).one().city_id
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

    return make_response(err, 400)
