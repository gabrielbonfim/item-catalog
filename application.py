from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash
from flask import session as login_session
import random
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import os
from werkzeug.utils import secure_filename
from pprint import pprint

# Definition of the upload folder and the allowed extension in the item photo
# upload
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# Set the upload folder in the flask configuration app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# OAuth 2.0 parameters with the client_id
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Database connection and access session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Main page of the application where the categories and the last 10 items
# added are shown
@app.route('/')
def mainPage():
    # Defines 'username' and 'picture' to be passed to the templates, where
    # will be parsed to show the user info accordingly
    if 'username' in login_session:
        username = login_session['username']
        picture = login_session['picture']
    else:
        username = ''
        picture = ''
    # Categories to be passed to the template
    categories = session.query(Category)
    # Last 10 items inserted in the databse to be passed to the template
    items = session.query(Item).order_by(Item.id.desc()).limit(10)
    return (render_template('latest_items.html', categories=categories,
            items=items, username=username, picture=picture))


# Page that lists the items of the selected category
@app.route('/category/<int:category_id>')
def categoryListItems(category_id):
    # Defines 'username' and 'picture' to be passed to the templates, where
    # will be parsed to show the user info accordingly
    if 'username' in login_session:
        username = login_session['username']
        picture = login_session['picture']
    else:
        username = ''
        picture = ''
    # Categories to be passed to the template
    categories = session.query(Category)
    # Items of the selected category to be passed to the template
    items = session.query(Item).filter_by(category_id=category_id)
    category = session.query(Category).filter_by(id=category_id).one().name
    return (render_template('category_items.html', category=category,
            categories=categories, items=items, username=username,
            picture=picture))


# Page of the details of the selected item
@app.route('/item/<int:item_id>')
def getItem(item_id):
    # Defines 'username' and 'picture' to be passed to the templates, where
    # will be parsed to show the user info accordingly
    if 'username' in login_session:
        username = login_session['username']
        picture = login_session['picture']
    else:
        username = ''
        picture = ''
    # Categories to be passed to the template
    categories = session.query(Category)
    # Selected item to be passed to the template
    item = session.query(Item).filter_by(id=item_id).one()
    # Category name of the selected item to be passed to the template
    category = session.query(Category).filter_by(
        id=item.category_id).one().name
    return (render_template('item_detail.html', item=item,
            categories=categories, category=category, username=username,
            picture=picture))


# Page for the creation of a new category
@app.route('/category/new', methods=['GET'])
def newCategory():
    # Defines 'username' and 'picture' to be passed to the templates, where
    # will be parsed to show the user info accordingly
    if 'username' in login_session:
        username = login_session['username']
        picture = login_session['picture']
    else:
        username = ''
        picture = ''
    return (render_template('category_add.html', username=username,
            picture=picture))


# New category save
@app.route('/category/new', methods=['POST'])
def saveNewCategory():
    # Validates that the name of the new categoty is not empty
    if request.form['new_category']:
        try:
            # Create a new categoty object and try to save
            cat_name = request.form['new_category']
            newCategory = Category(
                name=cat_name, user_id=getUserID(login_session['email']))
            session.add(newCategory)
            session.commit()
            flash("New category created")
            return redirect(url_for('mainPage'))
        except Exception as e:
            session.rollback()
            # Verifies if the error is because the user is trying to save a
            # categoty name that already exists on the database
            if 'UNIQUE constraint' in e.message:
                flash("You are trying to add an category that already exists")
            # Informs the user about the other errors
            else:
                flash("Error trying to save new category." + str(e))
            return render_template('category_add.html')
    else:
        flash("Category name cannot be empty")
        return render_template('category_add.html')


# Category delete
@app.route('/category/delete/<int:category_id>', methods=['GET', 'POST'])
def deleleCategory(category_id):
    # if the access is made trough GET the user is sent to the confirmation
    # page
    if request.method == "GET":
        # Defines 'username' and 'picture' to be passed to the templates,
        # where will be parsed to show the user info accordingly
        if 'username' in login_session:
            username = login_session['username']
            picture = login_session['picture']
        else:
            username = ''
            picture = ''
        # Message to be displayed in the confirmation page
        message = "Delete category " + session.query(Category).filter_by(
            id=category_id).one().name + "?"
        # The confirmation page is common to the elimination of items and
        # categories. del_type can be set to "category" or "item"
        del_type = "category"
        return (render_template('delete_confirm.html', id=category_id,
                message=message, del_type=del_type, username=username,
                picture=picture))
    # If the access is made trough POST, is time to delete the category from
    # the database
    if request.method == "POST":
        # The category we want to delete
        itemToDelete = session.query(Category).filter_by(
            id=category_id).one()
        # Validation of the user associated with the category. If the user
        # associated is the same who is connected, can eliminate the category.
        # The user associated can be empty if the script to populate the
        # database were executed
        if (itemToDelete.user_id is not None and
                itemToDelete.user_id == getUserID(login_session['email'])):
            # Validation if the category has items associated. Only if there
            # are no items associated, the category can be eliminated
            nItems = session.query(Item).filter_by(
                category_id=category_id).count()
            if nItems > 0:
                flash(
                    "The category " + itemToDelete.name +
                    " has associated items. Cannot be deleted")
                return redirect(url_for('mainPage'))
            # Elimination of the category from de database
            try:
                session.delete(itemToDelete)
                session.commit()
                flash("Category " + itemToDelete.name + " deleted.")
            # Informs the user of any error that occorred
            except Exception as e:
                session.rollback()
                flash("Error deleting " + itemToDelete.name + str(e))
        else:
            flash("Only the user hwo created the category can delete it.")
    return redirect(url_for('mainPage'))


@app.route('/item/new', methods=['GET', 'POST'])
def addItem():
    # if the access is made trough GET the user is sent to the item creation
    # page
    if request.method == "GET":
        # Defines 'username' and 'picture' to be passed to the templates,
        # where will be parsed to show the user info accordingly
        if 'username' in login_session:
            username = login_session['username']
            picture = login_session['picture']
        else:
            username = ''
            picture = ''
        # Categories to be passed to the template
        categories = session.query(Category)
        if categories.count() is 0:
            flash("You first need to create a category")
            return redirect(url_for('mainPage'))
        return (render_template('item_add.html', categories=categories,
                username=username, picture=picture))
    # If the access is made trough POST, is time to create the item in the
    # database
    if request.method == "POST":
        # Validates if the request has an image
        if 'picture' in request.files:
            # Gets the file from the request
            file = request.files['picture']
            image = file.filename
            try:
                # Validates the file existance and if the file extension is on
                # the permited extensions list
                if file and allowed_file(file.filename):
                    # Implements protection from some known attacks that can
                    # be done trough the name of the file
                    filename = secure_filename(file.filename)
                    # Saves the file to disk
                    file.save(
                        os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    flash("Only PNG, JPG and JPEG allowed")
                    return redirect(request.url)
            except Exception as e:
                flash("Error saving image: " + str(e))
                return redirect(request.url)
        else:
            image = None
        # Validates if the name is not empty
        if request.form['name']:
            name = request.form['name']
        else:
            flash("Name cannot be empty")
            return redirect(request.url)
        # Validates if the description is not empty
        if request.form['description']:
            description = request.form['description']
        else:
            flash("Description cannot be empty")
            return redirect(request.url)
        category = request.form['category']
        # Creates the new object in memory
        newItem = Item(
            name=name, description=description, image=image,
            category_id=category, user_id=getUserID(login_session['email']))
        # Save the new item into the database
        try:
            session.add(newItem)
            session.commit()
            flash("Item " + name + " created.")
            return redirect(url_for('mainPage'))
        # Informs the user of any error that occorred
        except Exception as e:
            session.rollback()
            flash("Error creating new item: " + str(e))
            return redirect(request.url)


@app.route('/item/update/<int:item_id>', methods=['GET', 'POST'])
def updateItem(item_id):
    # if the access is made trough GET the user is sent to the item edition
    # page
    if request.method == "GET":
        # The item to edit
        item = session.query(Item).filter_by(id=item_id).one()
        if item.user_id is not getUserID(login_session['email']):
            flash("Only the user who created the item can edit it.")
            return redirect(url_for('mainPage'))
        # Defines 'username' and 'picture' to be passed to the templates,
        # where will be parsed to show the user info accordingly
        if 'username' in login_session:
            username = login_session['username']
            picture = login_session['picture']
        else:
            username = ''
            picture = ''
        # Categories to be passed to the template
        categories = session.query(Category)
        return (render_template('item_add.html', categories=categories,
                username=username, picture=picture, item=item))
    # If the access is made trough POST, is time to update the item in the
    # database
    if request.method == "POST":
        # Validates if the request has an image
        if 'picture' in request.files:
            # Gets the file from the request
            file = request.files['picture']
            image = file.filename
            try:
                # Validates the file existance and if the file extension is on
                # the permited extensions list
                if file and allowed_file(file.filename):
                    # Implements protection from some known attacks that can
                    # be done trough the name of the file
                    filename = secure_filename(file.filename)
                    # Saves the file to disk
                    file.save(
                        os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    flash("Only PNG, JPG and JPEG allowed")
                    return redirect(request.url)
            except Exception as e:
                flash("Error saving image: " + str(e))
                return redirect(request.url)
        else:
            image = None
        # Validates if the name is not empty
        if request.form['name']:
            name = request.form['name']
        else:
            flash("Name cannot be empty")
            return redirect(request.url)
        # Validates if the description is not empty
        if request.form['description']:
            description = request.form['description']
        else:
            flash("Description cannot be empty")
            return redirect(request.url)
        category = request.form['category']
        # Update in memory the item with the new values
        item = session.query(Item).filter_by(id=item_id).one()
        item.name = name
        item.description = description
        item.category_id = category
        if image:
            item.image = image
        # Updates the item in databse
        try:
            session.commit()
            flash("Item " + name + " updated.")
            return redirect(url_for('mainPage'))
        # Informs the user of any error that occorred
        except Exception as e:
            session.rollback()
            flash("Error updating item: " + str(e))
            return redirect(request.url)


@app.route('/item/delete/<int:item_id>', methods=['GET', 'POST'])
def deleteItem(item_id):
    # if the access is made trough GET the user is sent to the confirmation
    # page
    if request.method == "GET":
        # Defines 'username' and 'picture' to be passed to the templates,
        # where will be parsed to show the user info accordingly
        if 'username' in login_session:
            username = login_session['username']
            picture = login_session['picture']
        else:
            username = ''
            picture = ''
        # Message to be displayed in the confirmation page
        message = "Delete item " + session.query(Item).filter_by(
            id=item_id).one().name + "?"
        # The confirmation page is common to the elimination of items and
        # categories. del_type can be set to "category" or "item"
        del_type = "item"
        return (render_template('delete_confirm.html', id=item_id,
                message=message, del_type=del_type, username=username,
                picture=picture))
    # If the access is made trough POST, is time to delete the item from
    # the database
    if request.method == "POST":
        # The item we wnt to delete
        itemToDelete = session.query(Item).filter_by(id=item_id).one()
        # Validation of the user associated with the item. If the user
        # associated is the same who is connected, can eliminate the item.
        # The user associated can be empty if the script to populate the
        # database were executed
        if (itemToDelete.user_id is not None and
                itemToDelete.user_id == getUserID(login_session['email'])):
            # Elimination of the item from de database
            try:
                session.delete(itemToDelete)
                session.commit()
                flash("Item " + itemToDelete.name + " deleted.")
                # Informs the user of any error that occorred
            except Exception as e:
                session.rollback()
                flash("Error deleting " + itemToDelete.name + str(e))
        else:
            flash("Only the user hwo created the category can delete it.")
    return redirect(url_for('mainPage'))


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=login_session['state'])


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
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
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
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
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

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Create user if doesn't exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session[user_id] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 150px; height: 150px;border-radius: '
    output += '150px;-webkit-border-radius:150px;-moz-border-radius:150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/logout')
def logout():
    return render_template('logout.html')


@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?'
    url += 'token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# API


# Return all the categories and its items
@app.route('/api/v1.0/catalog', methods=['GET'])
def apiGetCatalog():
    return buildAPICatalog()


# Return all the categories
@app.route('/api/v1.0/category/all', methods=['GET'])
def apiGetAllCategories():
    return buildAPIAllCategories()


# Return all the items in a specific category
@app.route('/api/v1.0/category/<int:category_id>/items', methods=['GET'])
def apiGetItemsFromCategory(category_id):
    return buildAPIItemsFromCategory(category_id)


# Returns the detail of an item
@app.route('/api/v1.0/item/<int:item_id>', methods=['GET'])
def apiGetItemDetail(item_id):
    return buildAPIItemDetail(item_id)

# User Helper Functions


# Creates the catalog returned by apiGetCatalog()
def buildAPICatalog():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    catalog = list()
    catalog_item = list()
    for category in categories:
        item_list = list()
        for item in items:
            if item.category_id is category.id:
                item_list.append(item.serialize)
        catalog_item.append({"id": category.id, "name": category.name})
        catalog_item.append({"Items": item_list})
    catalog.append({"Catalog": catalog_item})
    return jsonify(catalog)


# Creates the list with all the categories returned by apiGetAllCategories()
def buildAPIAllCategories():
    categories = session.query(Category).all()
    cat_list = list()
    for category in categories:
        cat_list.append(category.serialize)
    return jsonify(cat_list)


# Creates the list with all the item in a given category returned by
# apiGetItemsFromCategory()
def buildAPIItemsFromCategory(category_id):
    items = session.query(Item).filter_by(category_id=category_id)
    item_list = list()
    for item in items:
        item_list.append(item.serialize)
    return jsonify(item_list)


# Creates de item details returned by apiGetItemDetail()
def buildAPIItemDetail(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item.serialize)


# Creates user in the database from the OAuth user logged on
def createUser(login_session):
    newUser = User(username=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Gets the user information based on the ID
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Gets the user ID from the email address
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Validates if the file extension is allowed to upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
