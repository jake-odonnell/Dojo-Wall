from Flask_app.config.mysqlconnection import connectToMySQL

class Comment:
    def __init__(self, data:dict):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None