"""Breadcrumbs: Tracking a user's restaurant history"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Restaurant, Visit, Category, City, RestaurantCategory, Image, Connection
from model import connect_to_db, db

import os

# from flask import jsonify
# Use simplejson which encodes JSON correctly and supports Decimal types
import simplejson as json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/login", methods=["POST"])
def login():
    """Check if user's email matches password to login, otherwise ask user to try again."""

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    return redirect("/")


@app.route("/signup")
def signup():
    """Check if user exists in database, otherwise add user to database."""

    return render_template("signup.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    # Query to get all users
    users = db.session.query(User).all()

    return render_template("user_list.html", users=users)


@app.route("/user-visits.json")
def user_restaurant_visits():
    """Return info about user's restaurant visits as JSON."""

    user_visits = db.session.query(Visit).filter(Visit.user_id == 1).all()

    rest_visits = {}

    for visit in user_visits:
        rest_visits[visit.visit_id] = {
            "restaurant": visit.restaurant.name,
            "address": visit.restaurant.address,
            "phone": visit.restaurant.phone,
            "image_url": visit.restaurant.image_url,
            # Need to convert latitude and longitude to strings or floats
            # Otherwise get a TypeError: Decimal is not JSON serializable
            # "latitude": float(visit.restaurant.latitude),
            # "longitude": float(visit.restaurant.longitude)
            # Use simplejson which encodes JSON correctly and supports Decimal types
            "latitude": visit.restaurant.latitude,
            "longitude": visit.restaurant.longitude
        }

    return json.dumps(rest_visits, use_decimal=True)
    # return jsonify(rest_visits)


@app.route("/users/<int:user_id>")
def user_profile(user_id):
    """Show user profile with map and list of visited restaurants."""

    # Query by user id to return that record in database about user info
    user = db.session.query(User).filter(User.user_id == user_id).one()

    return render_template("user_profile.html", user=user)


@app.route("/restaurants")
def restaurant_list():
    """Show list of restaurants."""

    # Query to get all restaurants, sorted alphabetically
    restaurants = db.session.query(Restaurant).order_by(Restaurant.name).all()

    return render_template("restaurant_list.html", restaurants=restaurants)


@app.route("/restaurants/<int:restaurant_id>")
def restaurant_profile(restaurant_id):
    """Show restaurant information."""

    # Query by restaurant id to return the record from the database and access its attributes
    restaurant = db.session.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).one()

    return render_template("restaurant_profile.html", restaurant=restaurant)


@app.route("/restaurants/search")
def search_restaurants():
    """Search for a restaurant."""

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
