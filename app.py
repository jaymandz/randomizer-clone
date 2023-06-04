import json, os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
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

def __dict_from_list_result(r):
    items = db.session.execute(
        db.select(ListItem).filter_by(list_id=r.id)
    ).scalars()
    return {
        'id': r.id,
        'name': r.name,
        'items': [ { 'id': i.id, 'body': i.body } for i in items ],
    }

@application.get('/')
def index():
    return render_template('index.html')

@application.get('/_get_all_lists')
def get_all_lists():
    result = db.session.execute(db.select(List)).scalars()
    return jsonify([ __dict_from_list_result(r) for r in result ])

@application.get('/_get_list')
def get_list():
    result = db.session.execute(
        db.select(List).filter_by(id=request.args.get('id'))
    ).scalar_one()
    return jsonify(__dict_from_list_result(result))

@application.post('/_add_list')
def add_list():
    nl = List()
    nl.name = request.json['name']
    db.session.add(nl)

    db.session.flush()
    db.session.refresh(nl)

    for i in request.json['items']:
        item = ListItem()
        item.list_id = nl.id
        item.body = i['body']
        db.session.add(item)
    
    db.session.commit()
    return 'ok'

@application.post('/_delete_list')
def delete_list():
    l = db.get_or_404(List, request.json['id'])
    db.session.delete(l)
    db.session.commit()
    return 'ok'

@application.post('/_edit_list_item')
def edit_list_item():
    item = db.get_or_404(ListItem, request.json['id'])
    item.body = request.json['data']['body']
    db.session.commit()
    return 'ok'

@application.post('/_edit_list_name')
def edit_list_name():
    l = db.get_or_404(List, request.json['id'])
    l.name = request.json['data']['name']
    db.session.commit()
    return 'ok'

@application.post('/_add_list_item')
def add_list_item():
    l = db.get_or_404(List, request.json['list_id'])

    item = ListItem()
    item.list_id = l.id
    item.body = request.json['body']
    db.session.add(item)

    db.session.commit()
    return { 'insert_id': item.id }

@application.post('/_delete_list_item')
def delete_list_item():
    item = db.get_or_404(ListItem, request.json['id'])
    db.session.delete(item)
    db.session.commit()
    return 'ok'

@application.get('/_get_all_elements')
def get_all_elements():
    # Practice good etiquette. Close all files you open.
    file = open('elements.json', 'r')
    elements = json.load(file)
    file.close()
    # Now send the contents to the client.
    return jsonify(elements)

@application.get('/_get_all_countries')
def get_all_countries():
    # Practice good etiquette. Close all files you open.
    file = open('countries.json', 'r')
    countries = json.load(file)
    file.close()
    # Now send the contents to the client.
    return jsonify(countries)