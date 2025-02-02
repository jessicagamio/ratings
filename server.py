"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Ratings, Movies, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """show a list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register')
def register_form():
    """Show Registration form"""

    return render_template("registration_form.html")

@app.route('/register', methods =["POST"])
def register_process():
    """Process Registration form"""

    email = request.form.get("email")
    password = request.form.get("password")

    # if User.query.filter(User.email.in_(email)):
    if User.query.filter(User.email == email).first():
        return redirect('/') 

    else:
        user= User(email = email, password = password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')

@app.route('/showlog')
def show_login_form():
    """show login form"""

    return render_template("login.html")


@app.route('/login')
def login_form():
    email = request.args.get("email")
    password = request.args.get("password")


    if db.session.query(User.email).filter(User.email == email).first():
        record= User.query.filter(User.email == email).first()
        # print("==>",record.user_id)
        session['user'] = record.user_id
        flash("logged in as %s" % record.user_id)
        return redirect('/')
    else:
        flash("wrong password")
        return redirect('/showlog')


# @app.route('/logoutform')
# def logout_form():
#     """display log out form"""

#     return render_template('logout.html')


@app.route('/logout')
def logout():
    """display log out form"""
    session.pop('user')
    flash("Logged Out")

    return redirect('/')


@app.route('/users/<user_id>')
def userInfo(user_id):
    """display user info"""
    # print("++++++>>>>>",user_id)
    user = User.query.get(user_id)
    age = user.age
    zipcode = user.zipcode

    # records = Ratings.query.filter(Ratings.user_id==user_id).all()
    # #movies = records.movie_title
    # movie_records = Movies.query.filter(Movies.movie_id == records.movie_id).all()
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>", movie_records)




    return render_template('user_info.html', user=user)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
