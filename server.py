from Flask_app import app
from Flask_app.controllers import users, posts, comments

if __name__ == '__main__':
    app.run(debug = True)