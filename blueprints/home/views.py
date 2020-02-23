from flask import Flask, Blueprint, render_template, url_for, redirect
from forms import TeamSearchForm
from models import TeamPit

import google_auth

home = Blueprint('home', __name__, template_folder="templates")

@home.route("/")
def index():
    if not google_auth.is_logged_in():
        return(redirect(url_for('google_auth.login')))

    """
    form = TeamSearchForm()

    teams = Team.query.all()
    
    # process scoring attributes
    for team in teams:
        team.score = []

        if team.score_lower:
            team.score.append("Lower")
        if team.score_outer:
            team.score.append("Outer")
        if team.score_inner:
            team.score.append("Inner")

        team.auto_score = []

        if team.auto_score_lower:
            team.score.append("Lower")
        if team.auto_score_outer:
            team.score.append("Outer")
        if team.auto_score_inner:
            team.score.append("Inner")
    """

    return(render_template('home/index.html'))