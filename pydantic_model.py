from pydantic import BaseModel

from fastapi import HTTPException

class JWTError(HTTPException):
    def __init__(self, status_code: int = 401, detail: str = "JWT token error"):
        super().__init__(status_code=status_code, detail=detail)


class Movie(BaseModel):
    Title: str= None
    Year: int= None
    Summary: str= None
    Short_Summary: str= None
    IMDB_ID: str
    Runtime: int= None
    YouTube_Trailer: str = None
    Rating: str= None
    Movie_Poster: str= None
    Director: str= None
    Writers: str= None
    Cast: str= None

class MovieReq(Movie):

    class Config:
            orm_mode = True
    

class MovieSearch(BaseModel):
    year_from: int = None
    year_to: int = None
    title: str = None
    rating_from: str = None
    rating_to: str = None
    actor: str = None
    director: str = None



class UserBase(BaseModel):
    username:str

class UserCreate(UserBase):
    password:str

class UserDB(UserBase):
    hashedpassword : str

class User(UserBase):
    id: int
    
