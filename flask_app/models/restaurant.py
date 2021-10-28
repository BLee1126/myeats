from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_app.models.post import Post

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex = re.compile(r'^(?=.*\d)(?=.*[A-Z])(?!.*[^a-zA-Z0-9@#$^+=])(.{8,})$')

class Restaurant:
    def __init__(self, data):
        self.id = data['id']
        self.restaurant_name = data['restaurant_name']
        self.restaurant_city = data['restaurant_city']
        self.restaurant_email = data['restaurant_email']
        self.restaurant_password = data['restaurant_password']
        self.restaurant_state = data['restaurant_state']
        self.restaurant_street = data['restaurant_street']
        self.restaurant_cuisine = data['restaurant_cuisine']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = None
    def __eq__(self, other):
        return self.id == other.id

    @staticmethod
    def validate_restaurant(data):
        is_valid = True

        if len(data['restaurant_name']) < 2:
            flash("Restaurant name must be at least 2 characters.")
            is_valid = False
        if len(data['restaurant_city']) < 2:
            flash("Restaurant city must be at least 2 characters.")
            is_valid = False
        if not email_regex.match(data['restaurant_email']):
            flash("Please enter a valid email address.")
            is_valid = False
        if  len(Restaurant.get_restaurant_by_email(data)) != 0:
            flash("Restaurant with this email already exits.")
            is_valid = False
        if not password_regex.match(data['restaurant_password']):
            flash("Password needs to be atleast 8 characters and must include a minumum of 1 uppercase letter and number.")
            is_valid = False
        if data['password_confirm'] != data['restaurant_password']:
            flash("Password inputs need to match.")
            is_valid = False
        return is_valid
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM restaurants;'
        connection = connectToMySQL('my_eats')
        results = connection.query_db(query)
        
        restaurants = []

        for result in results:
            restaurant = cls(result)
            restaurants.append(restaurant)
        return restaurants

    @classmethod
    def create_restaurant(cls, data):
        query = 'INSERT INTO restaurants (restaurant_name, restaurant_email, restaurant_city, restaurant_state, restaurant_street, restaurant_cuisine, restaurant_password) VALUES (%(restaurant_name)s,%(restaurant_email)s, %(restaurant_city)s, %(restaurant_state)s, %(restaurant_street)s, %(restaurant_cuisine)s, %(restaurant_password)s)'

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        return results

    @classmethod
    def edit_restaurant(cls, data):
        query = "UPDATE restaurants SET restaurant_email = %(restaurant_email)s, restaurant_name = %(restaurant_name)s, restaurant_city = %(restaurant_city)s, restaurant_state = %(restaurant_state)s, restaurant_street = %(restaurant_street)s, restaurant_cuisine = %(restaurant_cuisine)s, updated_at = NOW(), restaurant_password = %(restaurant_password)s WHERE restaurants.id = %(restaurant_id)s"

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        return results


    @classmethod
    def get_restaurant_by_email(cls, data):
        query = 'SELECT * FROM restaurants WHERE restaurants.restaurant_email = %(restaurant_email)s'

        connection = connectToMySQL('my_eats')
        result = connection.query_db(query, data)
        restaurants = []
        for restaurant in result:
            restaurants.append(cls(restaurant))

        if restaurants:
            return restaurants[0]

        else: 
            return None;

    @classmethod
    def get_restaurant_by_id(cls, data):
        query = 'SELECT * FROM restaurants WHERE restaurants.id = %(restaurant_id)s'


        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)[0]
        restaurant = cls(results)

        return restaurant

    @classmethod
    def get_restaurant_by_food_type(cls, data):
        query = 'SELECT * FROM restaurants JOIN foods ON restaurant_id WHERE food_type = %(food_type)s' 

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        restaurants = []
        for restaurant in results:
            restaurants.append(cls(restaurant))
        return restaurants

    @classmethod
    def get_restaurants_by_state(cls, data):
        query = 'SELECT * FROM restaurants WHERE restaurant_state = %()s'


        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        restaurants = []
        for restaurant in results:
            restaurants.append(cls(restaurant))
        return restaurants

    @classmethod
    def get_posts(cls, data):
        query = 'SELECT * FROM restaurants JOIN posts ON posts.restaurant_id = restaurants.id JOIN users ON posts.user_id = users.id JOIN uploads ON uploads.user_id = posts.user_id WHERE restaurants.id = %(restaurant_id)s'  

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        posts = []

        for result in results:
            data = {
                'content': result['content'],
                'rating': result['rating'],
                'user_id': result['user_id'],
                'restaurant_id': result['restaurant_id'],
                'upload': result['uploads.content']
            }
            posts.append(data)

        return posts

    @classmethod
    def save_upload(cls, data):
        query = "INSERT INTO restaurant_uploads(description, uploads, restaurants_id ) VALUES(%(description)s, %(file_name)s, %(restaurant_id)s )"

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        return results

    @classmethod
    def get_uploads(cls, data):
        query = 'SELECT * FROM restaurant_uploads where restaurants_id = %(restaurant_id)s'

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)
        uploads = []
        for result in results:
            result['uploads'] = 'flask_app/assets/restaurants_uploads/'+ result['uploads']
            uploads.append(result)
            
        return uploads

    @classmethod
    def get_favorites(cls, data):
        query = 'SELECT * FROM favorites where restaurants_id = %(restaurant_id)s'
        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)
        favorites = []
        # for result in results:
        #     result['favorites'] = 
