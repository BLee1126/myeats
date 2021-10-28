from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
from flask_app.models.restaurant import Restaurant

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex = re.compile(r'^(?=.*\d)(?=.*[A-Z])(?!.*[^a-zA-Z0-9@#$^+=])(.{8,})$')

class User:
    def __init__(self, data):
      self.id = data['id']
      self.first_name = data['first_name']
      self.last_name = data['last_name']
      self.email = data['email']
      self.password = data['password']
      self.created_at = data['created_at']
      self.updated_at = data['updated_at']
    def __eq__(self, other):
          return self.id == other.id

    @staticmethod
    def validate_user(data):
      is_valid = True

      if len(data['first_name']) < 2:
          flash("Name must be at least 2 characters.")
          is_valid = False
      if len(data['last_name']) < 2:
          flash("Last name must be at least 2 characters.")
          is_valid = False
      if not email_regex.match(data['email']):
          flash("Please enter a valid email address.")
          is_valid = False
      if  len(User.get_user_by_email(data)) != 0:
          flash("User with this email already exits.")
          is_valid = False
      if not password_regex.match(data['password']):
          flash("Password needs to be atleast 8 characters and must include a minumum of 1 uppercase letter and number.")
          is_valid = False
      if data['password_confirm'] != data['password']:
          flash("Password inputs need to match.")
          is_valid = False
      return is_valid

    @classmethod
    def get_all(cls):
      query = 'SELECT * FROM users;'
      connection = connectToMySQL('my_eats')
      results = connection.query_db(query)
      users = []

      for result in results:
        person = cls(result)
        users.append(person)
      return users


    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s)'
        pw_hash = bcrypt.generate_password_hash(data['password'])
        data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': pw_hash,
        }
        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        return results
        
    @classmethod
    def edit_user(cls, data):
      query = "UPDATE users SET email = %(email)s, first_name = %(first_name)s, last_name = %(last_name)s, profile_pic = %(profile_pic)s, updated_at = NOW(), password = %(password)s WHERE users.id = %(user_id)s"

      connection = connectToMySQL('my_eats')
      results = connection.query_db(query, data)

      return results

    @classmethod
    def get_user_by_email(cls, data):
      query = 'SELECT * FROM users WHERE users.email = %(email)s'
      data = {
        'email': data['email']
      }
      connection = connectToMySQL('my_eats')
      results = connection.query_db(query, data)

      users = []
      for user in results:
          users.append(cls(user))

      return users

    @classmethod
    def get_user_by_id(cls, data):
      query = 'SELECT * FROM users WHERE users.id = %(user_id)s'

      connection = connectToMySQL('my_eats')
      result = connection.query_db(query, data)[0]


      return result

    @classmethod
    def get_following(cls, data):
      query = "SELECT * FROM follows JOIN users on users.id = follows.user_id WHERE follower_id = %(user_id)s;"

      connection = connectToMySQL('my_eats')
      results = connection.query_db(query, data)
      following_list = []

      for result in results:
        person = cls(result)
        following_list.append(person)

      return following_list

    @classmethod
    def get_suggestions(cls, data):
      query = "SELECT * FROM foods JOIN restaurants on restaurants.id = restaurant_id WHERE food_type = %(restaurant_cuisine)s;"

      connection = connectToMySQL('my_eats')
      results = connection.query_db(query, data)

      restaurants = []

      for restaurant in results:
        restaurants.append(Restaurant(restaurant))

      return restaurants


    @classmethod
    def add_favorite(cls, data):
      query = "INSERT INTO favorites (restaurant_id, user_id, ocassion) VALUES (%(restaurant_id)s, %(user_id)s, %(ocassion)s)"

      connection = connectToMySQL('my_eats')
      results = connection.query_db(query, data)

      return results

    @classmethod
    def remove_favorite(cls, data):
      query = "DELETE FROM favorites WHERE user_id = %(user_id)s AND restaurant_id = %(restaurant_id)s AND ocassion = %(ocassion)s"

      connection = connectToMySQL('my_eats')
      results = connection.query_db(query, data)

      return results

    @classmethod
    def add_follow(cls, data):
      query = "INSERT INTO follows (user_id, follower_id) VALUES (%(user_id)s, %(follower_id)s)"

      connection = connectToMySQL('my_eats')
      results = connection.query_db(query, data)

      return results

    @classmethod
    def delete_follow(cls, data):
      query = "DELETE FROM follows WHERE user_id = %(user_id)s AND follower_id = %(follower_id)s"
      connection = connectToMySQL('my_eats')
      connection.query_db(query, data)

      return 


    @classmethod
    def get_favorites(cls, data):
      query = "SELECT * FROM favorites JOIN restaurants ON restaurants.id = favorites.restaurant_id WHERE user_id = %(user_id)s"

      connection = connectToMySQL('my_eats')
      results = connection.query_db(query, data)

      restaurants = []

      for restaurant in results:
        restaurants.append(Restaurant(restaurant))

      return restaurants

    @classmethod
    def save_upload(cls, data):
        query = "INSERT INTO uploads(content, posts_restaurant_id, posts_id, users_id, file_name) VALUES(%(content)s, %(restaurant_id)s, %(post_id)s, %(user_id)s, %(file_name)s)"

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        return results

    @classmethod
    def get_all_uploads(cls, data):
        query = 'SELECT * FROM uploads where users_id = %(user_id)s'

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)
        uploads = []
        for result in results:
            result['uploads'] = 'flask_app/assets/users_uploads/'+ result['uploads']
            uploads.append(result)
            
        return uploads