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
        self.database_user = 'buokem'
        self.database_password = 'buokem'
        self.database_host = 'localhost:5432'
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.database_user, self.database_password, self.database_host, self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Get categories
    def test_get_categories(self):
        """Test _____________ """
        res = self.client().get('/api/categories')

        self.assertEqual(res.status_code, 200)

    def test_get_categories(self):
        """Test _____________ """
        res = self.client().get('/api/categories')

        self.assertEqual(res.status_code, 405)

    def test_get_categories(self):
        """Test _____________ """
        res = self.client().get('/api/categories')

        self.assertEqual(res.status_code, 400)

    # Get questions
    def test_get_questions(self):
        """Test _____________ """
        res = self.client().get('/api/questions')

        self.assertEqual(res.status_code, 200)

    def test_get_questions(self):
        """Test _____________ """
        res = self.client().get('/api/questions')

        self.assertEqual(res.status_code, 405)

    def test_get_questions(self):
        """Test _____________ """
        res = self.client().get('/api/questions')

        self.assertEqual(res.status_code, 400)
    
    # Delete question
    def test_delete_question(self):
        """Test _____________ """
        res = self.client().delete('/api/questions/${id}')

        self.assertEqual(res.status_code, 200)

    def test_delete_question(self):
        """Test _____________ """
        res = self.client().delete('/api/questions/${id}')

        self.assertEqual(res.status_code, 405)

    # Add question
    def test_add_question(self):
        """Test _____________ """
        res = self.client().post('/api/questions')

        self.assertEqual(res.status_code, 200)

    def test_add_question(self):
        """Test _____________ """
        res = self.client().post('/api/questions')

        self.assertEqual(res.status_code, 400)

    def test_add_question(self):
        """Test _____________ """
        res = self.client().post('/api/questions')

        self.assertEqual(res.status_code, 405)
    
    # Search question
    def test_search_questions(self):
        """Test _____________ """
        res = self.client().post('/api/questions')

        self.assertEqual(res.status_code, 200)

    def test_search_questions(self):
        """Test _____________ """
        res = self.client().post('/api/questions')

        self.assertEqual(res.status_code, 400)

    def test_search_questions(self):
        """Test _____________ """
        res = self.client().post('/api/questions')

        self.assertEqual(res.status_code, 405)    

    # Get questions by category
    def test_get_questions_category(self):
        """Test _____________ """
        res = self.client().get('/api/categories/${id}/questions')

        self.assertEqual(res.status_code, 200)

    def test_get_questions_category(self):
        """Test _____________ """
        res = self.client().get('/api/categories/${id}/questions')

        self.assertEqual(res.status_code, 400)

    def test_get_questions_category(self):
        """Test _____________ """
        res = self.client().get('/api/categories/${id}/questions')

        self.assertEqual(res.status_code, 405)

    # Post quizzes
    def test_post_quizzes(self):
        """Test _____________ """
        res = self.client().post('/api/quizzes')

        self.assertEqual(res.status_code, 200)

    def test_post_quizzes(self):
        """Test _____________ """
        res = self.client().post('/api/quizzes')

        self.assertEqual(res.status_code, 400)

    def test_post_quizzes(self):
        """Test _____________ """
        res = self.client().post('/api/quizzes')

        self.assertEqual(res.status_code, 405)

    



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()