
# Movie database API Documentation

This document provides an overview of the endpoints available in the Movie database API. The API is built using FastAPI and SQLite is designed to manage movie data and user interactions.

## Endpoints

### POST /users/

Registers a new user.

- **Input**: User registration details including username, password, and role (admin , user ) .
- **Output**: A success message indicating that the user has been created.
- **Dependencies**: Requires a database session.

### POST /login/

Authenticates a user and generates an access token.

- **Input**: Username and password.
- **Output**: An access token and token type (bearer) for successful login.
- **Dependencies**: Requires a database session.

### POST /movies/

Adds a new movie to the database. only Admin user can add new movies

- **Input**: Movie data including title, IMDB ID, year, rating, cast, director, etc.
- **Output**: The added movie's data.
- **Dependencies**: Requires authentication and an authorized role (need Admin user Bearer Token). Requires a database session.

### DELETE /movies/{movie_id}

Deletes a movie from the database. only Admin user can delete the movies

- **Input**: Movie ID (IMDB_ID in db).
- **Output**: A message indicating successful movie deletion.
- **Dependencies**: Requires authentication, an authorized role (need Admin user Bearer Token), and the movie's existence. Requires a database session.

### PUT /movies/modify/{movie_id}

Edits an existing movie's details. only Admin user can edit the details.

- **Input**: Movie ID (IMDB_ID in db) and updated movie data.
- **Output**: A message indicating successful movie update.
- **Dependencies**: Requires authentication, an authorized role (need Admin user Bearer Token), and the movie's existence. Requires a database session.

### GET /movies/search/

Searches for movies based on specified search criteria.

- **Input**: Movie search parameters such as title, year range, rating range, actor, and director.
- **Output**: A list of movies matching the search criteria.
- **Dependencies**: Requires a database session.

### POST /like/{username}/{imdb_id}

Allows a user to like a movie.

- **Input**: User's username and the movie's IMDB ID.
- **Output**: A message indicating that the user liked the movie.
- **Dependencies**: Requires authentication and matching username (need same User Bearer Token). Requires a database session.

### GET /likes/{username}

Retrieves a user's liked movies. Any User can view any User's Likes

- **Input**: User's username.
- **Output**: A list of movies liked by the user.
- **Dependencies**: Requires a database session.

---

# Setup The endpoints Locally


## Prerequisites

Docker

## Getting Started

Follow these steps to run the Dockerized API endpoints:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rangasai12/beyond-assignment.git

2. **Build Docker Image**:
   ```bash
   docker build -t beyondcc .

3. **Run Docker Container**:
   ```bash
   docker run -it -p 8000:8000 beyondcc

---
# Scaling

There are multiple issues that we might encounter and below are strategies to address them:

## Database

this Application is built on SQLite, which is suitable for small to medium scale applications as the user base grows , it might become harder for SQLite to manage the reads and writes

### Solution:
Transition to a more robust database system like PostgreSQL, which has server client architecture

## Concurrent Requests:

large number of requests from regular users can overwhelm the server

### Solution:
Load balancing and horizontal scaling, deploy multiple server instances and distribute the requests.




