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
from .. import  models, schemas, utils, database, models, oauth2
from .. database import engine,SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/votes", tags="Votes")

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db : Session =Depends(database.get_db()),
        current_user: int = Depends(oauth2.get_current_user)):
        vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)

        found_vote = vote_query.first()

        if (vote.dir == 1):
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                        detail=f"user {current_user.id} has already voted on this post {vote.post_id}.")
            new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.user_id)   
            db.add(new_vote)         
            db.commit()
            return {"message": "succesfully added vote."}       
        else:
            if not found_vote:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Vote does not exist.")
            
            vote_query.delete(synchronize_session=False)

            db.commit()
            return {"message": "succesfully deleted vote."}       



    
