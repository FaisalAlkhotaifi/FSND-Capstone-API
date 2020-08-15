import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Movie, Actor, MovieCategory, MovieActorAssign

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgres://localhost:5432/casting_agency_test"
        setup_db(self.app, self.database_path)

        self.casting_assistant_header = {
            'Authorization': 'Bearer ' + os.environ['CASTING_ASSISTANT_TOKEN']
        }
        self.casting_director_header = {
            'Authorization': 'Bearer ' + os.environ['CASTING_DIRECTER_TOKEN']
        }
        self.executive_producer_header = {
            'Authorization': 'Bearer ' + os.environ['EXECUTIVE_PRODUCER_TOKEN']
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # ------------------- #
    ### HELPER METHODS ###
    # -------------------#

    def assertNotEmpty(self, object):
        self.assertTrue(object)

    def assertSuccess(self, data, statusCode):
        self.assertEqual(statusCode, 200)
        self.assertEqual(data['success'], True)

    def assert404request(self, data, statusCode):
        self.assertEqual(statusCode, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def assert400request(self, data, statusCode):
        self.assertEqual(statusCode, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def assert422request(self, data, statusCode):
        self.assertEqual(statusCode, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def assert401request(self, data, statusCode):
        self.assertEqual(statusCode, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unathurize user')
    
    def assert403request(self, data, statusCode):
        self.assertEqual(statusCode, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'insufficient permission')

    ## ----------- MOVIES ------------- ##
    # ---------------------------------- #
    ###     TEST GET MOVIES REQUEST    ###
    # ---------------------------------- #
    
    # Test when using no token used
    def test_41_401_get_movie(self):
        res = self.client().get('/movie')
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting assistant token
    def test_42_get_movie_by_assistant(self):
        res = self.client().get(
            '/movie', 
            headers=self.casting_assistant_header
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)

    # Test when using casting director token
    def test_43_get_movie_by_director(self):
        res = self.client().get(
            '/movie', 
            headers=self.casting_director_header
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)

    # Test when using executive producer token
    def test_44_get_movie_by_producer(self):
        res = self.client().get(
            '/movie', 
            headers=self.executive_producer_header
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)

    # ---------------------------------- #
    ###     TEST POST MOVIE REQUEST    ###
    # ---------------------------------- #

    # Test when using no token used
    def test_45_401_post_movie(self):
        res = self.client().post('/movie')
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting assistant token
    def test_46_401_post_movie_by_assistant(self):
        res = self.client().post(
            '/movie', 
            headers=self.casting_assistant_header
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)

    # Test when using casting director token
    def test_47_401_post_movie_by_director(self):
        res = self.client().post(
            '/movie', 
            headers=self.casting_director_header
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting director token
    def test_48_400_post_movie_by_producer(self):
        res = self.client().post(
            '/movie', 
            headers=self.executive_producer_header,
            json={}
        )
        data = json.loads(res.data)

        self.assert422request(data, res.status_code)

    # Test when using executive producer token
    def test_49_post_movie_by_producer(self):
        res = self.client().post(
            '/movie', 
            headers=self.executive_producer_header,
            json={
                "name": "test movie name",
                "description": "test movie description",
                "movie_category_id": 11,
                "actors_id": [4, 5]
            }
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)
        self.assertNotEmpty(data['movie'])

    # ---------------------------------- #
    ###    TEST PATCH MOVIE REQUEST    ###
    # ---------------------------------- #

    # Test when using no token used
    def test_50_401_patch_movie(self):
        res = self.client().patch('/movie/1')
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting assistant token
    def test_51_401_patch_movie_by_assistant(self):
        res = self.client().patch(
            '/movie/1', 
            headers=self.casting_assistant_header,
            json={}
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using executive producer token and no body
    def test_52_400_patch_movie_by_producer(self):
        first_movie = Movie.query.order_by(Movie.id.desc()).first()
        if first_movie is not None:
            res = self.client().patch(
                f'/movie/{first_movie.id}', 
                headers=self.executive_producer_header,
                json={}
            )
            data = json.loads(res.data)

            self.assert400request(data, res.status_code)
        else:
            pass
    
    # Test when using executive producer token and none exist actor
    def test_53_404_patch_movie_by_director(self):
        res = self.client().patch(
            '/movie/1000', 
            headers=self.executive_producer_header
        )
        data = json.loads(res.data)

        self.assert404request(data, res.status_code)

    # Test when using casting director token
    def test_54_patch_movie_by_director(self):
        first_movie = Movie.query.order_by(Movie.id.desc()).first()
        if first_movie is not None:
            res = self.client().patch(
                f'/movie/{first_movie.id}', 
                headers=self.casting_director_header,
                json={
                    "name": "test movie name 222",
                    "description": "test movie description 222",
                    "movie_category_id": 11,
                    "actors_id": [4, 5]
                }
            )
            data = json.loads(res.data)

            self.assertSuccess(data, res.status_code)
            self.assertNotEmpty(data['movie'])
        else:
            pass

    # Test when using executive producer token
    def test_55_patch_movie_by_producer(self):
        first_movie = Movie.query.order_by(Movie.id.desc()).first()
        if first_movie is not None:
            res = self.client().patch(
                f'/movie/{first_movie.id}', 
                headers=self.executive_producer_header,
                json={
                    "name": "test movie name 222",
                    "description": "test movie description 222",
                    "movie_category_id": 11,
                    "actors_id": [4, 5]
                }
            )
            data = json.loads(res.data)

            self.assertSuccess(data, res.status_code)
            self.assertNotEmpty(data['movie'])
        else:
            pass
  
    # ---------------------------------- #
    ###    TEST DELETE MOVIE REQUEST   ###
    # ---------------------------------- #

    # Test when using no token used
    def test_56_delete_movie(self):
        res = self.client().delete('/movie/1')
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting assistant token
    def test_57_401_delete_movie_by_assistant(self):
        res = self.client().delete(
            '/movie/1', 
            headers=self.casting_assistant_header
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)

    # Test when using casting director token
    def test_58_401_delete_movie_by_director(self):
        res = self.client().delete(
            '/movie/1', 
            headers=self.casting_assistant_header
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using executive producer token and none exist actor
    def test_59_404_delete_movie_by_producer(self):
        res = self.client().delete(
            '/movie/1000', 
            headers=self.executive_producer_header
        )
        data = json.loads(res.data)

        self.assert404request(data, res.status_code)

    # Test when using executive producer token
    def test_60_delete_movie_by_producer(self):
        first_movie = Movie.query.order_by(Movie.id.desc()).first()
        if first_movie is not None:
            res = self.client().delete(
                f'/movie/{first_movie.id}', 
                headers=self.executive_producer_header
            )
            data = json.loads(res.data)

            self.assertSuccess(data, res.status_code)
            self.assertNotEmpty(data['deleted_id'])
        else: 
            pass

    ## ----------- ACTORS ------------- ##
    # ---------------------------------- #
    ###     TEST GET ACTOR REQUEST     ###
    # ---------------------------------- #

    # Test when using no token used
    def test_01_401_get_actor(self):
        res = self.client().get('/actor')
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting assistant token
    def test_02_get_actor_by_assistant(self):
        res = self.client().get(
            '/actor', 
            headers=self.casting_assistant_header
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)

    # Test when using casting director token
    def test_03_get_actor_by_director(self):
        res = self.client().get(
            '/actor', 
            headers=self.casting_director_header
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)

    # Test when using executive producer token
    def test_04_get_actor_by_producer(self):
        res = self.client().get(
            '/actor', 
            headers=self.executive_producer_header
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)

    # ---------------------------------- #
    ###     TEST POST ACTOR REQUEST    ###
    # ---------------------------------- #

    # Test when using no token used
    def test_05_401_post_actor(self):
        res = self.client().post('/actor')
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting assistant token
    def test_06_401_post_actor_by_assistant(self):
        res = self.client().post(
            '/actor', 
            headers=self.casting_assistant_header,
            json={}
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)

    # Test when using casting director token
    def test_07_post_actor_by_director(self):
        res = self.client().post(
            '/actor', 
            headers=self.casting_director_header,
            json={
                "name": "test actor name 1",
                "age": 23
            }
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)
        self.assertNotEmpty(data['actor'])

    # Test when using executive producer token
    def test_08_post_actor_by_producer(self):
        res = self.client().post(
            '/actor', 
            headers=self.executive_producer_header,
            json={
                "name": "test actor name 2",
                "age": 25
            }
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)
        self.assertNotEmpty(data['actor'])

    # Test when using casting director token
    def test_09_400_post_actor_by_director(self):
        res = self.client().post(
            '/actor', 
            headers=self.casting_director_header
        )
        data = json.loads(res.data)

        self.assert422request(data, res.status_code)

    # ---------------------------------- #
    ###    TEST PATCH ACTOR REQUEST    ###
    # ---------------------------------- #

    # Test when using no token used
    def test_10_401_patch_actor(self):
        res = self.client().patch('/actor/1')
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting assistant token
    def test_11_401_patch_actor_by_assistant(self):
        res = self.client().patch(
            '/actor/1', 
            headers=self.casting_assistant_header,
            json={}
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting director token and none exist actor
    def test_12_404_patch_actor_by_director(self):
        res = self.client().patch(
            '/actor/1000', 
            headers=self.casting_director_header
        )
        data = json.loads(res.data)

        self.assert404request(data, res.status_code)

    # Test when using casting director token and no body
    def test_13_400_patch_actor_by_director(self):
        first_actor = Actor.query.order_by(Actor.id.desc()).first()
        if first_actor is not None:
            res = self.client().patch(
                f'/actor/{first_actor.id}', 
                headers=self.casting_director_header,
                json={}
            )
            data = json.loads(res.data)

            self.assert400request(data, res.status_code)
        else:
            pass

    # Test when using casting director token
    def test_14_patch_actor_by_director(self):
        first_actor = Actor.query.order_by(Actor.id.desc()).first()
        if first_actor is not None:
            res = self.client().patch(
                f'/actor/{first_actor.id}', 
                headers=self.casting_director_header,
                json={
                    "name": "test actor name 3",
                    "age": 23
                }
            )
            data = json.loads(res.data)

            self.assertSuccess(data, res.status_code)
            self.assertNotEmpty(data['actor'])
        else:
            pass

    # Test when using executive producer token
    def test_15_patch_actor_by_producer(self):
        first_actor = Actor.query.order_by(Actor.id.desc()).first()
        if first_actor is not None:
            res = self.client().patch(
                f'/actor/{first_actor.id}', 
                headers=self.executive_producer_header,
                json={
                    "name": "test actor name 4",
                    "age": 25
                }
            )
            data = json.loads(res.data)

            self.assertSuccess(data, res.status_code)
            self.assertNotEmpty(data['actor'])
        else:
            pass
  
    # ---------------------------------- #
    ###   TEST DELETE ACTOR REQUEST    ###
    # ---------------------------------- #

    # Test when using no token used
    def test_16_delete_actor(self):
        res = self.client().delete('/actor/1')
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting assistant token
    def test_17_401_delete_actor_by_assistant(self):
        res = self.client().delete(
            '/actor/1', 
            headers=self.casting_assistant_header
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting director token and none exist actor
    def test_18_404_delete_actor_by_director(self):
        res = self.client().delete(
            '/actor/1000', 
            headers=self.casting_director_header
        )
        data = json.loads(res.data)

        self.assert404request(data, res.status_code)

    # Test when using casting director token
    def test_19_delete_actor_by_director(self):
        first_actor = Actor.query.order_by(Actor.id.desc()).first()
        if first_actor is not None:
            res = self.client().delete(
                f'/actor/{first_actor.id}', 
                headers=self.casting_director_header
            )
            data = json.loads(res.data)

            self.assertSuccess(data, res.status_code)
            self.assertNotEmpty(data['deleted_id'])
        else: 
            pass

    # Test when using executive producer token
    def test_20_delete_actor_by_producer(self):
        first_actor = Actor.query.order_by(Actor.id.desc()).first()
        if first_actor is not None:
            res = self.client().delete(
                f'/actor/{first_actor.id}', 
                headers=self.executive_producer_header
            )
            data = json.loads(res.data)

            self.assertSuccess(data, res.status_code)
            self.assertNotEmpty(data['deleted_id'])
        else: 
            pass
    
    ## --------- CATEGORIES ----------- ##
    # ---------------------------------- #
    ###   TEST GET CATEGORIES REQUEST  ###
    # ---------------------------------- #

    # Test when using no token used
    def test_21_401_get_category(self):
        res = self.client().get('/movieCategory')
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting assistant token
    def test_22_get_category_by_assistant(self):
        res = self.client().get(
            '/movieCategory', 
            headers=self.casting_assistant_header
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)

    # Test when using casting director token
    def test_23_get_category_by_director(self):
        res = self.client().get(
            '/movieCategory', 
            headers=self.casting_director_header
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)

    # Test when using executive producer token
    def test_24_get_category_by_producer(self):
        res = self.client().get(
            '/movieCategory', 
            headers=self.executive_producer_header
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)

    # ---------------------------------- #
    ###  TEST POST CATEGORIES REQUEST  ###
    # ---------------------------------- #

    # Test when using no token used
    def test_25_401_post_category(self):
        res = self.client().post('/movieCategory')
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting assistant token
    def test_26_401_post_category_by_assistant(self):
        res = self.client().post(
            '/movieCategory', 
            headers=self.casting_assistant_header,
            json={}
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)

    # Test when using casting director token
    def test_27_401_post_category_by_director(self):
        res = self.client().post(
            '/movieCategory', 
            headers=self.casting_director_header,
            json={}
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using executive producer token
    def test_28_400_post_category_by_producer(self):
        res = self.client().post(
            '/movieCategory', 
            headers=self.executive_producer_header
        )
        data = json.loads(res.data)

        self.assert422request(data, res.status_code)

    # Test when using executive producer token
    def test_29_post_category_by_producer(self):
        res = self.client().post(
            '/movieCategory', 
            headers=self.executive_producer_header,
            json={
                "name": "test category name 1",
            }
        )
        data = json.loads(res.data)

        self.assertSuccess(data, res.status_code)
        self.assertNotEmpty(data['movie_category'])

    # ---------------------------------- #
    ###  TEST PATCH CATEGORIES REQUEST ###
    # ---------------------------------- #

    # Test when using no token used
    def test_30_401_patch_category(self):
        res = self.client().patch('/movieCategory/1')
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting assistant token
    def test_31_401_patch_category_by_assistant(self):
        res = self.client().patch(
            '/movieCategory/1', 
            headers=self.casting_assistant_header,
            json={}
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)

    # Test when using casting director token
    def test_32_patch_category_by_director(self):
        res = self.client().patch(
            '/movieCategory/1',
            headers=self.casting_director_header,
            json={}
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using executive producer token and no body
    def test_33_400_patch_category_by_director(self):
        first_category = MovieCategory.query.order_by(MovieCategory.id.desc()).first()
        if first_category is not None:
            res = self.client().patch(
                f'/movieCategory/{first_category.id}', 
                headers=self.executive_producer_header,
                json={}
            )
            data = json.loads(res.data)

            self.assert400request(data, res.status_code)
        else:
            pass
    
    # Test when using executive producer token and none exist actor
    def test_34_404_patch_category_by_producer(self):
        res = self.client().patch(
            '/movieCategory/1000', 
            headers=self.executive_producer_header
        )
        data = json.loads(res.data)

        self.assert404request(data, res.status_code)

    # Test when using executive producer token
    def test_35_patch_category_by_producer(self):
        first_category = MovieCategory.query.order_by(MovieCategory.id.desc()).first()
        if first_category is not None:
            res = self.client().patch(
                f'/movieCategory/{first_category.id}', 
                headers=self.executive_producer_header,
                json={
                    "name": "test category name update 2",
                }
            )
            data = json.loads(res.data)

            self.assertSuccess(data, res.status_code)
            self.assertNotEmpty(data['movie_category'])
        else:
            pass
  
    # ---------------------------------- #
    ### TEST DELETE CATEGORIES REQUEST ###
    # -----------------------------------#

    # Test when using no token used
    def test_36_delete_category(self):
        res = self.client().delete('/movieCategory/1')
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using casting assistant token
    def test_37_401_delete_category_by_assistant(self):
        res = self.client().delete(
            '/movieCategory/1', 
            headers=self.casting_assistant_header
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)

    # Test when using casting director token
    def test_38_401_delete_category_by_director(self):
        res = self.client().delete(
            '/movieCategory/1', 
            headers=self.casting_assistant_header
        )
        data = json.loads(res.data)

        self.assert401request(data, res.status_code)
    
    # Test when using executive producer token and none exist actor
    def test_39_404_delete_category_by_producer(self):
        res = self.client().delete(
            '/movieCategory/1000', 
            headers=self.executive_producer_header
        )
        data = json.loads(res.data)

        self.assert404request(data, res.status_code)

    # Test when using executive producer token
    def test_40_delete_category_by_producer(self):
        first_category = MovieCategory.query.order_by(MovieCategory.id.desc()).first()
        if first_category is not None:
            res = self.client().delete(
                f'/movieCategory/{first_category.id}', 
                headers=self.executive_producer_header
            )
            data = json.loads(res.data)

            self.assertSuccess(data, res.status_code)
            self.assertNotEmpty(data['deleted_id'])
        else: 
            pass

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()