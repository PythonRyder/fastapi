from http.client import HTTPException
from msilib import schema
from poplib import CR
from pyexpat import model
from time import time
from typing import Optional,List
from click import command
from fastapi import APIRouter, FastAPI, Response, status,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import random, randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import func

from app import oauth2
from .. import models, schemas ,oauth2
from .. database import engine,SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags="Posts")

my_posts = [{'title':'title of post 62', 'content': 'content of post 62','id':62},{'title':'title of post 63', 'content': 'I like Pizza','id':63}]

def _update_database(post:schemas.Post):
    my_posts.append(post)


@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    return posts

###############################################################################################################

@router.post("/createposts")
def create_posts(new_post: schemas.CreatePost,db:Session=Depends(get_db), 
                    get_current_user:int=Depends(oauth2.get_current_user)):

    post_dict = new_post.dict()
    post_dict = {
        'title': "favourite fruit",
        'content': "PuranPoli",
        'published': True
        # 'rating' :  9.8,
    }

    # userInput:
    # post_dict['title'] = str(input("Enter The tile of the post:"))
    # post_dict['content'] = str(input("Enter The content of the post:"))
    # post_dict['published'] = input("Do you want it to be published(True/False):")
    # post_dict['rating'] = float(input("rate your own Post:"))

    post_dict['id'] = randrange(0,100000000)

    my_posts.append(post_dict)
    #update database:
    _update_database(post_dict)
    # print(my_posts)
    return my_posts
print(my_posts)

# a_demo_dict = [{'title':'title of post 62', 'content': 'content of post 62','id':randrange(0,100000000)]
# create_posts(a_demo_dict)

#To create the schema for the data received from the client:Pydantic module
#TODO:Define the structure 
#title:str, content:str, published:boolean


###############################################################################################################

@router.post("/createpost")
def Create_post_path(id:float,title:str,content:str,published:bool):

    post_dict = schemas.Post.dict()
    # title_post = str(input("Enter The tile of the post:"))
    # content_tobe_posted = str(input("Enter The content of the post:"))
    # true_or_false = input("Do you want it to be published(True/False):")
    # id_of_post = float(id)  
    # post_dict['title'] = title_post
    # post_dict['content'] = content_tobe_posted
    # post_dict['published'] = true_or_false
    # post_dict['rating'] =   id_of_post    
    post_dict['id'] = id
    post_dict['title'] = title
    post_dict['content'] = content
    post_dict['published'] = published
    
    my_posts.append(post_dict)
    #update database:
    _update_database(post_dict)
    # print(my_posts)
    return my_posts

################################################################################################################


# print(my_posts)
# @router.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_posts(post:Post):
#     cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,
#     (post.title,post.content,post.published))
#     new_post = cursor.fetchone()
#     conn.commit()

#     return {'data':new_post}


###############################################################################################################
#To get 

@router.get("/posts")
def get_posts(db:Session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user),
                limit:int=10,skip:int=0, search:Optional[str]=" "): 
    """
    
    """
    print(limit,skip,search)
    # posts = db.querry(models.Post).filter(models.Post.owner_id==current_user.user_id).all()
    posts = db.querry(models.Post).filter(models.Post.owner_id==current_user.user_id).limit(limit).offset(skip).all()

    return posts 
###############################################################################################################
#To get anothother version of above get posts:

@router.get("/posts")
def get_posts(db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user),
                limit:int = 10 , skip:int = 0, search:Optional[str] = ""): 
    """
        To get anothother version of above get posts: Chaging filter criteria:
    """
    print(limit,skip,search)
    # posts = db.querry(models.Post).filter(models.Post.owner_id==current_user.user_id).all()
    posts = db.querry(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #this will fetch the posts with "content" with "search" parameter values.
    #this will outer join the tables and group by 
    results = db.query(models.Post, func.count()).join(models.Vote, 
                        models.Vote.post_id == models.Post.post_id, isouter=True).group_by(models.Post.id) 
    print(results)
    return posts 

###############################################################################################################

post_ids = []
for post in my_posts:
    post_ids.append(post['id'])

# print(post_ids)


@router.get("/posts/{id}")  #, response_model=schemas.Post
async def get_post(id:int, db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user)): 
    # print(**post.dict()): 
    # print(id)
    # cursor.execute("""SELECT * FROM posts WHERE post_id = %s""",(str(id)))
    # test_post = cursor.fetchone()
    # print(test_post)
 

    # for post in my_posts: 
    #     if id == post['id']:
    #         break 
    # else:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
    #                         detail=f"post with id {id} is not found.")
        # post = None
        # response.status_code = status.HTTP_404_NOT_FOUND #404
        # return {"message":f"post with id {id} is not found."} 
    # return {"Post Details":post}
    # return my_posts[f"{id}"] 
    post = db.query(models.Post).filter(models.Post.post_id==id).first()
    # print(type(post))

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"Post with id {id} does not exist.")
                                    
    if post.owner_id != current_user.post_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorised perform requested action")

    return post   

@router.get("/posts/latest")
def get_latest_post():
    return my_posts[-1]


###############################################################################################################

#DELETE
@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user)): 
    # print(**post.dict()):
    #find the index in the array that has required  
    # cursor.execute("""DELETE from posts where post_id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # print(deleted_post)

    # index = find_index_post(id)
    # print(index)

    post_query = db.query(models.Post).filter(models.Post.post_id==id)

    post = post_query.first()

    if post_query.first()  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                detail = f"post with id:{id} does not exists")
    # my_posts.pop(index)
    # archeive.append(post_deleted)

    #Checking if the the attept to delete owner's own post and others posts:
    if post.owner_id != current_user.post_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

######################


#upd ate

@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.CreatePost, db: Session = Depends(get_db),current_user:int= Depends(oauth2.get_current_user)): 
    # print(**post.dict()):

    post_query = db.query(models.Post).filter(models.Post.post_id == id)
    post = post_query.first()
    print(post)

    post_query = db.query(models.Post).filter(models.Post.post_id==id)

    post = post_query.first()

    if post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post id {id} does not exist.") #,detail = f"post with id:{id} does not exists")
                               
    if post.owner_id != current_user.post_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised perform requested action")

 
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first() 

######################################################################################################################
#Update

# @router.put("/posts/{id}")
# def update_post(id:int, updated_post:scemas.Post, db: Session = Depends(get_db)):
#     #using database connection
#     # cursor.execute("""UPDATE posts 
#     #                 SET title = %s, content =%s, published=%s where post_id = %s returning * """, (post.title,post.content,post.published,str(id) ))
#     # test_updated_post = cursor.fetchone()
#     # conn.commit()
#     # print(test_updated_post) 
    
#     # index = find_index_post(id)
#     # print(post)
#     # print(index)

#     post_query = db.query(models.scemas.Post).filter(models.Post.post_id == id)
#     post = post_query.first()
#     print(post)

#     if post  == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post id {id} does not exist.") #,detail = f"post with id:{id} does not exists")
    
#     post_query.update(updated_post.dict(), synchronize_session=False)

#     # post_dict = post.dict()
#     # post_dict['id'] = id 
#     # my_posts[te] = post_dict
#     # return {"data":post_dict}
#     db.commit()

#     return({'data': post_query.first()})

##############################################################################################################
#Test:

@router.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return{"data":posts}


#####################################################################################################################

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.Post, db: Session=Depends(get_db), current_user:int= Depends(oauth2.get_current_user)): 
    """
    
    """
    print(current_user.email)
    # print(**post.dict())
    new_post = models.Post(owner_id = current_user.post_id,**post.dict())
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    #adding to the database
    db.add(new_post)   
    db.commit()
    db.refresh(new_post) #just like "returning * "

    return new_post
