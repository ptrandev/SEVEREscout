from flask import Flask, Blueprint, render_template, url_for, redirect, request
from forms import MatchReportForm, TeamSearchForm
from models import MatchReport, Match, Team, TeamStats
from app import db

import os
import requests
import google_auth

match_scout = Blueprint("match_scout", __name__, template_folder="templates")

@match_scout.route("/")
def all_matches():
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  form = TeamSearchForm()
  matches = Match.query.order_by(Match.match).join(MatchReport).all()

  return(render_template("match_scout/all_matches.html", matches=matches, form=form))

@match_scout.route("/match/<int:match_number>", methods=["GET", "POST"])
def match(match_number):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  form = TeamSearchForm()
  match = Match.query.filter_by(match=match_number).join(MatchReport).first()

  return(render_template("match_scout/match.html", match=match, form=form))

@match_scout.route("/add_match_report", defaults={"team_number": None}, methods=["GET", "POST"])
@match_scout.route("/add_match_report/<int:team_number>", methods=["GET","POST"])
def add_match_report(team_number):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  form = MatchReportForm(request.form)

  if request.method == "POST" and form.validate():
    user_info = google_auth.get_user_info()

    match_report = MatchReport()

    # metadata
    match_report.alliance = form.alliance.data
    match_report.station = form.station.data
    match_report.created_by = user_info["id"]

    # auto
    match_report.auto_move = form.auto_move.data
    match_report.auto_score_bottom = form.auto_score_bottom.data
    match_report.auto_score_upper = form.auto_score_upper.data
    match_report.auto_collect_balls = form.auto_collect_balls.data

    # teleop
    match_report.teleop_score_bottom = form.teleop_score_bottom.data
    match_report.teleop_score_upper = form.teleop_score_upper.data
    match_report.teleop_attempts = form.teleop_attempts.data

    # control panel
    match_report.control_panel_rotation = form.control_panel_rotation.data
    match_report.control_panel_position = form.control_panel_position.data

    # hang
    match_report.hang_able = form.hang_able.data
    match_report.hang_level = form.hang_level.data
    match_report.hang_position = form.hang_position.data
    match_report.hang_active = form.hang_active.data

    # defense
    match_report.defense_performance = form.defense_performance.data
    match_report.defense_penalties = form.defense_penalities.data

    # comms
    match_report.connection_issues = form.connection_issues.data
    match_report.brownouts = form.brownouts.data
    match_report.emergency_stop = form.emergency_stop.data

    #notes
    match_report.notes = form.notes.data

    # calculate points and statistics
    match_report.auto_points = ((form.auto_score_bottom.data * 2) + (form.auto_score_upper.data * 4))
    if match_report.auto_move == True:
      match_report.auto_points += 5
    match_report.teleop_points = ((form.teleop_score_bottom.data) + (form.teleop_score_upper.data * 2))

    if form.teleop_attempts.data == 0:
      match_report.teleop_success_rate = 0.0
    else:
      match_report.teleop_success_rate = float((form.teleop_score_bottom.data + form.teleop_score_upper.data) / (form.teleop_attempts.data))

    match_report.control_panel_points = 0
    if match_report.control_panel_rotation == True:
      match_report.control_panel_points += 10
    if match_report.control_panel_position == True:
      match_report.control_panel_points += 20

    match_report.hang_points = 0
    if match_report.hang_able == True:
      match_report.hang_points += 25
    if match_report.hang_level == True:
      match_report.hang_points += 15

    # find team from form
    team = Team.query.filter_by(team_number=form.team_number.data).first()

    # if team doesn't exist, make it
    if not team:
      team = Team()
      team.team_number = form.team_number.data

    # add match report to team
    team.match_reports.append(match_report)

    match = Match.query.filter(Match.match==form.match.data).first()

    if not match:
      match = Match()
      match.match = form.match.data
      match.event = form.event.data

    match_report.match_id = match.id

    db.session.add(team)
    db.session.add(match_report)
    db.session.commit()

    generateTeamStats(form.team_number.data)

    return(redirect(url_for("match_scout.add_match_report")))

  return(render_template("match_scout/add_match_report.html", form=form, team_number=team_number))

@match_scout.route("/edit_match_report/<int:match_report_id>", methods=["GET", "POST"])
def edit_match_report(match_report_id):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  # get match report info, find associated team
  match_report = MatchReport.query.filter(MatchReport.id == match_report_id).join(Match).first()
  team = Team.query.filter_by(id=match_report.team_id).first()

  form = MatchReportForm(request.form)

  if request.method == "POST" and form.validate():
    user_info = google_auth.get_user_info()

    # metadata
    match_report.alliance = form.alliance.data
    match_report.station = form.station.data
    match_report.created_by = user_info["id"]

    # auto
    match_report.auto_move = form.auto_move.data
    match_report.auto_score_bottom = form.auto_score_bottom.data
    match_report.auto_score_upper = form.auto_score_upper.data
    match_report.auto_collect_balls = form.auto_collect_balls.data

    # teleop
    match_report.teleop_score_bottom = form.teleop_score_bottom.data
    match_report.teleop_score_upper = form.teleop_score_upper.data
    match_report.teleop_attempts = form.teleop_attempts.data

    # control panel
    match_report.control_panel_rotation = form.control_panel_rotation.data
    match_report.control_panel_position = form.control_panel_position.data

    # hang
    match_report.hang_able = form.hang_able.data
    match_report.hang_level = form.hang_level.data
    match_report.hang_position = form.hang_position.data
    match_report.hang_active = form.hang_active.data

    # defense
    match_report.defense_performance = form.defense_performance.data
    match_report.defense_penalties = form.defense_penalities.data

    # comms
    match_report.connection_issues = form.connection_issues.data
    match_report.brownouts = form.brownouts.data
    match_report.emergency_stop = form.emergency_stop.data

    #notes
    match_report.notes = form.notes.data

    # calculate points and statistics
    match_report.auto_points = ((form.auto_score_bottom.data * 2) + (form.auto_score_upper.data * 4))
    if match_report.auto_move == True:
      match_report.auto_points += 5
    match_report.teleop_points = ((form.teleop_score_bottom.data) + (form.teleop_score_upper.data * 2))

    if form.teleop_attempts.data == 0:
      match_report.teleop_success_rate = 0.0
    else:
      match_report.teleop_success_rate = float((form.teleop_score_bottom.data + form.teleop_score_upper.data) / (form.teleop_attempts.data))

    match_report.control_panel_points = 0
    if match_report.control_panel_rotation == True:
      match_report.control_panel_points += 10
    if match_report.control_panel_position == True:
      match_report.control_panel_points += 20

    match_report.hang_points = 0
    if match_report.hang_able == True:
      match_report.hang_points += 25
    if match_report.hang_level == True:
      match_report.hang_points += 15

    # find team from form
    team = Team.query.filter_by(team_number=form.team_number.data).first()

    # if team doesn't exist, make it
    if not team:
      team = Team(
        team_number = form.team_number.data
      )

    # add match report to team
    team.pit_reports.append(match_report)

    db.session.add(team)
    db.session.commit()

    generateTeamStats(form.team_number.data)

    return(redirect(url_for("match_scout.add_match_report")))
  else:
    # metadata
    form.team_number.data = team.team_number
    form.match.data = match_report.match.match
    form.alliance.data = match_report.alliance
    form.station.data = match_report.station

    # auto
    form.auto_move.data = match_report.auto_move
    form.auto_collect_balls.data = match_report.auto_collect_balls
    form.auto_score_bottom.data = match_report.auto_score_bottom
    form.auto_score_upper.data = match_report.auto_score_upper

    # teleop
    form.teleop_score_bottom.data = match_report.teleop_score_bottom
    form.teleop_score_upper.data = match_report.teleop_score_upper
    form.teleop_attempts.data = match_report.teleop_attempts

    # control panel
    form.control_panel_rotation.data = match_report.control_panel_rotation
    form.control_panel_position.data = match_report.control_panel_position

    # defense
    form.defense_performance.data = match_report.defense_performance
    form.defense_penalities.data = match_report.defense_penalties

    # hang
    form.hang_able.data = match_report.hang_able
    form.hang_level.data = match_report.hang_level
    form.hang_active.data = match_report.hang_active
    form.hang_position.data = match_report.hang_position
    
    # comms
    form.emergency_stop.data = match_report.emergency_stop
    form.connection_issues.data = match_report.connection_issues
    form.brownouts.data = match_report.brownouts
    
    # notes
    form.notes.data = match_report.notes

  return(render_template("match_scout/edit_match_report.html", form=form, match_report=match_report))

@match_scout.route("/delete_match_report/<int:match_report_id>", methods=["POST"])
def delete_match_report(match_report_id):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  # get match report info from db
  match_report = MatchReport.query.filter(MatchReport.id == match_report_id).join(Match).first()
  
  db.session.delete(match_report)
  db.session.commit()
  
  return(redirect(url_for("match_scout.all_matches")))

def generateTeamStats(team_number):
  team = Team.query.filter_by(team_number=team_number).first()
  match_reports = MatchReport.query.filter(MatchReport.team_id==team.id).all()

  if match_reports:
    team = Team.query.filter(Team.team_number==team_number).first()
    
    if not team:
      team = Team()
      team.team_number = team_number
      db.session.add(team)
      db.session.commit()
    
    team_stats = TeamStats.query.filter(TeamStats.team_id==team.id).first()
    
    if team_stats:
      team_stats.team_id = team.id
      team_stats.auto_points = 0
      team_stats.auto_points_avg = 0
      team_stats.teleop_points = 0
      team_stats.teleop_points_avg = 0
      team_stats.teleop_score_bottom = 0
      team_stats.teleop_score_bottom_avg = 0
      team_stats.teleop_score_upper = 0
      team_stats.teleop_score_upper_avg = 0
      team_stats.teleop_successful_attempts = 0
      team_stats.teleop_attempts = 0
      team_stats.teleop_success_rate = 0
      team_stats.control_panel_points = 0
      team_stats.control_panel_points_avg = 0
      team_stats.hang_points = 0
      team_stats.hang_points_avg = 0
      team_stats.hang_able = 0
      team_stats.hang_success_rate = 0
      team_stats.defense_penalties = 0
      team_stats.defense_penalties_avg = 0
      team_stats.connection_issues = 0
      team_stats.connection_issues_avg = 0
      team_stats.brownouts = 0
      team_stats.brownouts_avg = 0
      team_stats.emergency_stops = 0
      team_stats.emergency_stops_avg = 0
      team_stats.num_matches = 0

      already_exists = True
    else:
      team_stats = TeamStats(
        team_id = team.id,
        auto_points = 0,
        auto_points_avg = 0,
        teleop_points = 0,
        teleop_points_avg = 0,
        teleop_score_bottom = 0,
        teleop_score_bottom_avg = 0,
        teleop_score_upper = 0,
        teleop_score_upper_avg = 0,
        teleop_successful_attempts = 0,
        teleop_attempts = 0,
        teleop_success_rate = 0,
        control_panel_points = 0,
        control_panel_points_avg = 0,
        hang_points = 0,
        hang_points_avg = 0,
        hang_able = 0,
        hang_success_rate = 0,
        defense_penalties = 0,
        defense_penalties_avg = 0,
        connection_issues = 0,
        connection_issues_avg = 0,
        brownouts = 0,
        brownouts_avg = 0,
        emergency_stops = 0,
        emergency_stops_avg = 0,
        num_matches = 0
      )

      already_exists = False

    num_match_reports = MatchReport.query.filter_by(team_id=team.id).count()

    team_stats.num_matches = num_match_reports

    for match_report in match_reports:
      team_stats.auto_points += match_report.auto_points
      team_stats.teleop_points += match_report.teleop_points
      team_stats.teleop_score_bottom += match_report.teleop_score_bottom
      team_stats.teleop_score_upper += match_report.teleop_score_upper
      team_stats.teleop_successful_attempts += (match_report.teleop_score_bottom + match_report.teleop_score_upper)
      team_stats.teleop_attempts += match_report.teleop_attempts
      team_stats.control_panel_points += match_report.control_panel_points
      team_stats.hang_points += match_report.hang_points
      team_stats.defense_penalties += match_report.defense_penalties

      if match_report.hang_able == True:
          team_stats.hang_able += 1
      if match_report.connection_issues == True:
          team_stats.connection_issues +=  1
      if match_report.brownouts == True:
          team_stats.brownouts += 1
      if match_report.emergency_stop == True:
          team_stats.emergency_stops += 1

    if team_stats.teleop_attempts == 0:
      team_stats.teleop_success_rate = 0.0
    else:
      team_stats.teleop_success_rate = round(team_stats.teleop_successful_attempts / team_stats.teleop_attempts, 4)
    team_stats.auto_points_avg = round(team_stats.auto_points / team_stats.num_matches, 4)
    team_stats.teleop_points_avg = round(team_stats.teleop_points / team_stats.num_matches, 4)
    team_stats.teleop_score_bottom_avg = round(team_stats.teleop_score_bottom / team_stats.num_matches, 4)
    team_stats.teleop_score_upper_avg = round(team_stats.teleop_score_upper / team_stats.num_matches, 4)
    team_stats.hang_points_avg = round(team_stats.hang_points / team_stats.num_matches, 4)
    team_stats.hang_success_rate = round(team_stats.hang_able / team_stats.num_matches, 4)
    team_stats.control_panel_points_avg = round(team_stats.control_panel_points / team_stats.num_matches, 4)
    team_stats.defense_penalties_avg = round(team_stats.defense_penalties / team_stats.num_matches, 4)
    team_stats.connection_issues_avg = round(team_stats.connection_issues / team_stats.num_matches, 4)
    team_stats.brownouts_avg = round(team_stats.brownouts / team_stats.num_matches, 4)
    team_stats.emergency_stops_avg = round(team_stats.emergency_stops / team_stats.num_matches, 4)

    if not already_exists:
      db.session.add(team_stats)

    db.session.commit()