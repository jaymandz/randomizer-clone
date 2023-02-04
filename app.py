import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv(os.path.dirname(__file__)+'/.env')

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')

db = SQLAlchemy(application)
migrate = Migrate(application, db)

@application.get('/')
def index():
    return render_template('index.html')
