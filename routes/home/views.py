from flask import Blueprint, render_template

home = Blueprint('home', __name__)

@home.route('/')  # Route for the page
def home_page():
	return(render_template("home/home.html"))