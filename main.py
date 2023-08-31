from fastapi import FastAPI, HTTPException,Depends
import jwt
# from passlib.context import CryptContext
from connect import Session
from models import MovieData
import models
from typing import List
import pydantic_model
from passlib.context import CryptContext
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

# from pydantic_model import Movie,MovieSearch


SECRET_KEY = "83knnjh23kjh490923894832423488333jh"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALLOWED_ROLES = ["admin", "user"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def get_current_user_role(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        if role !="admin":
            raise HTTPException(status_code=403, detail="Permission denied")
        return role
    except:
        raise HTTPException(status_code=401, detail="Token invalid or expired")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_user = payload.get("sub")
        if not token_user:
            raise HTTPException(status_code=403, detail="Permission denied")
        return token_user
    except:
        raise HTTPException(status_code=401, detail="Token invalid or expired")
    

def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()



@app.post("/users/")
def create_user(username: str, password: str, roletype: str, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    if roletype not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role") 
    
    hashed_password = password_context.hash(password)
    new_user = models.User(username=username, hashed_password=hashed_password, role=roletype)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"user created"}


@app.post("/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not password_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/movies/")
def create_movie(movie: pydantic_model.Movie,current_user_role: str = Depends(get_current_user_role),session: Session = Depends(get_db)):
    existing_movie = session.query(MovieData).filter(MovieData.IMDB_ID == movie.IMDB_ID).first()
    if existing_movie:
        # session.close()
        raise HTTPException(status_code=404, detail="Movie with the same IMDB_ID already exists")
    db_movie = MovieData(**movie.dict())
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    # session.close()
    return movie

@app.delete("/movies/{movie_id}")
def delete_movie(
    movie_id: str,
    current_user_role: str = Depends(get_current_user_role),
    session: Session = Depends(get_db)
):
    movie = session.query(MovieData).filter(MovieData.IMDB_ID == movie_id).first()
    if movie:
        session.delete(movie)
        session.commit()
        # session.close()
        return {"message": "Movie deleted"}
    raise HTTPException(status_code=404, detail="Movie not found")


@app.put("/movies/modify/{movie_id}")
def edit_movie(
    movie_id: str,
    updated_movie: pydantic_model.Movie,current_user_role: str = Depends(get_current_user_role),session: Session = Depends(get_db)):
    movie = session.query(MovieData).filter(MovieData.IMDB_ID == movie_id).first()
    if movie:
        for key, value in updated_movie.dict().items():
            setattr(movie, key, value)
        session.commit()
        # session.close()
        return {"message": "Movie updated"}
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get("/movies/search/", response_model=List[pydantic_model.Movie])
async def search_movies(search_params: pydantic_model.MovieSearch = Depends(),session: Session = Depends(get_db)):

    query = session.query(MovieData)

    if search_params.year_from:
        query = query.filter(MovieData.Year >= search_params.year_from)
    if search_params.year_to:
        query = query.filter(MovieData.Year <= search_params.year_to)
    if search_params.title:
        query = query.filter(MovieData.Title.ilike(f'%{search_params.title}%'))
    if search_params.rating_from:
        query = query.filter(MovieData.Rating >= search_params.rating_from)
    if search_params.rating_to:
        query = query.filter(MovieData.Rating <= search_params.rating_to)
    if search_params.actor:
        query = query = query.filter(MovieData.Cast.ilike(f'%{search_params.actor}%'))

    if search_params.director:
        query = query = query.filter(MovieData.Director.ilike(f'%{search_params.director}%'))

    movies = query.all()
    # session.close()

    response_movies = [pydantic_model.Movie(**movie.__dict__) for movie in movies]
    return response_movies

@app.post("/like/{username}/{imdb_id}")
async def like_movie(username: str, imdb_id: str,current_user_role: str = Depends(get_current_user), db: Session = Depends(get_db)):

    if username!=current_user_role:
        raise HTTPException(status_code=404, detail="User not Authorized") 
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    movie = db.query(MovieData).filter(MovieData.IMDB_ID == imdb_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    existing_like = (
        db.query(models.Likes)
        .filter(models.Likes.username == username, models.Likes.IMDB_ID == imdb_id)
        .first()
    )
    if existing_like is None:
        like = models.Likes(username=username, IMDB_ID=imdb_id)
        db.add(like)
        db.commit()

    return {"message": f"User {username} liked movie {movie.Title}"}

@app.get("/likes/{username}")
async def get_user_likes(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    liked_movies = (
        db.query(MovieData)
        .join(models.Likes, models.Likes.IMDB_ID == MovieData.IMDB_ID)
        .filter(models.Likes.username == username)
        .all()
    )
    
    return {"user": user.username, "liked_movies": liked_movies}