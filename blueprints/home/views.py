from flask import Flask, Blueprint, render_template, url_for, redirect
from forms import TeamSearchForm
from models import PitReport, User
from app import db

import google_auth

home = Blueprint('home', __name__, template_folder="templates")

@home.route("/")
def index():
    if not google_auth.is_logged_in():
        return(redirect(url_for('google_auth.login')))

    # check if in db already, if not make entry
    user_info = google_auth.get_user_info()
    user = User.query.filter(User.user_id==user_info["id"]).first()
    
    if not user:
        user = User()
        user.user_id = user_info["id"]
        user.first_name = user_info["given_name"]
        user.last_name = user_info["family_name"]

        db.session.add(user)
        db.session.commit()

    """
    form = TeamSearchForm()

    teams = Team.query.all()
    
    # process scoring attributes
    for team in teams:
        team.score = []

        if team.score_bottom:
            team.score.append("Bottom")
        if team.score_outer:
            team.score.append("Outer")
        if team.score_inner:
            team.score.append("Inner")

        team.auto_score = []

        if team.auto_score_bottom:
            team.score.append("Bottom")
        if team.auto_score_outer:
            team.score.append("Outer")
        if team.auto_score_inner:
            team.score.append("Inner")
    """

    return(render_template('home/index.html'))