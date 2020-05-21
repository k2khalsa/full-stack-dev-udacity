import sys
from flask import Flask, render_template, request, redirect, jsonify, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#app setup, db setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={"expire_on_commit": False})

#migrate setup
migrate = Migrate(app, db)

#Todo list table setup
class TodoList (db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    #setup child table relation
    todos = db.relationship('Todo', backref='list',lazy=True, cascade='all, delete-orphan')


#Todo items table setup
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    #setup parent table relation
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)
    def __repr__(self):
      return f'<Todo {self.id} {self.description}>'

#db.create_all() removed due to the addtion of migration 

#route to show general page
@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html', 
    lists = TodoList.query.order_by('id').all(),
    active_list = TodoList.query.get(list_id),
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all())

#route to create new todo item
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
      description = request.get_json()['description']
      list_id = request.get_json()['list_id']
      todo = Todo(description=description)
      active_list = TodoList.query.get(list_id)
      todo.list = active_list
      db.session.add(todo)
      db.session.commit()
      body['description'] = todo.description
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info)
    finally:
      db.session.close()
    if error:
      abort(400)
    else:
      return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
#pulls todo_id from url
def set_compelted_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

#current results in an error on the HTML side but still deletes record from DB
@app.route('/todos/<todo_id>', methods=['DELETE'])
#pulls todo_id from url
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id = todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True})