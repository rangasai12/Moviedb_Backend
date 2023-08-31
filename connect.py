import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Base

print("creating tables")

# Read CSV files
movie_df = pd.read_csv("./dataCsv/movie_data.csv")

# Set up SQLite database
db_engine = create_engine('sqlite:///movie_database.db')


Base.metadata.create_all(db_engine)

# Store dataframes in the database
movie_df.to_sql('movies', db_engine, if_exists='replace', index=False)

Session = sessionmaker(bind=db_engine)
