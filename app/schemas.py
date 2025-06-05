# Defines the pydantic schemas of request and response to/from the API
from email.message import EmailMessage
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


''' 2 this schema controls account creation for users, it controls the request and response'''
# This schema handles requests for users to create account(request model)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# This schema handles response after users have created their account(response model)
class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True




'''1 this schema controls post request and response'''
# This is a schema for the requests (i.e, user sending data to us) and it gives performs validations on post requests validation. (request model)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


# This is a schema for the response(i.e, we sending data to the user), (response model)
class Post(PostBase):
    post_id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True


class PostOut(Post):
    likes: int

    class Config:
        orm_mode = True


''' 3 this schema controls user login, it controls the request and response and provides validation'''
# This schema handles requests for users to login(request model)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# This schema handles response during users login(response model)
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None



''' 4 this schema controls user likes, it controls the request and response and provides validation'''
class LikeAction(BaseModel):
    post_id: int
    liked: bool


    class Config:
        orm_mode = True
