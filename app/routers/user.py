from http.client import HTTPException
from msilib import schema
from poplib import CR
from pyexpat import model
from time import time
from typing import Optional,List
from click import command
from fastapi import FastAPI, Response, status,Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import random, randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import  models, schemas, utils
from .. database import engine,SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags="Users")

#New User Information:
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db: Session=Depends(get_db)):

    #Hashing the password: - user.password

    hashed_password = utils.hash(user.password) 
    user.password = hashed_password

    new_user = models.User(**user.dict()) # "**" for unpacking
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #just like "returning * "

    return new_user

#####################################################################################################################
@router.get("/users/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def get_user(id:int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"User with id: {id} does not exist.")
    return user