# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. ~~Use Flask-CORS to enable cross-domain requests and set response headers.~~
2. ~~Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.~~ 
3. ~~Create an endpoint to handle GET requests for all available categories.~~ 
4. ~~Create an endpoint to DELETE question using a question ID.~~ 
5. ~~Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.~~ 
6. ~~Create a POST endpoint to get questions based on category.~~ 
7. ~~Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.~~ 
8. ~~Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.~~ 
9. ~~Create error handlers for all expected errors including 400, 404, 422 and 500.~~ 

## End Points
GET '/categories'
```
- Fetches a dictionary of categories
- Request Arguments: None
- Sample curl: curl http://127.0.0.1:5000/categories
- Returns: 
{
    {'1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"},
    "success": true
}
```

GET '/questions'
```
- Fetches a dictionary of questions along with number of total questions
- Results are paginated in groups of 10.
- Request Arguments: None
- Sample curl: curl http://127.0.0.1:5000/questions
- Returns: 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 22
}
```
DELETE '/questions/<int:question_id>'
```
- Deletes question with id (question_id) from questions list and returns remaining questions
- Request Arguments: None
- Sample curl: curl http://127.0.0.1:5000/questions/6 -X DELETE
- Returns: 
{
    "success": True,
    "questions": [
    ],
    "deleted question": 6,
    'total_questions': 21
}
```
POST '/questions'
```
- Adds a new question based on request arguments and returns full list of questions
- Request Arguments: 
{
	"question": "Sample Question",
	"answer": "Sample Answer",
	"category": 3,
	"difficulty": 3
}
- Sample curl: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Sample Question", "answer": "Sample Answer", "difficulty": 3, "category": "3" }'

- Returns: 
{
    "created": 37,
    "questions": [
    ],
    "success": true,
    "total_questions": 23
}
```
POST '/questions/search'
```
- Searches for questions that match search term in request
- Request Arguments: 
{
	"searchTerm": "organ"
}
- Sample curl: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "organ"}'
- Returns: 
{
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```
GET '/categories/<int:categories_id>/questions'
```
- Gets all questions under specificed by category id 
- Request Arguments: None
- Sample curl: curl http://127.0.0.1:5000/categories/2/questions
- Returns: 
{
    "questions": [
    ],
    "success": true,
    "total_questions": 5
}
```
POST '/quizzes'
```
- Uses request parameters of category and previous questions to return a random question
- Request Arguments: 
{
	"quiz_category": {
		"id": "2",
		"type":"Art"
	},
	"pervious_question": [12]
}
- Sample curl: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5, 6], "quiz_category": {"type": "Art", "id": "2"}}'
- Returns: 
{
  "question": {
    "answer": "Jackson Pollock", 
    "category": 2, 
    "difficulty": 2, 
    "id": 19, 
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  }, 
  "success": true, 
  "total_questions": 5
}
```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```