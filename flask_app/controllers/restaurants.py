from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.restaurant import Restaurant
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = 'flask_app/assets/restaurants_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# RESTAURANT LOGIN/REGISTER PAGE
@app.route('/restaurants/register')
def show_restaurant_registration():
    return render_template('restaurant_login.html')

# CREATE RESTAURANT
@app.route('/restaurants/create', methods = ['POST'])
def create_restaurant():
    if Restaurant.validate_restaurant(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['restaurant_password'])
        data = {
            'restaurant_name': request.form['restaurant_name'],
            'restaurant_city': request.form['restaurant_city'],
            'restaurant_state' : request.form['restaurant_state'],
            'restaurant_street' : request.form['restaurant_street'],
            'restaurant_cuisine' : request.form['restaurant_cuisine'],
            'restaurant_email' : request.form['restaurant_email'],
            'restaurant_password': pw_hash,
        }
        Restaurant.create_restaurant(data)
        restaurant = Restaurant.get_restaurant_by_email(data)[0]
        session['restaurant_id'] = restaurant.id
        return redirect(f'/restaurants/dashboard/{restaurant.id}')
    return redirect('/')

# LOGIN RESTUARANT
@app.route('/restaurants/login', methods =['POST'] )
def log_in():

    session['reg_submit'] = False
    session['login_submit'] = True
    data = {
        'restaurant_email': request.form['restaurant_email']
    }
    restaurant_in_db = Restaurant.get_restaurant_by_email(data)
    if not restaurant_in_db:
        flash("Ahh beans...your email and/or password is incorrect :-/")
        return redirect("/restaurants/register")

    if not bcrypt.check_password_hash(restaurant_in_db.restaurant_password, request.form['restaurant_password']):
        flash("Ahh beans...your email and/or password is incorrect :-/")
        return redirect('/restaurants/register')
    # STORE SESSION DATA
    session['restaurant_id'] = restaurant_in_db.id

    return redirect(f'/restaurants/dashboard/{restaurant_in_db.id}')

# RESTAURANT DASHBAORD
@app.route ('/restaurants/dashboard/<int:restaurant_id>', methods=['GET'])
def dashboard(restaurant_id):
    if not 'restaurant_id' in session:
        flash('Log in first!')
        return redirect('/restaurants/register')
    data = {
        'restaurant_id': restaurant_id
    }

    restaurant = Restaurant.get_restaurant_by_id(data)
    return render_template('restaurant_dashboard.html', restaurant = restaurant)

# Restaurant cuisiine (set from user dashboard) - here due to naming convention of url
@app.route('/restaurants/category/<string:category>')
def set_category(category):
    session['category'] = category
    print("made it to this route")
    return redirect(request.referrer)

@app.route('/restaurants/category')
def unset_category():
    if 'category' in session:
        session.pop('category')
        return redirect(request.referrer)
    
    return redirect(request.referrer)

@app.route ('/restaurants/profile/<int:restaurant_id>', methods=['GET'])
def profile(restaurant_id):
    if 'restaurant_id' in session:

        data = {
            'restaurant_id': restaurant_id
        }

        restaurants = Restaurant.get_all()

        restaurant = Restaurant.get_restaurant_by_id(data)
        return render_template('restaurant_profile.html', restaurant = restaurant, restaurants = restaurants)
    elif 'user_id' in session:
        data = {
            'restaurant_id': restaurant_id
        }
        restaurants = Restaurant.get_all()

        restaurant = Restaurant.get_restaurant_by_id(data)
        return render_template('restaurant_profile.html', restaurant = restaurant, restaurants = restaurants)
    else:
        flash('Log in first!')
        return redirect('/restaurants/register')

# Restaurant UPLOADS
@app.route('/restaurants/uploader', methods=['POST', 'GET'])
def restaurants_upload_file():
    restaurant_id = session['restaurant_id']
    if request.method == 'POST':
        file = request.files['image']
        file.name = request.form['name']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.name)+'.png'))

        if not request.form['description']:
            request.form['description'] = ''

        data = {
            'restaurant_id': session['restaurant_id'],
            'description': request.form['description'],
            'file_name': secure_filename(file.filename)
        }
        Restaurant.save_upload(data)

        flash('file uploaded successfully')
        return redirect(f'/restaurants/dashboard/{restaurant_id}')
    
    

    return redirect(f'/restaurants/dashboard/{restaurant_id}')

#RESTAURANT UPLOADS GET
@app.route('/restaurants/get_uploads')
def restaurant_uploads():
    restaurant_id = session['restaurant_id']
    data = {
        'restaurant_id': session['restaurant_id']
    }
    Restaurant.get_uploads(data)


    return redirect(f'/restaurants/dashboard/{restaurant_id}')
            
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        #     return 'File uploaded successfully'
