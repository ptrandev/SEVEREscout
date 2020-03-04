from flask import Flask, Blueprint, render_template, url_for, redirect, request
from forms import MatchReportForm, TeamSearchForm
from models import MatchReport, Match
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

    team = MatchReport()

    # metadata
    team.team_number = form.team_number.data
    team.alliance = form.alliance.data
    team.station = form.station.data
    team.created_by = user_info["id"]

    # auto
    team.auto_move = form.auto_move.data
    team.auto_score_bottom = form.auto_score_bottom.data
    team.auto_score_upper = form.auto_score_upper.data
    team.auto_collect_balls = form.auto_collect_balls.data

    # teleop
    team.teleop_score_bottom = form.teleop_score_bottom.data
    team.teleop_score_upper = form.teleop_score_upper.data
    team.teleop_attempts = form.teleop_attempts.data

    # control panel
    team.control_panel_rotation = form.control_panel_rotation.data
    team.control_panel_position = form.control_panel_position.data

    # hang
    team.hang_able = form.hang_able.data
    team.hang_level = form.hang_level.data
    team.hang_position = form.hang_position.data
    team.hang_active = form.hang_active.data

    # defense
    team.defense_performance = form.defense_performance.data
    team.defense_penalties = form.defense_penalities.data

    # comms
    team.connection_issues = form.connection_issues.data
    team.brownouts = form.brownouts.data
    team.emergency_stop = form.emergency_stop.data

    #notes
    team.notes = form.notes.data

    # calculate points and statistics
    team.auto_points = ((form.auto_score_bottom.data * 2) + (form.auto_score_upper.data * 4))
    if team.auto_move == True:
      team.auto_points += 5
    team.teleop_points = ((form.teleop_score_bottom.data) + (form.teleop_score_upper.data * 2))
    team.teleop_success_rate = float((form.teleop_score_bottom.data + form.teleop_score_upper.data) / (form.teleop_attempts.data))

    team.control_panel_points = 0
    if team.control_panel_rotation == True:
      team.control_panel_points += 10
    if team.control_panel_position == True:
      team.control_panel_points += 20

    team.hang_points = 0
    if team.hang_able == True:
      team.hang_points += 25
    if team.hang_level == True:
      team.hang_points += 15

    match = Match.query.filter_by(match=form.match.data).first()
    
    if not match:
      match = Match()
      match.match = form.match.data
      match.event = form.event.data

    match.match_reports.append(team)

    db.session.add(match)
    db.session.add(team)
    db.session.commit()

    return(redirect(url_for("match_scout.add_match_report")))

  return(render_template("match_scout/add_match_report.html", form=form, team_number=team_number))

@match_scout.route("/edit_match_report/<int:match_report_id>", methods=["GET","POST"])
def edit_match_report(match_report_id):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  # get match report info from db
  match_report = MatchReport.query.filter(MatchReport.id == match_report_id).join(Match).first()

  form = MatchReportForm(request.form)

  if request.method == "POST" and form.validate():
    user_info = google_auth.get_user_info()

    # metadata
    match_report.team_number = form.team_number.data
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

    db.session.commit()

    return(redirect(url_for("match_scout.add_match_report")))
  else:
    # metadata
    form.team_number.data = match_report.team_number
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