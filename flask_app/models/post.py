from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.comment import Comment


    


class Post:
    def __init__(self, data):
        self.user_id = data['users_id']
        self.restaurant_id = data['restaurants_id']
        # self.rating = data['rating']
        self.content = None
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comments = None
        self.restaurant_name = data['restaurant_name']
        self.restaurant_state = data['restaurant_state']
        self.restaurant_city = data['restaurant_city']
        self.restaurant_street = data['restaurant_street']
        self.uploads = None

    @classmethod
    def get_all_posts_user(cls, data):
        query = 'SELECT * FROM posts JOIN users ON users.id = posts.users_id JOIN restaurants on restaurants.id = restaurants_id WHERE users.id = %(user_id)s'
        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        posts = []

        for result in results:
            post = cls(result)
            
            data = {
                'user_id': result['users_id']
            }
            post.comments = Comment.get_comments_from_post(data)
            posts.append(post)


        return posts



    @classmethod
    def get_all_posts_restaurant(cls, data):
        query = 'SELECT * FROM posts WHERE posts.restaurant_id = %(restaurant_id)s'

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        posts = []

        for result in results:
            post = cls(result)
            data = {
                'user_id': result.user_id
            }
            post.comments = Comment.get_comments_from_post(data)
            posts.append(post)

        return posts

    @classmethod
    def create_post(cls, data):
        query = "INSERT INTO posts (users_id, restaurants_id, content) VALUES (%(user_id)s, %(restaurant_id)s, %(content)s)"

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        return results
    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts WHERE users_id = %(user_id)s AND restaurants_id = %(restaurant_id)s"

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        return results

    @classmethod
    def get_uploads_for_post():
        query = 'SELECT * FROM uploads where users_id = %(user_id)s'

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)
        uploads = []
        for result in results:
            result['uploads'] = 'flask_app/assets/restaurants_uploads/'+ result['uploads']
            uploads.append(result)
            
        return uploads

    




