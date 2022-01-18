import socket
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


#CONFIG
app = Flask(__name__)
# Connecting to mysql database using python sql alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://csc2033_team39:Sews|ToeGong@localhost:3307/csc2033_team39'
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LdwZQgeAAAAADGS0TsKqD_310OwG1aF2mxliOMD"
app.config['RECAPTCHA_PRIVATE_KEY'] = "6LdwZQgeAAAAANQRFfcDT9czDaIPD19zx6rblLIG"

db = SQLAlchemy(app)


# ERROR PAGE VIEWS Reference from CSC2021
@app.errorhandler(400)
def bad_request(error):
    # Adding page 500 error to the security logs
    return render_template('400.html'), 400


@app.errorhandler(403)
def forbidden(error):
    # Adding page 500 error to the security logs
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found(error):
    # Adding page 500 error to the security logs
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    # Adding page 500 error to the security logs

    return render_template('500.html'), 500


@app.errorhandler(503)
def service_unavailable(error):
    # Adding page 500 error to the security logs

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


@app.route("/donate")
def donate():
    return render_template('donate.html')


@app.route("/profile")
def profile():
    return render_template('profile.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == '__main__':
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    app.run(host=my_host, port=free_port, debug=True)
