from curses.ascii import HT
from datetime import datetime,timedelta
from itsdangerous import NoneAlgorithm
from jose import JWTError, jwt

from app import models
from . import schemas, database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from .config import settings



oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl='login',)

SECRET_KEY = settings.secrete_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


#
def create_access_token(data:dict):
    """
    Gets encoded token on the basis of data and the expiration time,
    which gets passed into jwt.encode() gets encoded jwt token.
    """

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode , SECRET_KEY, algorithm= [ALGORITHM])

    return encoded_jwt 

#Rt
def verify_access_token(token:str, credentials_exceptions):
    """
    retruns token data after entering token after verifying thet user is in the system
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)

        id:str = payload.get("user_id")

        if id is None:
            raise credentials_exceptions
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exceptions

    return token_data

#
def get_current_user(token:str=Depends(oauth2_scheme),db:Session= Depends(database.get_db)):
    credentials_exceptions = HT(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"could not validate credentials",
                                headers = {"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token, credentials_exceptions)

    user = db.query(models.User).filte(models.User.user_id == token.id).first()


    return user