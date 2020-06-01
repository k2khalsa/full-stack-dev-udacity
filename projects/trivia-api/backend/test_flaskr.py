import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

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

    # TESTING RETRIEVING CATEGORIES
    def test_retrieve_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['success'], True)

    # TESTING RETRIEVING QUESTIONS
    def test_retrieve_questions(self):
        response = self.client().get('/questions/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['total_question']), 19)
        self.assertEqual(data['success'], True)

    # TESTING QUESTION POST
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
        self.assertEqual(len(data['total_question']), question_count_before+1)
        self.assertEqual(data['success'], True)

    # TESTING QUESTION DELETE
    def test_delete_question(self):
        question_count_before = len(Question.query.all())
        question_to_delete = Question.query.one()
        response = self.client.delete(
            '/questions/{}'.format(question_to_delete.id))
        data = json.loads(reponse.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['total_question']), question_count_before-1)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted question'], question_to_delete.id)

    # TESTING QUESTION SEARCH
    def test_search_question(self):
        new_search = {
            'searchTerm': 'organ'
        }

        response = self.client().post('/questions/search', json=new_search)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['total_question']), 1)
        self.assertEqual(data['success'], True)

    # TESTING QUIZ
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
        self.assertEqual(data['questions']['category'], 3)
        self.assertEqual(data['success'], True)

    # TESTING ERRORS
    # Submitting quiz category_id that does not exist
    def test_error_404(self):
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

    # empty search on questions
    def test_error_405(self):
        new_search = {}

        response = self.client().post('/questions/search', json=new_search)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)

    # question missing from question submission
    def test_error_422(self):
        new_question = {
            'answer': 'new answer 2',
            'difficulty': 1,
            'category': 1
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)


        # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
