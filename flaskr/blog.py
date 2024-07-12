from flask import(
    Blueprint,flash,g,redirect,render_template,request,url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import abort
from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint('blog',__name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title,body,created,author_id,username'
        'FROM post p JOIN user u ON p.author_id = u.id'
        'ORDER BY CREATED DESC'
    ).fetchall()
    return render_template('blog/index.html',posts=posts)

@bp.route('/create',methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        title =request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title,body,author_id)'
                'VALUES(?,?,?)'
                (title,body,g.user['id'])
            )
            db.commit()
            return redirect('blog/create.html')

def get_post(id,check_author=True):
    post = get_db().execute(
        'SELECT p.id,title,body ,created,author_id,username'
        'FROM POST P JOIN usr u on p.author_id = user.id'
        'WHERE p.id = ?',
        (id)
    ).fetchall()
    if post is None:
        abort(404,"f post id {id} does not exist.")
    if check_author and post['author_id'] != g.user[id]:
        abort(403)
    return post

@bp.rout('/<int:id>/update',mehtods=('GET','POST'))
@login_required
def update(id):
    
