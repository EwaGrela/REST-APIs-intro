from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt 
from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError

from .config import pwd_context, oauth2_scheme, users, ALGORITHM, SECRET_KEY
from .models import UserInDB, TokenData



class Authenticator:

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)


    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def get_user(db, username: str):
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)


    def authenticate_user(self, users, username: str, password: str):
        user = self.get_user(users, username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user


    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = self.get_user(users, username=token_data.username)
        if user is None:
            raise credentials_exception
        if user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user

