from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, SearchForm, LogoutForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from ghibli_requests import *

app = Flask(__name__)
proxied = FlaskBehindProxy(app)

app.config['SECRET_KEY'] = '72e9f4947d7402c35e624639d2f3e0e8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

engine = create_engine('sqlite:///site.db')
meta = db.MetaData()

user = ''


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Watchlist(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    title = db.Column(db.String(40), unique=False, nullable=False)

    def __repr__(self):
        return f"Watchlist('{self.username}', '{self.title}')"


@app.route("/")
def home():
    return render_template('home.html',
                           title='Home', text='Welcome to the app!')


@app.route("/about")
def about():
    return render_template('about.html',
                           title='About', text='Learn about this app')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # checks if entries are valid
        user = User(username=form.username.data,
                    email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))  # if so - send to home page
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    global user
    form = LoginForm()
    target = User.query.filter_by(username=form.username.data).all()
    password = User.query.filter_by(
               username=form.username.data).first().password
    if form.validate_on_submit() and (target != []) and
    (password == form.password.data):  # checks if entries are valid
        user = form.username.data
        return redirect(url_for('my_watchlist'))  # if so - send to home page
    return render_template('login.html', form=form)


@app.route("/my_watchlist")
def my_watchlist():
    return render_template('watchlist.html',
                           title=f'{user}\'s Watchlist',
                           items=Watchlist.query.filter_by(
                                 username=user).all())


@app.route("/my_watchlist/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        ttl = get_title(form.query.data)
        if (ttl is not None):
            title = Watchlist(username=user, title=ttl['title'])
            db.session.add(title)
            db.session.commit()
            flash(f'{form.query.data} has been added to your watchlist!',
                  'success')
        else:
            flash(f'{form.query.data} could not be found', 'failure')
    return render_template('search.html', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    form = LogoutForm()
    if form.validate_on_submit():
        user = ''
        return redirect(url_for('home'))
    return render_template('logout.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
