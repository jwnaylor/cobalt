import constants
import datetime
from random import randint
from flask import Flask
from flask.ext import restful  # @UnresolvedImport
from flask.ext.restful import abort, reqparse, fields, marshal_with # @UnresolvedImport
from flask.ext.sqlalchemy import SQLAlchemy #@UnresolvedImport
from sqlalchemy.sql.functions import func


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=constants.SQLITE_DB_FILE
db = SQLAlchemy(app)
api=restful.Api(app)


def question_exists(question_id):
    qu=Question.query.filter(Question.id == question_id).exists()
    return db.session.query(qu).scalar()

def ensure_question_exists(question_id):
    if not question_exists(question_id):
        abort(404, message="Question with id {} does not exist".format(question_id));


class QuestionRequestParser:
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument('question', location='form')
        self.parser.add_argument('answer', location='form')
        self.parser.add_argument('distractor', action='append', dest='distractors', default=[], location='form')
        self.parser.add_argument('page', type=int, location='args')
        self.parser.add_argument('pagesize', type=int, location='args')
        self.parser.add_argument('orderby', location='args', choices=('id', 'question', 'answer'))
        self.parser.add_argument('orderbydesc', location='args', type=bool, default=False)
        self.parser.add_argument('answer-lt', location='args', type=int)
        self.parser.add_argument('answer-eq', location='args', type=int)
        self.parser.add_argument('answer-gt', location='args', type=int)
        
    def parse_args(self):
        return self.parser.parse_args()
    
parser = QuestionRequestParser()


class CSVField(fields.Raw):
    def format(self, value):
        return value.split(',')
    
question_fields = {'id': fields.String,
                   'question': fields.String,
                   'answer': fields.String,
                   'distractors': CSVField
                   }
        

class HealthCheckResource(restful.Resource):
    def get(self):
        return {'timestamp': str(datetime.datetime.now())}
    
api.add_resource(HealthCheckResource, '/healthcheck')


class QuestionResource(restful.Resource):
    @marshal_with(question_fields)
    def get(self, question_id):
        ensure_question_exists(question_id)
        return Question.query.get(question_id)
        # return {'id': q.id, 'question': q.question, 'answer': q.answer, 'distractors': q.distractors.split(',')}, 200
    
    def delete(self, question_id):
        ensure_question_exists(question_id)
        q = Question.query.get(question_id)
        db.session.delete(q)
        db.session.commit()
        return '', 204
    
    def put(self, question_id):
        ensure_question_exists(question_id)
        q = Question.query.get(question_id)
        params=parser.parse_args()
        if params['question']: q.question=params.get('question') 
        if params['answer']: q.anwser=params.get('answer')
        if params['distractors']: q.distractors=','.join(params.get('distractors'))
        db.session.commit()
        return '', 201
    
api.add_resource(QuestionResource, '/question/<int:question_id>', endpoint='question_endpoint')


class QuestionRandomResource(restful.Resource):
    @marshal_with(question_fields)
    def get(self):
        max_id=self._maxid()[0]
        question_id=None
        max_tries=10
        tries=0
        while(tries < max_tries):
            question_id=randint(1, max_id)
            if question_exists(question_id):
                break
            tries+=1
            
        return Question.query.get(question_id)
            
    def _maxid(self):
        return db.session.query(func.max(Question.id)).first()
    
api.add_resource(QuestionRandomResource, '/question/random', endpoint='question_random_endpoint')    

    
class QuestionsResource(restful.Resource):
    @marshal_with(question_fields)
    def get(self):
        items=None
        params=parser.parse_args()
        print "Params: ", params
        
        qu=Question.query
        
        orderby_criterion=None
        if params['orderby'] == 'id': orderby_criterion=Question.id
        elif params['orderby'] == 'question': orderby_criterion=Question.id
        else: orderby_criterion=Question.answer
        if params['orderbydesc']: orderby_criterion = orderby_criterion.desc()
        qu=qu.order_by(orderby_criterion)
        
        if params['answer-lt']: 
            qu=qu.filter(Question.answer < params['answer-lt'])
        if params['answer-eq']: 
            qu=qu.filter(Question.answer == params['answer-eq'])
        if params['answer-gt']: 
            qu=qu.filter(Question.answer > params['answer-gt'])

        if params.get('page', None):
            items=qu.paginate(page=params['page'], per_page=params['pagesize']).items
        else:
            items=qu.all()
        return items, 200
    
    def post(self):
        params=parser.parse_args()
        q = Question()
        if 'question' in params: q.question=params.get('question') 
        if 'answer' in params: q.answer=params.get('answer')
        if 'distractors' in params: q.distractors=','.join(params.get('distractors'))
        db.session.add(q)
        db.session.commit()
        return q.id, 201

api.add_resource(QuestionsResource, '/questions', endpoint='questions_endpoint')


class Question(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    question=db.Column(db.String(256), nullable=False)
    answer=db.Column(db.String(64), nullable=False)
    distractors=db.Column(db.String(256), nullable=False)
    

if __name__ == '__main__':
    app.run(debug=True)
