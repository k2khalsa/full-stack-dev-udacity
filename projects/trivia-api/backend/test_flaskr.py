import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import random

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'password', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # TESTING RETRIEVING CATEGORIES SUCCESS
    def test_retrieve_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_categories'], 6)
        self.assertEqual(data['success'], True)

    # TESTING RETRIEVING QUESTIONS SUCCESS
    def test_retrieve_questions(self):
        question_count = len(Question.query.all())
        response = self.client().get('/questions/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_questions'], question_count)
        self.assertEqual(data['success'], True)

    # TESTING QUESTION POST SUCCESS
    def test_post_question(self):
        question_count_before = len(Question.query.all())
        new_question = {
            'question': 'new question 1?',
            'answer': 'new answer 1',
            'difficulty': 1,
            'category': 1
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_questions'], question_count_before+1)
        self.assertEqual(data['success'], True)

    # TESTING QUESTION DELETE SUCCESS
    def test_delete_question(self):
        question_count_before = len(Question.query.all())
        response = self.client().delete(
            '/questions/17')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_questions'], question_count_before-1)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted question'], 17)

    # TESTING QUESTION SEARCH SUCCESS
    def test_search_question(self):
        new_search = {
            'searchTerm': 'organ'
        }

        response = self.client().post('/questions/search', json=new_search)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['success'], True)

    # TESTING RETRIEVING QUESTION FOR GIVEN CATEGORY SUCCESS
    def test_retrieve_questions_w_category(self):
        random_category_id = random.randint(1, 6)
        random_category_id_questions_count = Question.query.filter(
            Question.category == random_category_id).count()
        response = self.client().get('/categories/{}/questions'.format(random_category_id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_questions'],
                         random_category_id_questions_count)
        self.assertEqual(data['success'], True)

    # TESTING QUIZ SUCCESS
    def test_quiz(self):
        new_quiz = {
            'quiz_category': {
                'id': 3,
                'type': 'Geography'
            },
            'previous_questions': []
        }
        response = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['question']['category'], 3)
        self.assertEqual(data['success'], True)

    # TESTING ERRORS
    # deleting a question that does not exist
    def test_error_404_question_delete(self):
        response = self.client().delete(
            '/questions/60000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # Submitting quiz category_id that does not exist
    def test_error_404_quiz_post(self):
        new_quiz = {
            'quiz_category': {
                'id': 10,
                'type': 'Geography'
            },
            'previous_questions': []
        }
        response = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # Submitting incorrect URL for questions
    def test_error_404_questions_get(self):
        response = self.client().get('/quests/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # Submitting incorrect URL for categories
    def test_error_404_categories_get(self):
        response = self.client().get('/categorys')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # empty search on questions
    def test_error_405_question_search_get(self):
        new_search = {}

        response = self.client().post('/questions/search', json=new_search)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)

    # question missing from question submission
    def test_error_422_question_post(self):
        new_question = {
            'answer': 'new answer 2',
            'difficulty': 1,
            'category': 1
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    # requesting questions from non existing category
    def test_error_422_retrieve_questions_w_category(self):
        response = self.client().get('/categories/5000/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

        # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
