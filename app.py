import socket, copy
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bootstrap import Bootstrap
from functools import wraps



# CONFIG
app = Flask(__name__)
# Connecting to mysql database using python sql alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://csc2033_team39:Sews|ToeGong@localhost:3307/csc2033_team39'
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LdwZQgeAAAAADGS0TsKqD_310OwG1aF2mxliOMD"
app.config['RECAPTCHA_PRIVATE_KEY'] = "6LdwZQgeAAAAANQRFfcDT9czDaIPD19zx6rblLIG"
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


# REQUIRES_ROLES Reference from CSC2021
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                # Redirect the user to an unauthorised notice!
                return redirect(url_for('403'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper


# ERROR PAGE VIEWS Reference from CSC2021
@app.errorhandler(400)
def bad_request(error):
    db_add_commit(new_security_error('400'))
    return render_template('400.html'), 400


@app.errorhandler(403)
def forbidden(error):
    db_add_commit(new_security_error('403'))
    if current_user:
        new_security_event('UNAUTHORISED ACCESS ATTEMPT', current_user.email)
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found(error):
    db_add_commit(new_security_error('404'))
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db_add_commit(new_security_error('500'))
    return render_template('500.html'), 500


@app.errorhandler(503)
def service_unavailable(error):
    db_add_commit(new_security_error('503'))
    return render_template('503.html'), 503


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/shop")
def shop():
    return render_template('shop.html')


@app.route("/games")
def games():
    return render_template('games.html')


@app.route("/charities")
def charities():
    return render_template('charities.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')


def db_add_commit(an_object):  # Makes commit to db more compact
    db.session.add(an_object)
    db.session.commit()


if __name__ == '__main__':
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()
    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from models import User, new_security_error, new_security_event


    @login_manager.user_loader
    def load_user(user_key):
        return User.query.get(user_key)

    # import blueprints
    from user.views import users_blueprint
    from admin.views import admin_blueprint

    # register blueprints with app
    app.register_blueprint(users_blueprint)
    app.register_blueprint(admin_blueprint)
    app.run(host=my_host, port=free_port, debug=True)
