# Full Stack Trivia API Backend

## Overview
The Casting Agnecy Project is a system that user can create movies, create actors and assgin them to movies, and craate movies categories. each user has a role that he/she can only perform certain action based on his/her permission.

Roles:
    - Casting Assistant:
        - View movies, actors, and categories
    - Casting Director:
        - Same as Casting Assistant permission
        - Add, modify, and delete actors
        - Modify movies
    - Executive Producer:
        - Same as Casting Director permissions
        - Add, delete movies

The motivation of this project is to practice the skills learned during the Udacity FullStack NanoDegree program including
    - Create, Read, Update, Delete (CRUD) from database ([PostgresSQL](https://www.postgresql.org)) using [SQLAlchemy ORM](https://flask-sqlalchemy.palletsprojects.com/en/2.x/).
    - RESTful - API Using [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    - Authentication (Login, Permission, Roles) Using [Auth0](https://auth0.com/)
    - Deploying the project using [Heroku](https://www.heroku.com)

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
No need to set up the database. We will be using Heroku postgres database.

## Running the server

First ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export DATABASE_URL="postgres://vwirrjlhpzkdyl:da3557a09ba598cc6ee87b2d03dd85dce4b988e174b50705a6b31cea7ab953fe@ec2-52-23-86-208.compute-1.amazonaws.com:5432/daih93buo3ntgk"
export AUTH0_DOMAIN='falkhotaifi.us.auth0.com'
export ALGORITHMS=['RS256']
export API_AUDIENCE='castingAgency'
```

## Tasks

### Setup Auth0

To create you own auth0 follow these steps:

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:movies`
    - `add:movie`
    - `update:movie`
    - `delete:movie`
    - `get:actors`
    - `add:actor`
    - `update:actor`
    - `delete:actor`
    - `get:categories`
    - `add:category`
    - `update:category`
    - `delete:category`
6. Create new roles for:
    - Casting Assistant
        - can `get:actors`
        - can `get:categories`
        - can `get:movies`
    - Casting Director
        - can perform all Casting Assistant actions
        - can `add:actor`
        - can `delete:actor`
        - can `update:actor`
        - can `update:movie`
    - ExecutiveProducer
        - can perform all actions

## API Reference

### Getting Started
- Base URL: `https://casting-agency-fsnd-20.herokuapp.com/`

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```
The API will return six error types when requests fail:
- 400: Bad Request
- 401: Unathurize User 
- 403: Insufficient Permission
- 404: Resource Not Found
- 422: Not Processable

### Endpoints 
#### GET /movie
- General:
    - Returns a list of movie objects, success value
    - It accessed only by user with permission 'get:movies'
- Sample: `curl https://casting-agency-fsnd-20.herokuapp.com/movie`

``` 
{
    "movies": [
        {
            "actors": [
                {
                    "age": 59,
                    "id": 4,
                    "name": "GEORGE CLOONEY"
                },
                {
                    "age": 45,
                    "id": 5,
                    "name": "MARGOT ROBBIE"
                }
            ],
            "category": {
                "id": 3,
                "name": "Horror"
            },
            "details": {
                "description": "Elisabeth Moss gets her riot-grrrl on in Her Smell, delivering a tour-de-force performance of rampant egomania and self-destruction that galvanizes Alex Ross Perry’s film.",
                "id": 1,
                "name": "Her Smell"
            }
        }
    ],
    "success": true
}
```

#### POST /movie
- General:
    - Including a body that contains name, description, movie_category_id, actors_id
    - movie_category_id should be only the id of the category
    - actors_id should be a list of only actors id
    - Returns the new movie object and success value
    - It accessed only by user with permission 'post:movie'
- Sample: `curl https://casting-agency-fsnd-20.herokuapp.com/movie -X POST -H "Content-Type: application/json" -d '{ "name": "Dil Bechara", "description": "The emotional journey of two hopelessly in love youngsters, a young girl, Kizie, suffering from cancer, and a boy, Manny, who she meets at a support group.", "movie_category_id": 3, "actors_id": [4, 5] }'`

``` 
{
    "movie": {
        "actors": [
            {
                "actor_id": 4,
                "id": 20,
                "movie_id": 11
            },
            {
                "actor_id": 5,
                "id": 21,
                "movie_id": 11
            }
        ],
        "category": {
            "id": 3,
            "name": "Horror"
        },
        "details": {
            "description": "The emotional journey of two hopelessly in love youngsters, a young girl, Kizie, suffering from cancer, and a boy, Manny, who she meets at a support group 22222.",
            "id": 11,
            "name": "Dil Bechara 22222"
        }
    },
    "success": true
}
```

#### PATCH /movie/<int:movie_id>
- General:
    - Including a body that contains optional name, description, movie_category_id, actors_id
    - movie_category_id should be only the id of the category
    - actors_id should be a list of only actors id
    - Returns the new movie object and success value
    - It accessed only by user with permission 'update:movie'
- Sample: `curl https://casting-agency-fsnd-20.herokuapp.com/movie/11 -X PATCH -H "Content-Type: application/json" -d '{ "name": "Dil Bechara", "description": "The emotional journey of two hopelessly in love youngsters, a young girl, Kizie, suffering from cancer, and a boy, Manny, who she meets at a support group.", "movie_category_id": 3, "actors_id": [4, 5] }'`

``` 
{
    "movie": {
        "actors": [
            {
                "actor_id": 4,
                "id": 20,
                "movie_id": 11
            },
            {
                "actor_id": 5,
                "id": 21,
                "movie_id": 11
            }
        ],
        "category": {
            "id": 3,
            "name": "Horror"
        },
        "details": {
            "description": "The emotional journey of two hopelessly in love youngsters, a young girl, Kizie, suffering from cancer, and a boy, Manny, who she meets at a support group 22222.",
            "id": 11,
            "name": "Dil Bechara 22222"
        }
    },
    "success": true
}
```

#### DELETE /movie/<int:movie_id>
- General:
    - Returns a deleted drink id and success value
    - It accessed only by user with permission 'delete:movie'
- Sample: `curl https://casting-agency-fsnd-20.herokuapp.com/movie/11 -X DELETE`

``` 
{
    "deleted_id": "11",
    "success": true
}
```

#### GET /actor
- General:
    - Returns a list of actor objects, success value
    - It accessed only by user with permission 'get:actors'
- Sample: `curl https://casting-agency-fsnd-20.herokuapp.com/actor`

``` 
{
    "actors": [
        {
            "age": 39,
            "id": 1,
            "name": "CHRIS EVANS"
        }
    ],
    "success": true
}
```

#### POST /actor
- General:
    - Including a body that contains name, age
    - Returns the new actor object and success value
    - It accessed only by user with permission 'post:actor'
- Sample: `curl https://casting-agency-fsnd-20.herokuapp.com/actor -X POST -H "Content-Type: application/json" -d '{ "name": "New Actor", "age": 29}'`

``` 
{
    "actor": {
        "age": 29,
        "id": 6,
        "name": "New Actor"
    },
    "success": true
}
```

#### PATCH /actor/<int:actor_id>
- General:
    - Including a body that contains optinal name, age
    - Returns the new actor object and success value
    - It accessed only by user with permission 'update:actor'
- Sample: `curl https://casting-agency-fsnd-20.herokuapp.com/actor -X PATCH -H "Content-Type: application/json" -d '{ "name": "New Actor", "age": 29}'`

``` 
{
    "actor": {
        "age": 29,
        "id": 6,
        "name": "New Actor"
    },
    "success": true
}
```

#### DELETE /actor/<int:actor_id>
- General:
    - Returns a deleted drink id and success value
    - It accessed only by user with permission 'delete:actor'
- Sample: `curl https://casting-agency-fsnd-20.herokuapp.com/actor/6 -X DELETE`

``` 
{
    "deleted_id": "6",
    "success": true
}
```

#### GET /movieCategory
- General:
    - Returns a list of category objects, success value
    - It accessed only by user with permission 'get:categories'
- Sample: `curl https://casting-agency-fsnd-20.herokuapp.com/movieCategory`

``` 
{
    "movie_categories": [
        {
            "id": 1,
            "name": "Action"
        }
    ],
    "success": true
}
```

#### POST /movieCategory
- General:
    - Including a body that contains name, age
    - Returns the new actor object and success value
    - It accessed only by user with permission 'post:category'
- Sample: `curl https://casting-agency-fsnd-20.herokuapp.com/movieCategory -X POST -H "Content-Type: application/json" -d '{ "name": "New Actor", "age": 29}'`

``` 
{
    "movie_category": {
        "id": 6,
        "name": "New category"
    },
    "success": true
}
```

#### PATCH /movieCategory/<int:movie_category_id>
- General:
    - Including a body that contains name
    - Returns the new actor object and success value
    - It accessed only by user with permission 'update:category'
- Sample: `curl https://casting-agency-fsnd-20.herokuapp.com/movieCategory/6 -X PATCH -H "Content-Type: application/json" -d '{ "name": "New category"}'`

``` 
{
    "movie_category": {
        "id": 6,
        "name": "New category"
    },
    "success": true
}
```

#### DELETE /movieCategory/<int:movie_category_id>
- General:
    - Returns a deleted drink id and success value
    - It accessed only by user with permission 'delete:category'
- Sample: `curl https://casting-agency-fsnd-20.herokuapp.com/movieCategory/6 -X DELETE`

``` 
{
    "deleted_id": "6",
    "success": true
}
```

## Testing
To run the tests, run
```
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency.psql

# To set the configuration of Auth0

export AUTH0_DOMAIN='falkhotaifi.us.auth0.com'
export ALGORITHMS=['RS256']
export API_AUDIENCE='castingAgency'

# To set the token for each role

export CASTING_ASSISTANT_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNGTndGTnhXb1NTVl9uMnNWMEZzWCJ9.eyJpc3MiOiJodHRwczovL2ZhbGtob3RhaWZpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWUyMmU5ZGU4NmZiYjBiYTBjMDRhNDciLCJhdWQiOiJjYXN0aW5nQWdlbmN5IiwiaWF0IjoxNTk3NTAyNTgyLCJleHAiOjE1OTc1MDk3ODIsImF6cCI6IjdIYjY4bkhCeUdIbHZra1JCZk9VME5iWlFoM2J3T0NqIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0OmNhdGVnb3JpZXMiLCJnZXQ6bW92aWVzIl19.o8FiOO1C6hw9yByPcv-IjmO7ZjuJCCx6qzs4jITIej-BWl78I8avY8gM13SDP3GbSy24jCnPOdoAA4eZTP1mwVtb3hhrqtLgYgSaWD5IRBIRjivcaRASyluSOAAdJVFMGkmbIaOQoB5btNzBmM0452rXp7q7Jtis3j90TpVZikwNxzrS7WOUIQaGGxHVTEK5YzzByRprRqnuOv4aDEdHJcftWZKs3N5vaGRvUEj6SXVvvRxQNf6oSANDsizFM0twn98B2-ou4oXtpyUjkFEtuJ4DOnw6tLU-lbmSZiwN892B9Ybkmm51i1j9lZHSwVai5jGyVr2cKKrtvEj4J2BJzQ"

export CASTING_DIRECTER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNGTndGTnhXb1NTVl9uMnNWMEZzWCJ9.eyJpc3MiOiJodHRwczovL2ZhbGtob3RhaWZpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNjIzMDM2Mjg1OTUyMjA3MzI5NiIsImF1ZCI6WyJjYXN0aW5nQWdlbmN5IiwiaHR0cHM6Ly9mYWxraG90YWlmaS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk3NTAyNTQ4LCJleHAiOjE1OTc1MDk3NDgsImF6cCI6IjdIYjY4bkhCeUdIbHZra1JCZk9VME5iWlFoM2J3T0NqIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDptb3ZpZXMiLCJ1cGRhdGU6YWN0b3IiLCJ1cGRhdGU6bW92aWUiXX0.C5yqBM-Nvcc4MY_5r_0MeBKK0_I0Sema0qua9VcjD_ckJ-ywTTdiA-zm5_nP1hRFcrEjJGyVUzDZo9Kd74K07HeP_AtjV5vgwMmRO5ZKBM0vJxRXnkQlv5jCj3THmLBO8pus1_7LozurYcwt90arz1Ww3moDqZUY6YsHxt8o7Ehkt1uHHPFrCVThE6rfKvSTwCExhIBeJKuTKtJKRvV8jOIWt9zEccKfJaxeZGXJXbu5bXStbmIZwpOzzkLb6MI04LFs6f-Z7G1fp2uc6pBAL0wy50BUTMUNd5Y0mDVuNp8RNb9wq34jodWKRPEMVJsVO0L6eQOKFsiUFDPtwF5kAA"

export EXECUTIVE_PRODUCER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNGTndGTnhXb1NTVl9uMnNWMEZzWCJ9.eyJpc3MiOiJodHRwczovL2ZhbGtob3RhaWZpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNjkzNTg5NzczNTQ0ODk2MjYwNCIsImF1ZCI6WyJjYXN0aW5nQWdlbmN5IiwiaHR0cHM6Ly9mYWxraG90YWlmaS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk3NTAyNTE2LCJleHAiOjE1OTc1MDk3MTYsImF6cCI6IjdIYjY4bkhCeUdIbHZra1JCZk9VME5iWlFoM2J3T0NqIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDpjYXRlZ29yeSIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTpjYXRlZ29yeSIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDptb3ZpZXMiLCJ1cGRhdGU6YWN0b3IiLCJ1cGRhdGU6Y2F0ZWdvcnkiLCJ1cGRhdGU6bW92aWUiXX0.EGHa2Jw6pxSBGbTzYMIRKkfPkXmI-gfKe22fpeEKA4ut1QjvFrfCXor-GsWo-9g8F8uHZllGuxQqFd2ylQwg_MptMsvitylLzHrBwpeoIN4pnnuiEd_0OYjvaffu6sw4vBFJB6sFaNpe906VxViuwFFBNe4efFbeqs7MQNCxoJJ0mWa787_ov3jtT6SwEzHOzxjagF_OOuv5Cdi8ccLRCKXPfv4GFmogIDiYUg9kgz5WXoiyIYcHoArKCZSVQeAJMLtPyvcs9Qt1YGrw6pw548uaLFgFeh87tS-3tvW9PeAQ0pRFO_49ehwj5pbQ36A9N5sM2Xlyubou_VhrgQkP2g"

python test_app.py
```