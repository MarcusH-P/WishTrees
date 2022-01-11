import socket
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

#CONFIG
app = Flask(__name__)
# Connecting to mysql database using python sql alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://csc2033_team39:Sews|ToeGong@localhost:3307/csc2033_team39'
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LdwZQgeAAAAADGS0TsKqD_310OwG1aF2mxliOMD"
app.config['RECAPTCHA_PRIVATE_KEY'] = "6LdwZQgeAAAAANQRFfcDT9czDaIPD19zx6rblLIG"

db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

if __name__ == '__main__':
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    app.run(host=my_host, port=free_port, debug=True)
