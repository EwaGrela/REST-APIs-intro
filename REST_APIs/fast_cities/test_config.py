from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

# to get a string for secret key run:
# openssl rand -hex 32
SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 45

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Single hashing actually, although hard to break but can bu a subject to "rainbow table attack".
# This means that a person who obtains this data, can just prepare themselves with all combinations 
# of unhashed passwords made of 5-6 signs and their hashed equivalent and then obtain the unhashed version.
# One can prevent that by hashing multiple times - hasinh the hash, then the hashed hash, etc

# passwords are hashed using get_password_hash() method from Authenticator, do it and put them in here
users = {
    "ewa_trojanowska": {
        "username": "ewa_trojanowska",
        "hashed_password": "",
        "client_id": 1, 
        "active": True
    },
    "adam_kowalski": {
        "username": "adam_kowalski",
        "hashed_password": "",
        "client_id": 2, 
        "active": True
    },
     "jan_kowalski": {
        "username": "jan_kowalski",
        "hashed_password": "",
        "client_id": 3, 
        "active": False
    }
}

# Ready! Now rename the file to config.py so that your secrets not get commited