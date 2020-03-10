from flask import Flask, Blueprint, render_template, url_for, redirect, request
from forms import TeamForm, TeamSearchForm
from models import Match, MatchReport, Bookmark, PitReport, AllianceSuggestion, TeamStats, Team, TeamPhoto
from app import db

import os
import requests
import google_auth

team = Blueprint("team", __name__, template_folder="templates")

TBA_AUTH_KEY = os.environ.get("TBA_AUTH_KEY", default=False)

@team.route("/search", methods=["POST"])
def search():
    # check if logged in w/ google
    if not google_auth.is_logged_in():
        return(redirect(url_for("google_auth.login")))

    form = TeamSearchForm(request.form)

    # if POST request, validate form and redirect to info route w/ team #
    if form.validate():
        team_number = form.team_number.data
        
        return(redirect(url_for("team.profile", team_number=team_number)))

@team.route("/profile/<int:team_number>")
def profile(team_number):
    # check if logged in w/ google
    if not google_auth.is_logged_in():
        return(redirect(url_for("google_auth.login")))
    
    form = TeamSearchForm()

    # get team
    team = Team.query.filter_by(team_number=team_number).first()

    # get bookmark
    bookmark = Bookmark.query.filter(Bookmark.team_number == team_number).first()

    # get team info from TBA API
    response = requests.get(f"https://www.thebluealliance.com/api/v3/team/frc{team_number}", headers={"X-TBA-Auth-Key": TBA_AUTH_KEY})
    team_info = response.json()

    # get events from TBA API
    response = requests.get(f"https://www.thebluealliance.com/api/v3/team/frc{team_number}/events/2020", headers={"X-TBA-Auth-Key": TBA_AUTH_KEY})
    events = response.json()

    # get event statuses from TBA API
    response = requests.get(f"https://www.thebluealliance.com/api/v3/team/frc{team_number}/events/2020/statuses", headers={"X-TBA-Auth-Key": TBA_AUTH_KEY})
    event_statuses = response.json()

    # get OPRs (OPR, DPR, CCWM) from TBA API
    oprs = {}

    for event in event_statuses:
        response = requests.get(f"https://www.thebluealliance.com/api/v3/event/{event}/oprs", headers={"X-TBA-Auth-Key": TBA_AUTH_KEY})
        response = response.json()

        oprs[event] = response

    # get district from TBA API
    response = requests.get(f"https://www.thebluealliance.com/api/v3/team/frc{team_number}/districts", headers={"X-TBA-Auth-Key": TBA_AUTH_KEY})
    response = response.json()
    if response:
        district = response[len(response) - 1]
    else:
        district = None

    # get district ranking from TBA API
    if district:
        response = requests.get(f"https://www.thebluealliance.com/api/v3/district/{district.get('key')}/rankings", headers={"X-TBA-Auth-Key": TBA_AUTH_KEY})
        response = response.json()
        district_ranking = list(filter(lambda x:x["team_key"]==f"frc{team_number}", response))
    else:
        district_ranking = None

    if team:
        # get alliance suggestion 1st pick
        alliance_suggestion_1 = AllianceSuggestion.query.filter(AllianceSuggestion.team_id == team.id, AllianceSuggestion.pick_number == 1).first()

        # get alliance suggestion 2nd pick
        alliance_suggestion_2 = AllianceSuggestion.query.filter(AllianceSuggestion.team_id == team.id, AllianceSuggestion.pick_number == 2).first()

        match_reports = MatchReport.query.filter_by(team_id=team.id).join(Match).all()
        team_stats = TeamStats.query.filter_by(team_id=team.id).first()
        pit_reports = PitReport.query.filter_by(team_id=team.id).all()
        team_photos = TeamPhoto.query.filter_by(team_id=team.id).all()
    else:
        alliance_suggestion_1 = None
        alliance_suggestion_2 = None
        match_reports = None
        team_stats = None
        pit_reports = None
        team_photos = None

    return(render_template("team/profile.html", team_number=team_number,
                           match_reports=match_reports, team_stats=team_stats, team_photos=team_photos,
                           pit_reports=pit_reports, team_info=team_info, event_statuses=event_statuses, form=form,
                           bookmark=bookmark, events=events, district=district, district_ranking=district_ranking, oprs=oprs, alliance_suggestion_1=alliance_suggestion_1, alliance_suggestion_2=alliance_suggestion_2))

"""
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
        team.score_bottom = form.score_bottom.data
        team.score_outer = form.score_bottom.data
        team.score_inner = form.score_inner.data
        team.control_panel = form.control_panel.data
        team.auto_move = form.auto_move.data
        team.auto_score_bottom = form.auto_score_bottom.data
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

    # get team info from db
    team = Team.query.filter_by(team_number=team_number).first()

    # if POST request, validate form and edit db entry
    if request.method == "POST" and form.validate():
        team.team_number = form.team_number.data
        team.hang = form.hang.data
        team.balanced = form.balanced.data
        team.score_bottom = form.score_bottom.data
        team.score_outer = form.score_bottom.data
        team.score_inner = form.score_inner.data
        team.control_panel = form.control_panel.data
        team.auto_move = form.auto_move.data
        team.auto_score_bottom = form.auto_score_bottom.data
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
"""