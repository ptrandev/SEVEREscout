from flask import Flask, Blueprint, render_template, url_for, redirect, request
from forms import TeamForm, TeamSearchForm
from models import Match, MatchReport, Bookmark, PitReport
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

    # get bookmark
    bookmark = Bookmark.query.filter(Bookmark.team_number == team_number).first()

    # get team info from TBA API
    response = requests.get(f"https://www.thebluealliance.com/api/v3/team/frc{team_number}", headers={"X-TBA-Auth-Key": TBA_AUTH_KEY})
    team = response.json()

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
    print(response)
    district = response[len(response) - 1]
    
    print(district)

    # get district ranking from TBA API
    response = requests.get(f"https://www.thebluealliance.com/api/v3/district/{district.get('key')}/rankings", headers={"X-TBA-Auth-Key": TBA_AUTH_KEY})
    response = response.json()
    district_ranking = list(filter(lambda x:x["team_key"]==f"frc{team_number}", response))

    # get match info
    match_reports = MatchReport.query.filter_by(team_number=team_number).join(Match).all()

    if match_reports:
        num_match_reports = MatchReport.query.filter_by(team_number=team_number).count()
        # generate match statistics
        class TeamStatistics:
            auto_points = 0
            auto_points_avg = 0
            teleop_points = 0
            teleop_points_avg = 0
            teleop_score_bottom = 0
            teleop_score_bottom_avg = 0
            teleop_score_upper = 0
            teleop_score_upper_avg = 0
            teleop_successful_attempts = 0
            teleop_attempts = 0
            teleop_success_rate = 0
            control_panel_points = 0
            control_panel_points_avg = 0
            hang_points = 0
            hang_points_avg = 0
            defense_penalties = 0
            connection_issues = 0
            brownouts = 0
            emergency_stops = 0
            num_matches = 0

        team_statistics = TeamStatistics()

        team_statistics.num_matches = num_match_reports

        for match_report in match_reports:
            team_statistics.auto_points += match_report.auto_points
            team_statistics.teleop_points += match_report.teleop_points
            team_statistics.teleop_score_bottom += match_report.teleop_score_bottom
            team_statistics.teleop_score_upper += match_report.teleop_score_upper
            team_statistics.teleop_successful_attempts += (match_report.teleop_score_bottom + match_report.teleop_score_upper)
            team_statistics.teleop_attempts += match_report.teleop_attempts
            team_statistics.control_panel_points += match_report.control_panel_points
            team_statistics.hang_points += match_report.hang_points
            team_statistics.defense_penalties += match_report.defense_penalties

            if match_report.connection_issues == True:
                team_statistics.connection_issues +=  1
            if match_report.brownouts == True:
                team_statistics.brownouts += 1
            if match_report.emergency_stop == True:
                team_statistics.emergency_stops += 1

        team_statistics.teleop_success_rate = round(team_statistics.teleop_successful_attempts / team_statistics.teleop_attempts, 4)
        team_statistics.auto_points_avg = round(team_statistics.auto_points / team_statistics.num_matches, 2)
        team_statistics.teleop_points_avg = round(team_statistics.teleop_points / team_statistics.num_matches, 2)
        team_statistics.teleop_score_bottom_avg = round(team_statistics.teleop_score_bottom / team_statistics.num_matches, 2)
        team_statistics.teleop_score_upper_avg = round(team_statistics.teleop_score_upper / team_statistics.num_matches, 2)
        team_statistics.hang_points_avg = round(team_statistics.hang_points / team_statistics.num_matches, 2)
        team_statistics.control_panel_points_avg = round(team_statistics.control_panel_points / team_statistics.num_matches, 2)
    else:
        team_statistics = None

    # get pit reports
    pit_reports = PitReport.query.filter_by(team_number=team_number).all()

    return(render_template("team/profile.html", team_number=team_number,
                           match_reports=match_reports, team_statistics=team_statistics,
                           pit_reports=pit_reports, team=team, event_statuses=event_statuses, form=form,
                           bookmark=bookmark, events=events, district=district, district_ranking=district_ranking, oprs=oprs))

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