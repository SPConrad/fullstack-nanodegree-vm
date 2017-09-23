from models import Base, User
from flask import Flask, make_response, jsonify, request, url_for, abort, render_template, g, flash, redirect
from flask import session as login_session

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests



engine = create_engine('sqlite:///catalog-app.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Game Catalog"



#MAIN CATALOG VIEW

#/catalog/category/sub_category
#details for that subcategory
#project example:
#/catalog/Snowboarding/items
#"goggles, snowboard"
#/catalog/snowboarding/snowboard
#"Description: description of a snowboard"


#when logged in, user can CRUD on each page

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
    for x in xrange(32))
    return render_template('login.html', STATE=state)


@auth.verify_password
def verify_password(username_or_token, password):
    #Check to see if is token
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id = user_id).one()
    else:
        user = session.query(User).filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

@app.route('/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        print "missing arguments"
        abort(400)

    if session.query(User).filter_by(username = username).first() is not None:
        print "Existing user"
        user = session.query(User).filter_by(username=username).first()
        return jsonify({'message': 'user already exists'}), 200

    user = User(username = username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({'username': user.username}), 201

@app.route('/api/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)