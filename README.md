# cobalt
## Smarterer Coding Challenge

### Setup

1. Install sqlite3 if necessary
2. Clone repository, `git clone https://github.com/jwnaylor/cobalt.git`.  cd into /cobalt.
3. Setup a virtual env, activate it, and use pip to install requirements from requirements.txt.
4. Add cobalt/cobalt directory to PYTHONPATH
5. Create new sqlite db: `python cobalt/create_db.py`
6. Start api server: `python cobalt/app.py`


### Load initial data.

`python cobalt/loader.py smarterer_code_challenge_question_dump.csv`


### API ###

# Returns data for a single question chosen at random
`curl http://localhost:5000/question`

# Return data for the question with specified id
`curl http://localhost:5000/question/999`

# Delete question with id 999 and return status code 204 
`curl http://localhost:5000/question/999 -X DELETE`

# Update question with id 1000 and return status code 201
`curl http://localhost:5000/question/1000 -d "answer=342" -X PUT`

# Add a new questio
`curl http://localhost:5000/questions -d "question=What is 1+%2B+1?&answer=2&distractor=3&distractor=4" -X POST`

# List all questions
`curl http://localhost:5000/questions`

# List all questions (order by answer, or question, or id)
`curl http://localhost:5000/questions?orderby=answer`

# List all questions (order by answer descending)
`curl http://localhost:5000/questions?orderby=answer\&orderbydesc=yes`

# List all questions (filter for answers less than a number)
`curl http://localhost:5000/questions?answer-lt=1000`

# List all questions (filter for answers greater than a number)
`curl http://localhost:5000/questions?answer-gt=1000`

# List all questions (filter for answers equal to a number)
`curl http://localhost:5000/questions?answer-eq=1000`

# List a page full of questions and vary pagesize
`curl http://localhost:5000/questions?pagesize=5\&page=4`







