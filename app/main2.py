from http.client import HTTPException
from msilib import schema
from poplib import CR
from pyexpat import model
from sys import prefix
from time import time
from typing import Optional,List
from click import command
from fastapi import FastAPI, Response, status,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import random, randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils

from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
# from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI() 
# app = FastAPI(prefix="/posts") #reducing the path for router 

archeive = []



while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='PythonRyder',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesful")
        break
    except Exception as error:
        print("Some Error",error)
        time.sleep(3)



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

# app.include_router(post.router)
# app.include_router(user.router)

# from http.client import HTTPException
# from msilib import schema
# from poplib import CR
# from pyexpat import model
# from time import time
# from typing import Optional,List
# from click import command
# from fastapi import APIRouter, FastAPI, Response, status,Depends
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import random, randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from . import models, schemas
# from . database import engine,SessionLocal, get_db
# from sqlalchemy.orm import Session

# router = APIRouter(
#     prefix = "/posts"    
#     tags = ["Posts"] 
# )  #reducing the path for router 



my_posts = [{'title':'title of post 62', 'content': 'content of post 62','id':62},{'title':'title of post 63', 'content': 'I like Pizza','id':63}]

def _update_database(post:schemas.Post):
    my_posts.append(post)


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    return posts

###############################################################################################################

@app.post("/createposts")
def create_posts(new_post: schemas.CreatePost):

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

@app.post("/createpost")
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
# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_posts(post:Post):
#     cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,
#     (post.title,post.content,post.published))
#     new_post = cursor.fetchone()
#     conn.commit()

#     return {'data':new_post}


###############################################################################################################
post_ids = []
for post in my_posts:
    post_ids.append(post['id'])

# print(post_ids)


@app.get("/posts/{id}")  #, response_model=schemas.Post
async def get_post(id:int, db:Session=Depends(get_db)): 
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

 

@app.get("/posts/latest")
def get_latest_post():
    return my_posts[-1]


###############################################################################################################

#DELETE




@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    #find the index in the array that has required  
    # cursor.execute("""DELETE from posts where post_id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # print(deleted_post)

    # index = find_index_post(id)
    # print(index)

    post_query = db.query(models.Post).filter(models.Post.post_id==id)

    if post_query.first()  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                detail = f"post with id:{id} does not exists")
    # my_posts.pop(index)
    # archeive.append(post_deleted)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

######################
#upd ate
@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.post_id == id)
    post = post_query.first()
    print(post)

    if post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post id {id} does not exist.") #,detail = f"post with id:{id} does not exists")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first() 

######################################################################################################################
#Update

# @app.put("/posts/{id}")
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

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return{"data":posts}


#####################################################################################################################

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.Post, db: Session=Depends(get_db)): 
    # print(**post.dict())
    new_post = models.Post(**post.dict())
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    #adding to the database
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #just like "returning * "

    return new_post

@app.get("/")
def root():
    print("Welcome to my API !!!")
    return {"message": "Hello World Welcome to my API !!!"}


########################################################################################################################


#New User Information:
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
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
@app.get("/users/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def get_user(id:int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"User with id: {id} does not exist.")
    return user


