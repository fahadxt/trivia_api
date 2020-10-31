# Trivia API Backend ❤️ 

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

### Database Setup
With `POST` gres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


### API ✨

#### `GET` `/categories` 
#### Endpoint for get all available categories
**-** **Response result** (example):
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "total_categories": 6
}
```

------

#### `GET` `/questions` 
#### Endpoint for get all available questions with pagination (every 10 questions in one page) , and all categories , and total questions in the database
**-** **Request arguments**: Accept only integer "Page Number"

**-** **Response result** (example): `/questions?page=1`
```
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
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        ...
    ],
    "success": true,
    "total_questions": 31
}
```

------

#### `DELETE` `/questions/<question_id>` 
#### Endpoint for delete a question by id.
**-** **Request arguments** : Accept only integer "Question ID"

**-** **Response result** (example): `'/questions/1'`
```
{
    "deleted": "1",
    "success": true
}
```

------

#### `POST` `/questions` 
####  Endpoint for **`create a new question`** or **`search on questions`**


**`create a new question`**

**-** **Request body**
```
{
    "question": "string", 
    "answer": "string", 
    "difficulty": Integer, 
    "category": Integer
}
```
**-** **Response result** (example) :
```
{
    "created": Integer,
    "questions": [
        {
            "answer": "String",
            "category": Integer,
            "difficulty": Integer,
            "id": Integer,
            "question": "String"
        },
        ...
    ],
    "success": true,
    "total_questions": Integer
}
```
    
**`search on questions`**
 
**-** **Request body**
```
{
    "searchTerm": "String"
}
```

**-** **Response result** (example) :
```
{
    "current_category": null,
    "questions": [
        {
            "answer": "String",
            "category": Integer,
            "difficulty": Integer,
            "id": Integer,
            "question": "String"
        }
        ...
    ],
    "success": true,
    "total_questions": Integer
}
```

------
    
#### `GET` `/categories/<category_id>/questions` 
#### Endpoint to get questions based on category.
**-** **Request arguments**: Accept only integer "Category ID"

**-** **Response result** (example):  `'/categories/1/questions'`
```
{
    "current_category": Integer,
    "questions": [
        {
            "answer": "String",
            "category": Integer,
            "difficulty": Integer,
            "id": Integer,
            "question": "String"
        },
        ...
    ],
    "success": true,
    "total_questions": Integer
}
```

------
    
#### `POST` `/quizzes` 
#### Endpoint to get only one random question based on category, and you need to push the previous questions with body into `previous_questions` array to avoid any questions in this array.

> **_NOTE:_**  You can get a one question NOT based on category, by put the **id** in **quiz_category** equal 0. 

**-** **Request body** :
```
 {
    "quiz_category": 
    {
        "id":1
    }, 
    "previous_questions": []
}
```

**-** **Response result** (example) :
```
{
    "question": {
        "answer": "String",
        "category": Integer,
        "difficulty": Integer,
        "id": Integer,
        "question": "String"
    },
    "success": true
}
```

------
    

### Testing
To run the tests, run
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
