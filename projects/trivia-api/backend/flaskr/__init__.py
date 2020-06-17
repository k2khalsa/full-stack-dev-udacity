import os
import sys
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

# used for pagination function
QUESTIONS_PER_PAGE = 10


def random_question(archived_questions):
    # returns new random question from list of all questions
    all_questions_query = Question.query.all()
    all_question_query_count = Question.query.count()

    if len(archived_questions) == all_question_query_count:
        return None

    while True:
        random_question = all_questions_query[random.randrange(
            0, all_question_query_count, 1)]

        if random_question.id in archived_questions:
            continue
        else:
            return random_question.format()


def random_question_w_category(category, archived_questions):
    # returns new random question from list of all questions based on category given
    questions_category = Question.query.filter_by(category=category).all()
    if len(questions_category) == 0:
        abort(404)
    max_count = len(questions_category)

    if len(archived_questions) == max_count:
        return None

    while True:
        random_question = questions_category[random.randrange(
            0, len(questions_category), 1)]

        if random_question.id in archived_questions:
            continue
        else:
            return random_question.format()


def paginate_questions(request, selection):
    # returns formation questions for each page
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    # returns all categories
    def retrieve_categories():

        categories_query = Category.query.all()
        categories_query_count = len(categories_query)

        if categories_query_count == 0:
            abort(404)

        categories = {}
        for category in categories_query:
            categories[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': categories,
            'total_categories': categories_query_count
        })

    @app.route('/questions/', methods=['GET'])
    # returns all questions
    def retrieve_questions():

        categories_query = Category.query.all()
        questions_query = Question.query.all()
        question_query_count = len(questions_query)
        questions = paginate_questions(request, questions_query)

        if len(questions) == 0:
            abort(404)

        categories = {}
        for category in categories_query:
            categories[category.id] = category.type

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': question_query_count,
            'categories': categories,
            'current_category': None})

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    # deletes question based on question_id
    def delete_questions(question_id):
        question_query = Question.query.get(question_id)
        if question_query is None:
            abort(404)

        try:
            question_query.delete()

            questions_remaining = Question.query.all()
            questions = paginate_questions(request, questions_remaining)

            return jsonify({
                'success': True,
                'questions': questions,
                'deleted question': question_query.id,
                'total_questions': len(questions_remaining)
            })

        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    # adds new question
    def create_questions():
        body = request.get_json()
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')

        if new_question is None or new_answer is None or new_category is None:
            abort(422)

        try:
            new_question = Question(question=new_question, answer=new_answer,
                                    category=new_category, difficulty=new_difficulty)
            new_question.insert()
            questions_query = Question.query.all()
            questions = paginate_questions(request, questions_query)

            return jsonify({
                'success': True,
                'questions': questions,
                'created': new_question.id,
                'total_questions': len(questions_query)
            })
        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    # returns questons matching search term
    def search_questions():
        try:
            search_text = (request.get_json()).get('searchTerm')
            questions_query = Question.query.filter(
                Question.question.ilike('%' + search_text + '%'))

            query_count = Question.query.filter(
                Question.question.ilike('%' + search_text + '%')).count()

            if query_count == 0:
                abort(405)

            questions = paginate_questions(request, questions_query)

            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': query_count
            })

        except:
            abort(405)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_with_category(category_id):
        # returns all questions for given category
        try:
            questions_query = Question.query.filter(
                Question.category == category_id).all()
            if len(questions_query) == 0:
                abort(422)
            questions = paginate_questions(request, questions_query)

            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(questions_query)
            })
        except:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    # returns random questions to play quiz game
    def generate_question():
        body = request.get_json()
        category = body.get('quiz_category')
        archived_questions = body.get('previous_questions')

        try:
            if int(category['id']) > 0:
                question = random_question_w_category(
                    category['id'], archived_questions)

            else:
                question = random_question(archived_questions)

            return jsonify({
                'success': True,
                'question': question
            })

        except:
            abort(404)

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not found'
        }), 405

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
