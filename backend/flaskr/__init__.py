import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import *

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/categories', methods=['GET'])
    def categories():

        categories = Category.query.all()

        dict_categories = {category.id:str(category.type) for category in categories}
        return jsonify({
            'categories': dict_categories
            })


    @app.route('/api/categories', methods=['POST'])
    def add_categories():

        data = request.get_json()

        type = data['type']

        new_category = Category(type=type)

        db.session.add(new_category)
        db.session.commit()
        db.session.close()

        return jsonify({
            'success': True
        })

    @app.route('/api/categories/<int:category_id>', methods=['DELETE'])
    def delete_categories(category_id):

        category = Category.query.filter_by(id=category_id).first()

        db.session.delete(category)
        db.session.commit()
        db.session.close()

        return jsonify({
            'success': True,
            'question_id': category_id
            })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/questions', methods=['GET'])
    def get_questions():

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        questions = Question.query.order_by('id').all()
        categories = Category.query.all()

        category_id = 0

        formatted_questions = [question.format() for question in questions]
        dict_categories = {category.id:str(category.type) for category in categories}
        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'categories': dict_categories,
            'currentCategory': 'All'
            })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.filter_by(id=question_id).first()

        db.session.delete(question)
        db.session.commit()
        db.session.close()

        return jsonify({
            'success': True,
            'question_id': question_id
            })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/api/questions', methods=['POST'])
    def add_question_or_search():

        if 'question' in request.get_json():

            data = request.get_json()

            question = data['question']
            answer = data['answer']
            difficulty = data['difficulty']
            category = data['category']

            new_question = Question(question=question, answer=answer, difficulty=difficulty, category=category)

            db.session.add(new_question)
            db.session.commit()
            db.session.close()

            results = Question.query.filter_by(question=question).all()

            formatted_result = [result.format() for result in results]

            return jsonify({'question': formatted_result, 'success': True})
        else:

            """
            @TODO:
            Create a POST endpoint to get questions based on a search term.
            It should return any questions for whom the search term
            is a substring of the question.

            TEST: Search by any phrase. The questions list will update to include
            only question that include that string within their question.
            Try using the word "title" to start.
            """

            data = request.get_json()
            search_term = data['searchTerm']
            
            questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()

            formatted_questions = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions)
                })

        

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/api/categories/<category_id>/questions')
    def get_category_questions(category_id):

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        questions = Question.query.filter_by(category=str(category_id)).order_by('id').all()
        category = Category.query.filter_by(id=category_id).first()

        formatted_questions = [question.format() for question in questions]
        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'currentCategory': category.type
            })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/api/quizzes', methods=['POST'])
    def quiz():

        data = request.get_json()

        previous_questions = data['previous_questions']
        quiz_category = data['quiz_category']

        questions = Question.query.filter_by(category=str(quiz_category['id'])).order_by('id').all()

        formatted_questions = [question.format() for question in questions]

        n = random.randint(0, len(formatted_questions) - 1)

        while formatted_questions[n]['id'] in previous_questions:
            n = random.randint(0, len(formatted_questions) - 1)
        
        question = formatted_questions[n]


        return jsonify({
            'question': question
            })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(500)
    def server_error():
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(405)
    def not_allowed():
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(400)
    def bad_request():
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found():
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404


    @app.errorhandler(422)
    def cant_process():
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unable to process request"
        }), 422

    return app

