import sys
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(request, data):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    current_questions = [questions.format() for questions in data]
    current_questions = current_questions[start:end]

    return current_questions


def structure_categories(categories):
    formatted_categories = {}
    for i in categories:
        formatted_categories[i['id']] = i['type']

    return formatted_categories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.all()
            categories = [category.format() for category in categories]
            structured = structure_categories(categories=categories)

            return jsonify({'categories': structured})
        except:
            abort(422)

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
    @app.route('/questions')
    def get_questions():
        try:
            categories = [category.format()
                          for category in Category.query.order_by('id').all()]
            structured = structure_categories(categories=categories)
            questions = Question.query.order_by('id').all()
            current_questions = paginate(request, questions)

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'totalQuestions': len(questions),
                'currentCategory': 'History',
                'categories': structured,
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404, 'Question not found!')
            else:
                question.delete()
                return jsonify({
                    'success': True,
                    'id': question_id
                })
        except:
            print(sys.exc_info())
            abort(400)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        search_word = body.get('searchTerm', None)

        try:
            if search_word is not None:
                query = f'%{search_word}%'
                by_question = Question.question.ilike(query)
                result = Question.query.filter(by_question).all()
                result = [q.format() for q in result]
                return jsonify({
                    'questions': result,
                    'totalQuestions': len(result),
                    'currentCategory': 'hot',
                })
            else:
                question = body.get('question', None),
                answer = body.get('answer', None),
                category = body.get('category', None),
                difficulty = body.get('difficulty', None)

                if question is None or answer is None or category is None or difficulty is None:
                    abort(400, 'Missing required fields!')

                new_question = Question(
                    question=question, answer=answer, category=category, difficulty=difficulty)
                new_question.insert()

                return jsonify(new_question.format())
        except:
            print(sys.exc_info())
            abort(400)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        try:
            category = Category.query.filter(
                Category.id == category_id).one_or_none()

            if category is None:
                return abort(404)

            questions = Question.query.filter(
                Question.category == category_id).all()
            paginated = paginate(request, questions)

            return jsonify({
                'questions': paginated,
                'totalQuestion': len(questions),
                'currentCategory': category.type
            })
        except:
            print(sys.exc_info())
            abort(400)

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
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()

        try:
            previous_questions = body.get('previous_questions', None)
            category = body.get('quiz_category', None)

            if category != None:
                if category['id'] == 0:
                    questions = Question.query.all()
                else:
                    questions = Question.query.filter(
                        Question.category == category['id']).all()

                if questions == []:
                    abort(404)
                format_questions = [q.format() for q in questions]
                next_questions = []

                for question in format_questions:
                    if question['id'] not in previous_questions:
                        next_questions.append(question)

                if len(next_questions):
                    question = next_questions[random.randint(
                        0, len(next_questions) - 1)]
                    return jsonify({
                        'question': question,
                    })
                else:
                    return jsonify({
                        "question": None,
                    })
            else:
                abort(404)
        except:
            print(sys.exc_info())
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                "success": False,
                "error": 400,
                "message": "Bad Request",
            }
        ), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": error or "Resource Not Found",
            }
        ), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify(
            {
                "success": False,
                "error": 405,
                "message": "Method Not Allowed",
            }
        ), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "Unprocessable",
            }
        ), 422

    @app.errorhandler(500)
    def serverError(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500

    return app
