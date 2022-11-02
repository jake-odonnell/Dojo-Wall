from Flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from Flask_app.models.user import User

class Post:
    def __init__(self, data:dict):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.comments = []

    @classmethod
    def add_post(cls, data:dict):
        query = 'INSERT into posts (content, user_id) VALUES (%(content)s, %(user_id)s)'
        id = connectToMySQL('wall').query_db(query, data)
        return id

    @staticmethod
    def val_post(data:dict):
        is_val = True
        if data['content'] == '':
            is_val = False
            flash('* Post must not be blank')
        print(is_val)
        return is_val

    @classmethod
    def get_all_posts(cls):
        query = 'SELECT * FROM posts'
        results = connectToMySQL('wall').query_db(query)
        posts = []
        for post in results:
            user = User.get_user_from_id(post['user_id'])
            posts.append(cls(post))
            posts[-1].creator = user
        return posts