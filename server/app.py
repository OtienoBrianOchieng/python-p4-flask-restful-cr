#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)



class Index(Resource):
    def get(self):
        responce_dict = {
            'index' : 'Welcome to the Newsletter RESTFUL API',
        }
        response = make_response(
            jsonify(responce_dict),
            200,
        )
        return response

api.add_resource(Newsletter, '/')

class Newsletters(Resource):
    #get 
    def get_all(self):
        news_letter_list = [letter.to_dict() for letter in Newsletter.query.all()]

        response = make_response(
            jsonify(news_letter_list),
            200,
        )
        return response
    #post
    def post(self):
        new_newsletter = Newsletter(
            title = request.form['title'],
            body = request.form ['body'],
        )

        db.session.add(new_newsletter)
        db.session.commit()

        new_newsletter_dict = new_newsletter.to_dict()
        response = make_response(
            jsonify(new_newsletter_dict),
            201,
        )
        return response
class NewsletterByID(Resource):
    def get_by_id(self, id):
        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response
    
api.add_resource(Newsletters, '/newsletters')
api.add_resource(Newsletters, '/newsletters/<int:id>')



    



if __name__ == '__main__':
    app.run(port=5555, debug=True)
