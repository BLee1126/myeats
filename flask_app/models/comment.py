from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app


class Comment:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.post_user_id = data['post_user_id']
        self.post_id = data['posts_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.restaurant_id = data['restaurant_id']

    @classmethod
    def get_comments_from_post(cls, data):
        query = 'SELECT * FROM comments JOIN posts ON posts.users_id = comments.post_user_id WHERE comments.post_user_id = %(user_id)s '

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        comments = []
        for result in results:
            comment = cls(result)
            comments.append(comment)

        return comments

    def create_comment(cls, data):
        query = "INSERT INTO comments (user_id, post_user_id, content) VALUES (%(user_id)s, %(post_user_id)s, %(content)s)"

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        return results

    def delete_comment(cls, data):
        query = "DELETE FROM comments WHERE comments.posts_id = %(post_id)s"

        connection = connectToMySQL('my_eats')
        results = connection.query_db(query, data)

        return results