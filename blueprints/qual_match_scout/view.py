from flask import Flask, Blueprint, render_template, url_for, redirect, request
from forms import MatchReportForm
from models import MatchReport
from app import db

import os
import requests
import google_auth

qual_match_scout = Blueprint("qual_match_scout", __name__, template_folder="templates")

@qual_match_scout.route("/")
def all_matches():
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))
  
  match_reports = MatchReport.query.all()
  print(match_reports)

  return(render_template("qual_match_scout/all_matches.html", match_reports=match_reports))

@qual_match_scout.route("/match/<int:match_number>", methods=["GET", "POST"])
def match(match_number):

  match_reports = MatchReport.query.filter_by(match=match_number).all()

  return(render_template("qual_match_scout/match.html", match_reports=match_reports))

@qual_match_scout.route("/add_match_report", methods=["GET","POST"])
def add_match_report():
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  form = MatchReportForm(request.form)

  if request.method == "POST" and form.validate():
    user_info = google_auth.get_user_info()

    team = MatchReport(
      # metadata
      team_number = form.team_number.data,
      match = form.match.data,
      alliance = form.alliance.data,
      station = form.station.data,
      created_by = user_info['id'],
      
      # auto
      auto_move = form.auto_move.data,
      auto_score_lower = form.auto_score_lower.data,
      auto_score_upper = form.auto_score_upper.data,
      auto_collect_balls = form.auto_collect_balls.data,
      
      # teleop
      teleop_score_lower = form.teleop_score_lower.data,
      teleop_score_upper = form.teleop_score_upper.data,
      teleop_attempts = form.teleop_attempts.data,
      
      # control panel
      control_panel_rotation = form.control_panel_rotation.data,
      control_panel_position = form.control_panel_position.data,

      # hang
      hang_able = form.hang_able.data,
      hang_level = form.hang_level.data,
      hang_position = form.hang_position.data,
      hang_active = form.hang_active.data,
      
      # defense
      defense_performance = form.defense_performance.data,
      defense_penalties = form.defense_penalities.data,
      
      # comms
      connection_issues = form.connection_issues.data,
      brownouts = form.brownouts.data,
      emergency_stop = form.emergency_stop.data,
      
      #notes
      notes = form.notes.data
    )
    
    # calculate points and statistics
    team.auto_points = ((form.auto_score_lower.data * 2) + (form.auto_score_upper.data * 4))
    if team.auto_move == True:
      team.auto_points += 5
    team.teleop_points = ((form.teleop_score_lower.data) + (form.teleop_score_upper.data * 2))
    team.telop_success_rate = ((form.teleop_score_lower.data + form.teleop_score_upper.data)/(form.teleop_attempts.data))

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

    db.session.add(team)
    db.session.commit()

    return(redirect(url_for("qual_match_scout.add_match_report")))

  return(render_template("qual_match_scout/add_match_report.html", form=form))