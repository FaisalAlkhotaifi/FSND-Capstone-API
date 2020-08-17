import os
import sys
from datetime import datetime
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database.models import setup_db
from database.models import Movie
from database.models import Actor
from database.models import MovieCategory
from database.models import MovieActorAssign
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def hello():
        return "Welcome to Casting Agency API!"

    # Movie Endpoints

    @app.route('/movie')
    @requires_auth('get:movies')
    def getMovies(token):
        movies = Movie.query.order_by(Movie.date_updated).all()
        movies_formatted = []

        if movies is not None and len(movies) != 0:
            for movie in movies:
                single_movie = movie.format_long()

                category = MovieCategory.query.filter_by(
                    id=movie.movie_category_id
                  ).one_or_none()
                if category is not None:
                    single_movie['category'] = category.format()
                else:
                    single_movie['category'] = {}

                movies_formatted.append(single_movie)

        return jsonify({
            'success': True,
            'movies': movies_formatted
        })

    @app.route('/movie', methods=['POST'])
    @requires_auth('add:movie')
    def addMovie(token):
        body = request.get_json()

        movie_formatted = {}

        try:
            name = body.get('name', None)
            desc = body.get('description', None)
            movie_category_id = body.get('movie_category_id', None)
            actors_id = body.get('actors_id', None)

            # Check of any missing parameter.
            if name is None \
               or desc is None \
               or movie_category_id is None \
               or actors_id is None:
                abort(400)

            actors = []
            if actors_id is not None \
               and type(actors_id) is list:
                actors = Actor.query.filter(Actor.id.in_(actors_id)).all()

            movie = Movie(
                name=name, 
                description=desc, 
                movie_category_id=movie_category_id,
                actors=actors
            )

            movie.insert()

            movie_formatted = movie.format_long()

            # getting category details
            category = MovieCategory.query.filter_by(
              id=movie.movie_category_id
            ).one_or_none()
            if category is not None:
                movie_formatted['category'] = category.format()
            else:
                movie_formatted['category'] = {}

            return jsonify({
                'success': True,
                'movie': movie_formatted
            })
        except Exception as e:
            abort(422)

    @app.route('/movie/<movie_id>', methods=['PATCH'])
    @requires_auth('update:movie')
    def updateMovie(token, movie_id):
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)

        body = request.get_json()
        name = body.get('name', None)
        description = body.get('description', None)
        movie_category_id = body.get('movie_category_id', None)
        actors_id = body.get('actors_id', None)

        movie_formatted = {}

        # Check that at least there is one parameter to be updated
        if name is None \
           and description is None \
           and movie_category_id is None \
           and actors_id is None:
            abort(400)

        try:
            # only update the provided parameter
            if name is not None:
                movie.name = name
            if description is not None:
                movie.description = description
            if movie_category_id is not None:
                movie.movie_category_id = movie_category_id
            if actors_id is not None \
               and type(actors_id) is list:
                actors = Actor.query.filter(Actor.id.in_(actors_id)).all()
                movie.actors = actors

            movie.update()

            movie_formatted = movie.format_long()

            # getting category details
            category = MovieCategory.query.filter_by(
                id=movie.movie_category_id
              ).one_or_none()
            if category is not None:
                movie_formatted['category'] = category.format()
            else:
                movie_formatted['category'] = {}

            return jsonify({
                'success': True,
                'movie': movie_formatted
            })
        except Exception as e:
            abort(422)

    @app.route('/movie/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def deleteMovie(token, movie_id):
        movie = Movie.query \
                .filter_by(id=movie_id) \
                .one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.delete()

            return jsonify({
                "success": True,
                "deleted_id": movie_id
            })
        except Exception as e:
            abort(422)
    
    # Actor Endpoints

    @app.route('/actor')
    @requires_auth('get:actors')
    def getActor(token):
        actors = Actor.query.order_by(Actor.date_updated).all()
        actors_formatted = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': actors_formatted
        })

    @app.route('/actor', methods=['POST'])
    @requires_auth('add:actor')
    def addActor(token):
        body = request.get_json()

        try:
            name = body.get('name', None)
            age = body.get('age', None)

            # Check of any missing parameter.
            if name is None or age is None:
                abort(400)
            
            actor = Actor(name=name, age=age)
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception as e:
            abort(422)

    @app.route('/actor/<actor_id>', methods=['PATCH'])
    @requires_auth('update:actor')
    def updateActor(token, actor_id):
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)

        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)

        # Check that at least there is one parameter to be updated
        if name is None and age is None:
            abort(400)

        try:
            # only update the provided parameter
            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception as e:
            abort(422)
    
    @app.route('/actor/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def deleteActor(token, actor_id):
        actor = Actor.query \
                .filter_by(id=actor_id) \
                .one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()

            return jsonify({
                "success": True,
                "deleted_id": actor_id
            })
        except Exception as e:
            abort(422)

    # Movie Category Endpoints

    @app.route('/movieCategory')
    @requires_auth('get:categories')
    def getMovieCategory(token):
        movie_categories = MovieCategory.query.order_by(
            MovieCategory.date_updated
          ).all()
        movie_categories_formatted = [
            movie_category.format() for movie_category in movie_categories
        ]

        return jsonify({
            'success': True,
            'movie_categories': movie_categories_formatted
        })

    @app.route('/movieCategory', methods=['POST'])
    @requires_auth('add:category')
    def addMovieCategory(token):
        body = request.get_json()

        try:
            name = body.get('name', None)

            # Check of any missing parameter.
            if name is None:
                abort(400)
            
            movie_category = MovieCategory(name=name)
            movie_category.insert()

            return jsonify({
                'success': True,
                'movie_category': movie_category.format()
            })
        except Exception as e:
            abort(422)

    @app.route('/movieCategory/<movie_category_id>', methods=['PATCH'])
    @requires_auth('update:category')
    def updateMovieCategory(token, movie_category_id):
        movie_category = MovieCategory.query.filter_by(
            id=movie_category_id
          ).one_or_none()
        if movie_category is None:
            abort(404)

        body = request.get_json()
        name = body.get('name', None)

        # Check of missing name
        if name is None:
            abort(400)

        try:
            movie_category.name = name
            movie_category.update()

            return jsonify({
                'success': True,
                'movie_category': movie_category.format()
            })
        except Exception as e:
            abort(422)

    @app.route('/movieCategory/<movie_category_id>', methods=['DELETE'])
    @requires_auth('delete:category')
    def deleteMovieCategory(token, movie_category_id):
        movie_category = MovieCategory.query \
                .filter_by(id=movie_category_id) \
                .one_or_none()

        if movie_category is None:
            abort(404)

        try:
            movie_category.delete()

            return jsonify({
                "success": True,
                "deleted_id": movie_category_id
            })
        except Exception as e:
            abort(422)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def not_authorize(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unathurize user"
        }), 401

    @app.errorhandler(403)
    def insufficient_permission(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "insufficient permission"
        }), 403

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run()