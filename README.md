# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game.

The application:

1. Display questions - both all questions and by category and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

The trivia app will give the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

## API Reference

### Getting Started

- Base URL: The app can be run localy and is currently not hosted as a base URL. The default backend URL is `https://localhost:5000`
- Authentication: This current version does not have any authentication or API keys

### Endpoints

## GET /categories

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

Example: `curl http://localhost:5000/categories`

**_Response_**:

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### GET /questions

- This fetches all the questions paginated in step of 10 per page
- Request Parameters: `page` of type `int`
- Returns the categories (all categories), current category, a list of paginated (in 10) questions, success status and total questions.

Example: `curl http://localhost:5000/questions?page=1`

**_Response_**:

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    ...
  ],
  "success": true,
  "totalQuestions": 19
}
```

### DELETE /questions/`{question_id}`

- Deletes the question of a given ID if it exist and returns an error if the given question_id not found
- Request Parameters: `question_id` of type `int`; ID of the specific question to delete
- Returns an object of success and `id` of the deleted question

Example: `curl -X DELETE http://localhost:5000/questions/1`

**_Response_**:

```json
{
  "success": "True",
  "id": 1
}
```

### POST /questions

- Add a new question. Requires the question, answer, the category ID and the difficulty level (0-5) to be passed into the request body
- Request Body: `question`, `answer`, `category` and `difficulty` to set for the new question.
- Returns a dict of the new question created

Example: `curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d '{"question": "what is your name?", "answer": "farouk", "category":1, "difficulty": 1}'`

**_Response_**:

```json
{
  "id": 21,
  "question": "what is your name?",
  "answer": "farouk",
  "category": 1,
  "difficulty": 1
}
```

### GET /categories/`{category_id}`/questions

- Fetches all the questions for a specific category based on the `category_id` provided
- Request Parameters: `category_id`, ID of the category to fetch the questions from
- Returns the current category, a list of paginated (in 10) questions, and total questions (for the specified category).

Example: `curl http://localhost:5000/categories/2/questions`

**_Response_**:

```json
{
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    ...
  ],
  "totalQuestions": 15,
  "currentCategory": "Art"
}
```

### GET /questions

- Search for questions by the search term query. Returns any questions for whom the search term is a substring of the question.
- Request Body: `searchTerm` with the value to lookup
- Returns the current category, a list of paginated (in 10) questions, and total questions (of the total questions found)

Example: `curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d '{"searchTerm": "title"}'`

**_Response_**:

```json
{
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    ...
  ],
  "totalQuestions": 15,
  "currentCategory": "Art"
}
```

### POST /quizzes

- Takes `quiz_category` and `previous_questions` body parameters where these are the category to lookup the quiz and the array of questions ID previously answered, respectively and returns a random question from the available questions
- Request Body: json object of `quiz_category` and `previous_questions`
- Returns the current category, a list of paginated (in 10) questions, and total questions (for the specified category).

Example: `curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category": 1, "previous_questions": [] }'`

**_Response_**:

```json
{
  "questions": {
    "answer": "Apollo 13",
    "category": 5,
    "difficulty": 4,
    "id": 2,
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  }
}
```

## Authors

- [Farouk](https://github.com/jan-far)

## Acknowledgment

To the awesome team at Udacity
