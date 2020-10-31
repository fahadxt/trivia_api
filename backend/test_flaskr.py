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
        self.database_path ="postgresql://{}:{}@{}/{}".format('postgres','root','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        
        self.new_question = {
            'question': 'new question',
            'answer': 'new answer',
            'category': 1,
            'difficulty': 1
        }

        self.search = {
            'searchTerm': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?',
        }

        self.play_quiz = {
            'quiz_category': 
            {
                'id':0
            }, 
            'previous_questions': []
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
    
    # Test endpoint for new question (store) 
    def test_question_store(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        
    # Test endpoint for search on question
    def test_question_search(self):
        res = self.client().post('/questions', json=self.search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        
    # Test categories endpoint
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))
   
    # Test questions endpoint 
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
       
    # Test questions based on category endpoint 
    def test_get_questions_based_on_category(self):
        res = self.client().get('/categories/{}/questions'.format(2))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['current_category'], '2')
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    # Test endpoint for play quizzes
    def test_play_quiz(self):
        res = self.client().post('/quizzes', json=self.play_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['question']))
        self.assertEqual(data['success'], True)

    # Test endpoint for play quizzes without data
    def test_play_quiz_without_data(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test question DELETE endpoint
    def test_delete_question(self):
        last = Question.query.order_by(Question.id.desc()).first().format()
        res = self.client().delete('/questions/{}'.format(last['id']))
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == last['id']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)
        
    # Test question DELETE with invalid id
    def test_unprocessable_delete_question(self):
        res = self.client().delete('/questions/0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()