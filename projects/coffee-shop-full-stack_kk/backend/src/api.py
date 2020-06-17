import os
from flask import Flask, request, jsonify, abort, flash
from sqlalchemy import exc
import json
from flask_cors import CORS
import jose

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# Uncomment the line below on first run
# db_drop_and_create_all()

# ROUTES
@app.route('/drinks', methods=['GET'])
# returns all drinks
def get_drinks():
    try:
        drinks_query = Drink.query.all()
        if len(drinks_query) == 0:
            abort(422)
        drinks = [drink.short() for drink in drinks_query]
        return jsonify({
            'success': True,
            'drinks': drinks})
    except Exception:
        abort(422)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
# returns drink details to barista and manager
def get_drinks_detail():
    try:
        drinks_query = Drink.query.all()
        drinks = [drink.long() for drink in drinks_query]

        return jsonify({
            'success': True,
            'drinks': drinks})
    except Exception:
        abort(422)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
# adds new drink to database (only for manager)
def post_drink():
    drink_details = request.get_json()
    if drink_details is None:
        abort(422)
    drink_title = drink_details.get('title')
    drink_recipe = drink_details.get('recipe')
    try:
        new_drink = Drink(title=drink_title, recipe=json.dumps(drink_recipe))
        new_drink.insert()
        new_drink = Drink.query.filter_by(id=new_drink.id).first()
        return jsonify({
            'success': True,
            'drinks': new_drink.long()
        })
    except AuthError:
        abort(401)
    except Exception:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
# updates exisitng drink with id = drink_id from url with new details (only for manager)
def patch_drink(drink_id):
    try:
        drink_detail = request.get_json()
        title_update = drink_detail.get('title')
        recipe_update = drink_detail.get('recipe')
        drink_to_update = Drink.query.filter(
            Drink.id == drink_id).one_or_none()
        if drink_to_update is None:
            abort(422)
        if title_update:
            drink_to_update.title = title_update
        if recipe_update:
            drink_to_update.recipe = json.dumps(recipe_update)
        drink_to_update.update()

        return jsonify({
            'success': True,
            'drinks': [drink_to_update.long()]
        })
    except Exception:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
# deletes drink with id = drink_id from url from database (only for manager)
def delete_drink(drink_id):
    try:
        drink_to_delete = Drink.query.filter(Drink.id ==
                                             drink_id).one_or_none()
        drink_to_delete.delete()
        return jsonify({
            'success': True,
            'delete': drink_id
        })

    except Exception:
        abort(422)


# Error Handling
@app.errorhandler(400)
def error_400(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(404)
def error_404(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(422)
def error_422(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422


@app.errorhandler(405)
def error_405(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not found'
    }), 405


@app.errorhandler(500)
def error_500(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500


@app.errorhandler(AuthError)
def error_auth(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": "Authorization Error"
    }), 401


@app.errorhandler(401)
def error_401(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401
