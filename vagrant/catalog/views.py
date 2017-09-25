from models import Base, User, Game, Platform
from flask import Flask, make_response, jsonify, request, url_for, abort, render_template, g, flash, redirect
from flask import session as login_session
from flask_httpauth import HTTPBasicAuth

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

import random, string, datetime

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

auth = HTTPBasicAuth()


engine = create_engine('sqlite:///catalog-app.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Game Catalog"

# GET JSON FOR ALL GAMES IN A PLATFORM'S LIBRARY 
@app.route('/platform/<int:platform_id>/library/JSON')
def platformLibraryJSON(platform_id):
    platform = session.query(Platform).filter_by(id=platform_id).one()
    games = session.query(Game).filter_by(
        platform_id=platform_id).all()
    return jsonify(GameList=[i.serialize for i in games])
    
# GET JSON FOR SINGLE GAME
@app.route('/platform/<int:platform_id>/library/<int:game_id>/JSON')
def gameJSON(game_id):
    game = session.query(Game).filter_by(id=game_id).one()
    return jsonify(Game=game.serialize)

# GET JSON OF ALL PLATFORMS IN DB
@app.route('/platform/JSON')
def platformsJSON():
    platforms = session.query(Platform).all()
    return jsonify(platforms=[i.serialize for i in platforms])

@app.route('/users/JSON')
def usersJSON():
    users = session.query(User).all()
    return jsonify(platforms=[i.serialize for i in users])

#DELETE PLATFORM

# VIEW PLATFORM LIBRARY
@app.route('/platform/<int:platform_id>/')
@app.route('/platform/<int:platform_id>/library/')
def showPlatformLibrary(platform_id):
    platform = session.query(Platform).filter_by(id=platform_id).one()
    games = session.query(Game).filter_by(
        platform_id=platform_id).all()
    #if login_session['user_id'] == platform.user_id:
    return render_template('library.html', games=games, platform=platform)
    # else:
    #     creator = session.query(User).filter_by(id=platform.user_id).one()
    #     return render_template('publiclibrary.html', games=games, platform=platform, creator=creator)



# VIEW LIST OF PLATFORMS
@app.route('/')
@app.route('/platform/')
def showPlatforms():
    platforms = session.query(Platform).all()
    return render_template('platformlist.html', platforms=platforms)

# ADD A NEW PLATFORM
@app.route('/platform/new/', methods=['GET', 'POST'])
def addPlatform():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        print 'newPlatform'
        newPlatform = Platform(
            name='New Platform', user_id=100,released=datetime.date(1990, 1, 1), manufacturer='WillowTree'
        )
        flash('Creating new platform')
        session.commit()
        return redirect(url_for('showPlatforms'))
    else:
        return render_template('addPlatform.html')

# EDIT PLATFORM
@app.route('/platform/<int:platform_id>/edit/', methods=['GET', 'POST'])
def editPlatform(platform_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedPlatform = session.query(
        Platform).filter_by(id=platform_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedPlatform.name = request.form['name']
            flash('Platform successfully edited %s' % editedPlatform.name)
            return redirect(url_for('showPlatforms'))
    else:
        return render_template('editPlatform.html', platform=editedPlatform)
    
# DELETE PLATFORM
@app.route('/platform/<int:platform_id>/delete/', methods=['GET', 'POST'])
def deletePlatform(platform_id):
    if 'username' not in login_session:
        return redirect('/login')
    platformToDelete = session.query(
        Platform).filter_by(id=platform_id).one()
    if login_session['user_id'] == platformToDelete.user_id:   
        if request.method == 'POST':
            session.delete(platformToDelete)
            flash('%s Successfully Deleted' % platformToDelete.name)
            session.commit()
            return redirect(url_for('showPlatforms', platform_id=platform_id))
        else:
            return render_template('deletePlatform.html', platform=platformToDelete)
    else:
        return redirect(url_for('showMenu', platform_id=platform_id))

#@app.route('/addgame/')
@app.route('/platform/<int:platform_id>/addgame/')
def addGame(platform_id):
    if 'username' not in login_session:
        print "username not in login sessions"
        return redirect('/login')
    platform = session.query(Platform).filter_by(id=platform_id).one()
    if login_session['user_id'] == platform.user_id:
        if request.method == 'POST':
            newGame = Game(title=request.form['title'], developer=request.form['developer'], publisher=request.form[
                            'publisher'], releasedate=request.form['releasedate'], platform_id=platform.id, user_id=platform.user_id)
            session.add(newGame)
            session.commit()
            flash('New Game - %s Successfully Created' % (newGame.name))
            return redirect(url_for('showPlatforms', platform_id=platform_id))
        else:
            return render_template('newgame.html', platform_id=platform_id)
    else:
        flash('You do not have authorization to access this page')
        return redirect(url_for('showPlatforms', platform_id=platform_id))


#/catalog/category/sub_category
#details for that subcategory
#project example:
#/catalog/Snowboarding/items
#"goggles, snowboard"
#/catalog/snowboarding/snowboard
#"Description: description of a snowboard"


#when logged in, user can CRUD on each page

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        print "result['user_id'] != gplus_id:"
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    userID = getUserID(login_session['email'])
    print userID

    #if not userID
    if userID == None:
        userID = createUser(login_session)
        print userID

    print "login_session['user_id']"
    login_session['user_id'] = userID

    

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions

def createUser(login_session):
    newUser = User(username=login_session['username'], email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    print 'getUserInfo'
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)