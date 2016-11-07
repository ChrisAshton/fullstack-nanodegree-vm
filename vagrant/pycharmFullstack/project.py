from flask import Flask, render_template, url_for, request, redirect, flash

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)

    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/newitem', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created: %s" % newItem.name)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id, restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit_menu_item', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id= menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            menu_item.name = request.form['name']
        if request.form["description"]:
            menu_item.description = request.form["description"]
        if request.form["price"]:
            menu_item.price = request.form["price"]
        session.add(menu_item)
        session.commit()
        flash("%s edited" % menu_item.name)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, menu_item=menu_item, restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete_menu_item', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id= int(menu_id)).one()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(menu_item)
        session.commit()
        flash("% has been deleted" % menu_item.name)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=menu_item, restaurant=restaurant)


if __name__ == '__main__':
    app.secret_key = 'SUPER_SECRET_KEY'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
