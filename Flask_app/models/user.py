from Flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from .post import Post
from .comment import Comment
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__(self, data:dict):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.posts = []
        self.comments = []
    
    @classmethod
    def add_user(self, data:dict):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s);'
        id = connectToMySQL('wall').query_db(query, data)
        return id

    @classmethod
    def val_new_user(cls, data:dict):
        is_val = True
        if len(data['first_name']) < 2 or str.isalpha(data['first_name']) == False:
            is_val = False
            flash('* Must have valid first name')
        if len(data['last_name']) < 2 or str.isalpha(data['last_name']) == False:
            is_val = False
            flash('* Must have valid last name')
        if not EMAIL_REGEX.match(data['email']):
            is_val = False
            flash('* Must have valid email')
        emails = cls.get_all_emails()
        for email in emails:
            if email['email'] == data['email']:
                is_val = False
                flash('*Must have unique email')
        if len(data['password']) < 8:
            is_val = False
            flash('* Must have valid password')
        if not str.isalnum(data['password']):
            is_val = False
            flash('* Must have 1 letter and 1 number')
        else:
            if str.isalpha(data['password']) or str.isnumeric(data['password']):
                is_val = False
                flash('* Must have 1 letter and 1 number')
        if data['password'] != data['conf_password']:
            is_val = False
            flash('* Passwords must match')
        return is_val

    @staticmethod
    def get_all_emails():
        query = 'SELECT email FROM users'
        emails = connectToMySQL('wall').query_db(query)
        return emails

    @staticmethod
    def login(data:dict):
        query = 'SELECT id, password FROM users WHERE email = %(email)s'
        return connectToMySQL('wall').query_db(query, data)

    @classmethod
    def get_user_from_id(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        data = {'id': id}
        result = connectToMySQL('wall').query_db(query, data)
        user = cls(result[0])
        query = 'SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id WHERE users.id = %(id)s'
        data = {'id': id}
        result = connectToMySQL('wall').query_db(query, data)
        for post in result:
            data = {
                'id': post['id'],
                'content': post['content'], 
                'created_at': post['created_at'],
                'updated_at': post['updated_at'],
                'user_id': post['user_id'],
                'first_name': post['first_name']
            }
            user.posts.append(Post(data))
        query = 'SELECT * FROM comments LEFT JOIN users on users.id = comments.user_id WHERE users.id = %(id)s;'
        data = {'id': id}
        comments = connectToMySQL('wall').query_db(query, data)
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
            user.comments.append(Comment(data))
        return user