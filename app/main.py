from http.client import HTTPException
from msilib import schema
from poplib import CR
from pyexpat import model
from time import time
from typing import Optional,List
from click import command
from fastapi import FastAPI, Response, status,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import random, randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models , schemas

from . database import engine, SessionLocal, get_db
# from sqlalchemy.orm import Session
from .routers import post, user, auth, votes
from .config import settings

from fastapi.middleware.cors import CORSMiddleware


# #Once you know alembic this commad line is no longer needed
# models.Base.metadata.create_all(bind=engine)

 
app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) #CORSMiddleware is function which runs before a request

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)



archeive = []


# class UpdatedPost(BaseModel): 
#     title: str
#     content: str
#     published: bool=True
#     rating : Optional[float] = 9.8


my_posts = [{'title':'title of post 62', 'content': 'content of post 62','id':62},{'title':'title of post 63', 'content': 'I like Pizza','id':63}]


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post


def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            # print(index)
            return index
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} is not found.")


# find_index_post(62)
def _update_database(post:schemas.Post):
    my_posts.append(post)

################ ######################################################################################################




@app.get("/")
async def root():
    print("Welcome to my API !!!")
    return {"message": "Hello World Welcome to my API !!!"}


########################################################################################################################





