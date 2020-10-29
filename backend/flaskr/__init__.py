import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

#Pagination function
QUESTIONS_PER_PAGE = 10
def paginate(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):

  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  # endpoint for all available categories
  @app.route('/categories')
  def categories_index():
    categories = Category.query.order_by(Category.id).all()
    categories = {category.id: category.type for category in categories}

    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories,
      'total_categories': len(categories)
    })

  # endpoint for questions with pagination (every 10 questions)
  @app.route('/questions')
  def questions_index():
    selection = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()
    current_questions = paginate(request, selection)
    categories = {category.id: category.type for category in categories}
    
    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': categories,
      'current_category': None
    })

  # endpoint for DELETE a question by id (destroy) 
  @app.route("/questions/<question_id>", methods=['DELETE'])
  def question_destroy(question_id):
    try:
      data = Question.query.get(question_id)
      data.delete()

      return jsonify({
          'success': True,
          'deleted': question_id
      })
    except:
      abort(422)

  # endpoint for new question (store) OR search on question
  @app.route('/questions', methods=['POST'])
  def question_store_or_search():
    body = request.get_json()

    question = body.get('question', None)
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)
    search = body.get('searchTerm', None)


    if search:
      data = Question.query.filter( Question.question.ilike(f'%{search}%') ).all()
      questions = []
      for d in data:
        questions.append({
          "id": d.id,
          "question": d.question,
          "answer": d.answer,
          "category": d.category,
          "difficulty": d.difficulty
        })
      return jsonify({
          'success': True,
          'questions': questions,
          'total_questions': len(data),
          'current_category': None
      })

    else: 
      try:
        data = Question(
          question= question, 
          answer= answer, 
          category= category,
          difficulty= difficulty
        )
        data.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate(request, selection)

        return jsonify({
          'success': True,
          'created': data.id,
          'questions': current_questions,
          'total_questions': len(Question.query.all())
        })
        
      except:
            abort(422)

  # endpoint to get questions based on category
  @app.route("/categories/<category_id>/questions", methods=['GET'])
  def questions_based_on_category(category_id):
    try:

      data = Question.query.filter( Question.category == category_id ).all()

      questions = []
      for d in data:
        questions.append({
          "id": d.id,
          "question": d.question,
          "answer": d.answer,
          "category": d.category,
          "difficulty": d.difficulty
        })

      return jsonify({
          'success': True,
          'questions': questions,
          'total_questions': len(data),
          'current_category': category_id
      })

    except:
      abort(404)


  # endpoint for play quizzes
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():

    try:
      data = request.get_json()
      quiz_category = data.get('quiz_category')
      previous_questions = data.get('previous_questions')

      # Choose Category "ALL" -> Get a random questions from all categories
      if quiz_category['id'] == 0:
        questions = Question.query.filter(Question.id.notin_(previous_questions)).all()

      # Choose a specific category -> Get a random questions from this category
      else:
        questions = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()

      questions_data = []
      for question in questions:
        questions_data.append({
          "id": question.id,
          "question": question.question,
          "answer": question.answer,
          "category": question.category,
          "difficulty": question.difficulty
        })
      # print(questions_data)

      # question
      if len(questions_data) > 0:
        question = random.choice(questions_data)
      else:
        question = None

      return jsonify({
          'success': True,
          'question': question
      })
    except:
          abort(422)


  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422

  
  return app

    