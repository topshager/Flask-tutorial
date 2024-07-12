import os
from flask  import Flask
from.import db
from . import auth

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    #creating a flask instance


    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        #load the instance config, if it exists ,when not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        #load test config if passed in
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    #a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'hello ,world!'

    from.import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/',endpoint='index')
    
    return app
