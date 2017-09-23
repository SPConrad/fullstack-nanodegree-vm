from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#make an API get request
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)

@app.route('/')
@app.route('/hello')
#can add variables to path like so:
# @app.route('path/<type: variable_name>/path")
# type can be int, string, etc
@app.route('/restaurants/<int:restaurant_id>/')
# leave the trailing slash, flask will render the page even if it isn't included in the url 
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    output = ''
    # for item in items:
    #     output += "<h3>%s</h3>" % item.name
    #     output += item.price
    #     output += "</br>"
    #     output += item.description
    #     output += "</br>"
    #     output += "</br>"
    #     output += "</br>"
    return render_template('menu.html', restaurant = restaurant, items = items)
    


# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['price']:
            newMenuItem = MenuItem(
                name=request.form['name'], 
                description=request.form['description'], 
                price=request.form['price'], 
                course=request.form['course'], 
                restaurant=restaurant_id)
            session.commit()
            flash("New menu item created!")
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
            

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            editedItem.description = request.form['description']
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash("Menu item edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        item = session.query(MenuItem).filter_by(id = menu_id)
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    flash
    session.delete(itemToDelete)
    session.commit()
    flash("Menu item deleted!")
    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)