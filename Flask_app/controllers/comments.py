from Flask_app import app
from Flask_app.models.comment import Comment
from flask import request, redirect

@app.route('/add-comment', methods = ['POST'])
def f_add_comment():
    if Comment.val_comment(request.form):
        Comment.add_comment(request.form)
    return redirect('/wall')

@app.route('/delete-comment', methods = ['POST'])
def f_delete_comment():
    Comment.delete_comment(request.form)
    return redirect('/wall')