from flask import Flask
from flask_sqlalchemy import SQLAlchemy

HelloApp = Flask(__name__)
HelloApp.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/postgres' #connect db to application with config variable
HelloApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(HelloApp) #links an instance of a db that we can interact with

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'
db.create_all()

@HelloApp.route('/')
def index():
    person = Person.query.first()
    return 'Hello World ' + person.name

''' USE THIS IF FLASK RUN DOESNT WORK
if __name__ == '__main__':
    HelloApp.run()
'''