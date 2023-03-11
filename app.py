import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv(os.path.dirname(__file__)+'/.env')

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')

db = SQLAlchemy(application)
migrate = Migrate(application, db)

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

class ListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))
    body = db.Column(db.String())

@application.get('/')
def index():
    return render_template('index.html')

@application.get('/_get_all_lists')
def get_all_lists():
    return jsonify(db.session.execute(db.select(List)).all())