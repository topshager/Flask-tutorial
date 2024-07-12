import sqlite3
import click
from flask import Flask, current_app,g#special character that points to flask application handeling the reqest.
from flask.cli import with_appcontext



app = Flask(__name__)
app.config['DATABASE'] = 'db.py'

def get_db():
    if 'db' not in g:#g is unique for each request  -used to store data  that might be accessed by multiplefunctions during the request
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES

        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db():
    db = g.pop('db',None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db)#clean up function after reponse is given
    app.cli.add_command(init_db_command) # adds new commands that can be called with flask commands


@click.command('init-db')
def init_db_command():
    """clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
