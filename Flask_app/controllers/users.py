from Flask_app import app
from flask import render_template, redirect, session, request, flash
from Flask_app.models.user import User
from Flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login')
def r_login():
    if session:
        data = session
    else:
        data = {
            'first_name': '',
            'last_name': '',
            'email': ''
        }
    return render_template('login.html', info = data)

@app.route('/register', methods = ['POST'])
def f_register():
    if User.val_new_user(request.form):
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        session['user_id'] = User.add_user(data)
        return redirect('/wall')
    else:
        session['is_reg'] = True
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        return redirect('/login')

@app.route('/f-login', methods = ['POST'])
def f_login():
    if request.form['email'] == '' or request.form['password'] == '':
        session['is_reg'] = False
        flash('Invalid username/ password')
        return redirect('/login')
    user = User.login(request.form)
    if bcrypt.check_password_hash(user[0]['password'], request.form['password']):
        session['user_id'] = user[0]['id']
        return redirect('/wall')
    else:
        session['is_reg'] = False
        flash('Invalid username/ password')
        return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/wall')
def r_home():
    if session.get('user_id') == None:
        return redirect('/login')
    else:
        id = session['user_id']
        print(id)
        user = User.get_user_from_id(id)
        print(user.id)
        posts = Post.get_all_posts()
        return render_template('home.html', user = user, posts = posts)