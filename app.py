from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migration = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.route("/")
def index():
    return render_template("register.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            flash("user deja enregistre", "warning")
            return redirect(url_for('index'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("user a été bien enregistré", "success")

    return redirect(url_for('index'))


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["username"] = user.username
            return redirect(url_for('welcome'))

    return redirect(url_for('index'))


@app.route("/dashborad")
def welcome():
    name = session.get("username")
    return f"<h1> Bienvenue Mr {name}</h1>"


if __name__ == "__main__":
    app.run(debug=True, port=5012)
