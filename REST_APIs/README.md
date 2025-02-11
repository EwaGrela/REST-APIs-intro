how to run the apps:
1. `basic_flask_app`:
``` source flask_venv/bin/activate
 cd basic_flask_app/

  python app.py
```

2. `basic_fast_api_app`
```aiignore
 source fast_venv/bin/activate
basic_fast_api_app/
fastapi dev main.py
```

3. `flask_cities`
```
 source flask_venv/bin/activate
 ls
 cd flask_cities/
 
 flask --app cities init-db
 flask --app cities run --debug
```
example of POST request body: `{"country_name": "Poland", "city_name": "Zambrow", "country_id": 76}`
example of url for get (searchinh with query params): `http://127.0.0.1:5000/cities_app/cities?per_page=10&page=2&country_name=Poland`

4. `fast_cities`
```
 2060  source fast_venv/bin/activate
 2061  ls
 2062  cd fast_cities
 2063  ls
 2064  fastapi dev main.py

```
example of POST request body: 
to /countries endoint: `{"country" : "Poland", "country_id": 1}`
to /cities endpoint `{"city": "Warsaw", "country_id": 1, "city_id": 1, "country": "Poland"}`