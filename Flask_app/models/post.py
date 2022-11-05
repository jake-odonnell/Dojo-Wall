from Flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from .comment import Comment

class Post:
    def __init__(self, data:dict):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user_name = data['first_name']
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
        return is_val

    @classmethod
    def get_all_posts(cls):
        query = 'SELECT * FROM posts LEFT JOIN users ON users.id = posts.user_id ORDER BY posts. updated_at DESC'
        results = connectToMySQL('wall').query_db(query)
        posts = []
        for post in results:
            posts.append(cls(post))
            query = 'SELECT * FROM comments LEFT JOIN posts ON posts.id = comments.post_id LEFT JOIN users ON users.id = comments.user_id WHERE posts.id = %(id)s;'
            data = {'id': posts[-1].id}
            comments = connectToMySQL('wall').query_db(query, data)
            if comments:
                for comment in comments:
                    data = {
                        'id': comment['id'],
                        'content': comment['content'],
                        'created_at': comment['created_at'],
                        'updated_at': comment['updated_at'],
                        'user_id': comment['user_id'],
                        'user_first_name': comment['first_name'],
                        'post_id': comment['post_id']
                    }
                    posts[-1].comments.append(Comment(data))
        return posts

    @staticmethod
    def delete_post(data:dict):
        query = 'DELETE FROM comments WHERE post_id = %(id)s'
        connectToMySQL('wall').query_db(query, data)
        query = 'DELETE FROM posts WHERE id = %(id)s;'
        id = connectToMySQL('wall').query_db(query, data)
        return id