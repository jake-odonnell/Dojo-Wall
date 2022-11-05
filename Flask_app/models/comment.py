from Flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment:
    def __init__(self, data:dict):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user_name = data['user_first_name']
        self.post_id = data['post_id']

    @classmethod
    def add_comment(cls, data:dict):
        query = 'INSERT INTO comments (post_id, user_id, content) VALUES (%(post_id)s, %(user_id)s, %(content)s);'
        print(data)
        return connectToMySQL('wall').query_db(query, data)

    @staticmethod
    def val_comment(data:dict):
        is_val = True
        if data['content'] == '':
            is_val = False
            flash('Must include comment')
        return is_val

    @staticmethod
    def delete_comment(data:dict):
        query = 'DELETE FROM comments WHERE id = %(id)s;'
        id = connectToMySQL('wall').query_db(query, data)
        return id