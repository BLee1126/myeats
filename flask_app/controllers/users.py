from flask_app.models.restaurant import Restaurant
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'flask_app/assets/users_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('/login.html')

@app.route('/dashboard')
def success():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        other_users = User.get_all()
        friends = User.get_following(data)
        restaurants = Restaurant.get_all()
        favorites = User.get_favorites(data)

        return render_template('/dashboard.html', user = user, other_users = other_users, friends = friends, restaurants = restaurants, favorites = favorites)
    return redirect('/')

# CREATE USER
@app.route('/users/create', methods=['POST'])
def register_user():
    # session variables for toggling flash messages between login and reg forms
    session['reg_submit'] = True
    session['login_submit'] = False

    if not User.validate_user(request.form):
        return redirect('/')

    new_user = User.create_user(request.form)

    if new_user == False:
        print('Something went wrong registering user.')
        return redirect('/')
    # STORE SESSION DATA
    session['reg_submit'] = False
    session['user_id'] = new_user
    return redirect('/dashboard')

# LOGIN USER
@app.route('/login', methods=['POST'])
def login_user():
    # session variables for toggling flash messages between login and reg forms
    session['reg_submit'] = False
    session['login_submit'] = True

    data = { "email" : request.form["email"] }
    user_in_db = User.get_user_by_email(data)[0]

    if not user_in_db:
        flash("Ahh beans...your email and/or password is incorrect :-/")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Ahh beans...your email and/or password is incorrect :-/")
        return redirect('/')
    # STORE SESSION DATA
    session['user_id'] = user_in_db.id
    session['user_first_name'] = user_in_db.first_name
    return redirect('/dashboard')

# LOGOUT USER
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# USER POSTS
@app.route('/posts/new')
def post_form():
    return render_template('/user_post.html')

# USER PROFILE
@app.route('/users/profile')
def view_profile():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        friends = User.get_following(data)
        other_users = User.get_all()
        # posts = Post.get_all_posts_user(data)

        return render_template('/user_profile.html', user = user, friends = friends, other_users = other_users)
    return redirect('/')

# USER PROFILE BY ID
@app.route('/users/profile/<int:user_id>')
def view_users_profile(user_id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(user_id)
        friends = User.get_following(data)
        other_users = User.get_all()
        # posts = Post.get_all_posts_user(data)

        return render_template('/user_profile.html', user = user, friends = friends, other_users = other_users)
    return redirect('/')

#FOLLOW A USER
@app.route('/users/follow/<int:other_user>')
def follow_user(other_user):
    if 'user_id' in session:
        data = {
            'user_id': other_user,
            'follower_id': session['user_id']
        }
        User.add_follow(data)
        
        return redirect(request.referrer)

# USER UPLOADS
@app.route('/users/uploader/<int:post_id>/<int:restaurant_id>/<string:file_name>', methods=['POST', 'GET'])
def users_upload_file(post_id, restaurant_id, file_name):
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        data = {
            "content": file,
            "restaurant_id": restaurant_id,
            "post_id": post_id,
            "user_id": session.user_id,
            "file_name": file_name
        }

        User.save_upload(data)
            
        return 'File uploaded successfully'

# EDIT USER PROFILE
@app.route('/users/edit', methods=['POST'])
def edit_user_profile():
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "user_id": session['user_id'],
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            'password': pw_hash,
            "profile_pic": request.form['profile_pic']
        }
        User.edit_user(data)
        return redirect(request.referrer)
    return redirect(request.referrer)

# GET USER FAVORITES
@app.route('/users/favorites', methods=['POST'])
def get_all_favorites():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
        }
        restaurants =  User.get_favorites(data)
        return redirect('/dashboard')