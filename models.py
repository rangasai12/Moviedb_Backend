from sqlalchemy import create_engine, Column, Integer, String, DateTime, Time
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


Base = declarative_base()

class MovieData(Base):
    __tablename__ = 'movies'

    Title = Column(String)
    Year = Column(Integer)
    Summary = Column(String)
    Short_Summary = Column(String)
    IMDB_ID = Column(String, primary_key=True)
    Runtime = Column(Integer)
    YouTube_Trailer = Column(String)
    Rating = Column(String)
    Movie_Poster = Column(String)
    Director = Column(String)
    Writers = Column(String)
    Cast = Column(String)


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  



class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String, index=True)
    IMDB_ID = Column(String,index =True)
    



