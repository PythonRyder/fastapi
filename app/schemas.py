from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
import email_validator



##################################################################

class UserCreate(BaseModel):
    email : EmailStr
    password : str
    user_phone : str

class UserResponse(BaseModel):          #--|
    user_id : int                       #--|    This is sqlalchemy model                        
    email : EmailStr 
    user_phone : str                   #--|
    created_at : datetime
    #to create pydantic:
    class Config:
        orm_mode = True
        

class UserLogin(BaseModel):
    email : str
    password : str
#To create the schema
# class Post(BaseModel):
#     # post_id : int
#     title: str
#     content: str
#     published: bool=True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass  

class Post(PostBase): #Response Post Structure
    # post_id : int
    title :str
    content : str 
    published : bool
    created_at : datetime 
    owner_id : int
    owner : UserResponse #retrieves the owner info
    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id = int
    created_at : datetime


class Vote(BaseModel):
    post_id : int
    direction : conint(le=1,gt=-1)