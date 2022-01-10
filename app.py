# IMPORTS
import logging
import socket
from functools import wraps
from flask import Flask, render_template, request
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

app = Flask(__name__)


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

if __name__ == "__main__":
    app.run(debug=True)

    # BLUEPRINTS
    # import blueprints