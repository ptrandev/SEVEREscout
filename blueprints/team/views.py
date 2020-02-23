from flask import Flask, Blueprint, render_template, url_for, redirect, request
from forms import TeamForm, TeamSearchForm
from models import TeamPit
from app import db

import os
import requests
import google_auth

team = Blueprint("team", __name__, template_folder="templates")

TBA_AUTH_KEY = os.environ.get("TBA_AUTH_KEY", default=False)

@team.route("/team/search", methods=["POST"])
def search():
    # check if logged in w/ google
    if not google_auth.is_logged_in():
        return(redirect(url_for("google_auth.login")))

    form = TeamSearchForm(request.form)

    # if POST request, validate form and redirect to info route w/ team #
    if form.validate():
        team_number = form.team_number.data
        
        return(redirect(url_for("team.info", team_number=team_number)))

@team.route("/team/<int:team_number>")
def info(team_number):
    # check if logged in w/ google
    if not google_auth.is_logged_in():
        return(redirect(url_for("google_auth.login")))

    # get team info from TBA API
    response = requests.get(f"https://www.thebluealliance.com/api/v3/team/frc{team_number}",
                            headers={"X-TBA-Auth-Key": TBA_AUTH_KEY})
    tba_data = response.json()

    # get team info from db
    db_data = Team.query.filter_by(team_number=team_number).first()

    return(render_template("team/info.html", tba_data=tba_data, db_data=db_data,
                           team_number=team_number))


@team.route("/team/add", defaults={"team_number": None}, methods=["GET", "POST"])
@team.route("/team/add/<int:team_number>", methods=["GET", "POST"])
def add(team_number):
    # check if logged in w/ google
    if not google_auth.is_logged_in():
        return(redirect(url_for("google_auth.login")))

    form = TeamForm(request.form)

    # if POST request, validate form and create db entry
    if request.method == "POST" and form.validate():
        team = Team()

        team.team_number = form.team_number.data
        team.hang = form.hang.data
        team.balanced = form.balanced.data
        team.score_lower = form.score_lower.data
        team.score_outer = form.score_lower.data
        team.score_inner = form.score_inner.data
        team.control_panel = form.control_panel.data
        team.auto_move = form.auto_move.data
        team.auto_score_lower = form.auto_score_lower.data
        team.auto_score_outer = form.auto_score_outer.data
        team.auto_score_inner = form.auto_score_inner.data
        team.drivetrain = form.drivetrain.data
        team.notes = form.notes.data
        team.weight = form.weight.data

        db.session.add(team)
        db.session.commit()

        return(redirect(url_for("home.index")))

    return(render_template("team/add.html", form=form, team_number=team_number))

@team.route("/team/edit/<int:team_number>", methods=["GET", "POST"])
def edit(team_number):
     # check if logged in w/ google
    if not google_auth.is_logged_in():
        return(redirect(url_for("google_auth.login")))

    form = TeamForm(request.form)

    # get team info from fb
    team = Team.query.filter_by(team_number=team_number).first()

    # if POST request, validate form and edit db entry
    if request.method == "POST" and form.validate():
        team.team_number = form.team_number.data
        team.hang = form.hang.data
        team.balanced = form.balanced.data
        team.score_lower = form.score_lower.data
        team.score_outer = form.score_lower.data
        team.score_inner = form.score_inner.data
        team.control_panel = form.control_panel.data
        team.auto_move = form.auto_move.data
        team.auto_score_lower = form.auto_score_lower.data
        team.auto_score_outer = form.auto_score_outer.data
        team.auto_score_inner = form.auto_score_inner.data
        team.drivetrain = form.drivetrain.data
        team.notes = form.notes.data
        team.weight = form.weight.data
        
        db.session.commit()

        return(redirect(url_for("home.index")))

    # prepopulate notes
    form.notes.data = team.notes

    return(render_template("team/edit.html", form=form, team=team,
                           team_number=team_number))