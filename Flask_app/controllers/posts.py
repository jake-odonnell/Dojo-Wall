from Flask_app import app
from Flask_app.models.post import Post
from flask import request, redirect, render_template, session, flash

@app.route('/add-post', methods = ['POST'])
def f_add_post():
    if Post.val_post(request.form):
        id = Post.add_post(request.form)
    return redirect('/wall')

@app.route('/delete-post', methods = ['POST'])
def f_delete_post():
    Post.delete_post(request.form)
    return redirect('/wall')