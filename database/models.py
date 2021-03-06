import os
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

# -- LOCAL DATABASE -- #
# database_name = "casting_agency"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

actors_assign_to_movie = db.Table(
    'actors_assign_to_movie',
    db.Column(
        'movie_id',
        db.Integer,
        db.ForeignKey('Movie.id'),
        primary_key=True),
    db.Column(
        'actor_id',
        db.Integer,
        db.ForeignKey('Actor.id'),
        primary_key=True),
)


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    movie_category_id = Column(Integer)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_updated = Column(DateTime, nullable=False, default=datetime.utcnow)
    actors = db.relationship(
        'Actor',
        secondary=actors_assign_to_movie,
        backref=db.backref('movies', lazy=True))

    def __init__(self, name, description, movie_category_id, actors):
        self.name = name
        self.description = description
        self.movie_category_id = movie_category_id
        self.actors = actors

    def format_short(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'actors': [actor.format() for actor in self.actors]
        }
    
    def format_long(self):
        return {
            'details': {
                'id': self.id,
                'name': self.name,
                'description': self.description
            },
            'actors': [actor.format() for actor in self.actors]
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_updated = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class MovieCategory(db.Model):
    __tablename__ = 'Movie_Category'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_updated = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class MovieActorAssign(db.Model):
    __tablename__ = 'Movie_Actor_Assign'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('Movie.id', ondelete="CASCADE"))
    actor_id = Column(Integer, ForeignKey('Actor.id', ondelete='CASCADE'))
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_updated = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()