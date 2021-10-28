from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User

class Favorite:
    def __init__(self, data):
        self.user_id = data['users_id']
        self.restaurant_id = data['restaurants_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ocassion = ''

    @classmethod
    def get_all_favs_user(cls, data):
        query = 'SELECT * FROM favorites JOIN users ON users.id = favorites.users_id JOIN restaurants on restaurants.id = restaurants_id WHERE users.id = %(user_id)s'
        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        favs = []

        for result in results:
            post = cls(result)
            
            data = {
                'user_id': result['users_id'],
                'restaurant_id': result['restaurant_id'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at'],
                'ocassion': result['ocassion']
            }
            fav = Favorite(data)
            favs.append(fav)


        return favs

    @classmethod
    def get_all_favs_rest(cls, data):
        query = 'SELECT * FROM favorites JOIN restaurant ON restaurant.id = favorites.restaurant_id JOIN restaurants on restaurants.id = restaurants_id WHERE restaurant.id = %(user_id)s'
        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        favs = []

        for result in results:
            post = cls(result)
            
            data = {
                'user_id': result['users_id'],
                'restaurant_id': result['restaurant_id'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at'],
                'ocassion': result['ocassion']
            }
            fav = Favorite(data)
            favs.append(fav)


        return favs