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
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
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

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_failed_get_categories(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertTrue(data['currentCategory'])
        self.assertTrue(data['categories'])

    def test_failed_get_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_delete_questions(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id'], 5)
        self.assertEqual(question, None)

    def test_failed_question_delete(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_add_new_question(self):
        new_question = {
            'question': 'What is your favourite dance?',
            'answer': 'Ballet',
            'category': 5,
            'difficulty': 5
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(type(data['question']), str)

    def test_failed_add_new_question(self):
        new_question = {
            'question': 'What is your favourite dance?',
            'answer': 'Ballet',
            'category': 5,
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_search_questions(self):
        searchTerm = {'searchTerm': 'title'}
        res = self.client().post('/questions', json=searchTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_failed_search_questions(self):
        searchTerm = {'searchTerms': 'title'}
        res = self.client().post('/questions', json=searchTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        category = Category.query.filter(Category.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['currentCategory'], category.type)
        self.assertTrue(data['totalQuestion'])
        self.assertTrue(data['questions'])

    def test_failed_questions_by_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_get_quiz_questions(self):
        res = self.client().post(
            '/quizzes', json={'quiz_category': {'id': 1}, 'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_failed_get_quiz_questions(self):
        res = self.client().post(
            '/quizzes', json={'quiz_category': {'id': 1000}, 'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
