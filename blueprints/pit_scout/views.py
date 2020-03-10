from flask import Flask, Blueprint, render_template, url_for, redirect, request
from forms import PitReportForm, PitPhotosForm, TeamSearchForm
from models import PitReport, Team
from app import db
from werkzeug.utils import secure_filename
from pathlib import Path
import json

import os
import requests
import google_auth

pit_scout = Blueprint("pit_scout", __name__, template_folder="templates")

@pit_scout.route("/")
def all_reports():
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  form = TeamSearchForm()

  teams = Team.query.order_by(Team.team_number).join(PitReport).all()
  return(render_template("pit_scout/all_reports.html", teams=teams, form=form))

@pit_scout.route("/pit_report/<int:team_number>")
def pit_report(team_number):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  form = TeamSearchForm()

  team = Team.query.filter_by(team_number=team_number).first()

  pit_reports = PitReport.query.filter_by(team_id=team.id).all()

  return(render_template("pit_scout/pit_report.html", pit_reports=pit_reports, team_number=team_number, form=form))

@pit_scout.route("/add_pit_report", defaults={"team_number": None},
                 methods=["GET", "POST"])
@pit_scout.route("/add_pit_report/<int:team_number>", methods=["GET", "POST"])
def add_pit_report(team_number):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  form = PitReportForm(request.form)

  if request.method == "POST" and form.validate():
    user_info = google_auth.get_user_info()

    pit_report = PitReport()

    # metadata
    pit_report.event = form.event.data
    pit_report.created_by = user_info["id"]

    # drivetrain
    pit_report.drivetrain_type = form.drivetrain_type.data
    if form.drivetrain_type_other.data:
      pit_report.drivetrain_type_other = form.drivetrain_type_other.data

    pit_report.wheel_type = form.wheel_type.data
    if form.wheel_type_other.data:
      pit_report.wheel_type_other = form.wheel_type_other.data
    pit_report.wheel_number = form.wheel_number.data

    pit_report.motor_type = form.motor_type.data
    if form.motor_type_other.data:
      pit_report.motor_type_other = form.motor_type_other.data

    pit_report.motor_type = form.motor_type.data
    pit_report.motor_number = form.motor_number.data

    pit_report.drivetrain_notes = form.drivetrain_notes.data

    # physical characteristics
    if form.weight_unit.data == "Kilograms":
      pit_report.weight = form.weight.data * 2.20462
    else:
      pit_report.weight = form.weight.data
    
    if form.dimensions_unit.data == "Centimeters":
      pit_report.height = form.height.data * 0.393701
      pit_report.width = form.height.data * 0.393701
      pit_report.length = form.length.data * 0.393701
    else:
      pit_report.height = form.height.data
      pit_report.width = form.height.data
      pit_report.length = form.length.data
    
    if form.speed_unit.data == "Meters Per Second":
      pit_report.speed_unit = form.speed_unit.data * 3.28084
    else:
      pit_report.speed_unit = form.speed_unit.data

    # auto
    pit_report.auto_move = form.auto_move.data
    pit_report.auto_collect_balls = form.auto_collect_balls.data
    pit_report.auto_score_bottom = form.auto_score_bottom.data
    pit_report.auto_score_outer = form.auto_score_outer.data
    pit_report.auto_score_inner = form.auto_score_inner.data
    if form.auto_consistency.data:
      pit_report.auto_consistency = form.auto_consistency.data
    pit_report.auto_prefered_position = list(map(str, form.auto_prefered_position.data))
    
    print(pit_report.auto_prefered_position)

    # teleop
    pit_report.teleop_score_bottom = form.teleop_score_bottom.data
    pit_report.teleop_score_outer = form.teleop_score_outer.data
    pit_report.teleop_score_inner = form.teleop_score_inner.data
    if form.teleop_consistency.data:
      pit_report.teleop_consistency = form.teleop_consistency.data
    if form.teleop_ball_capacity.data:
      pit_report.teleop_ball_capacity = form.teleop_ball_capacity.data
    pit_report.teleop_prefered_position = form.teleop_prefered_position.data

    # control
    pit_report.control_panel_rotation = form.control_panel_rotation.data
    pit_report.control_panel_position = form.control_panel_position.data

    # hang
    pit_report.hang_able = form.hang_able.data
    pit_report.hang_level = form.hang_level.data
    pit_report.hang_prefered_position = form.hang_prefered_position.data
    if form.hang_consistency.data:
      pit_report.hang_consistency = form.hang_consistency.data
    pit_report.hang_time = form.hang_time.data
    pit_report.hang_active = form.hang_active.data

    # personnel
    if form.personnel_honesty.data:
      pit_report.personnel_honesty = form.personnel_honesty.data
    if form.personnel_answering.data:
      pit_report.personnel_answering = form.personnel_answering.data
    pit_report.personnel_notes = form.personnel_notes.data

    # notes
    pit_report.notes = form.notes.data
    
    team = Team.query.filter_by(team_number=form.team_number.data).first()

    if not team:
      team = Team(
        team_number = form.team_number.data
      )

    team.pit_reports.append(pit_report)

    db.session.add(team)
    db.session.add(pit_report)
    db.session.commit()

    return(redirect(url_for("pit_scout.all_reports", team_number=team_number)))

  return(render_template("pit_scout/add_pit_report.html", form=form, team_number=team_number))

@pit_scout.route("/add_pit_photos", defaults={"team_number": None},
                 methods=["GET", "POST"])
@pit_scout.route("/add_pit_photos/<int:team_number>", methods=["GET", "POST"])
def add_pit_photos(team_number):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))
  
  form = PitPhotosForm(request.form)
  
  if request.method == "POST":
    return(redirect(url_for("pit_scout.add_pit_report")))

  return(render_template("pit_scout/add_pit_photos.html", form=form))

@pit_scout.route("/edit_pit_report/<int:pit_report_id>", methods=["GET", "POST"])
def edit_pit_report(pit_report_id):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  # get pit report info, find associated team
  pit_report = PitReport.query.filter(PitReport.id == pit_report_id).first()
  team = Team.query.filter_by(id=pit_report.team_id).first()

  form = PitReportForm(request.form)
  
  if request.method == "POST" and form.validate():
    user_info = google_auth.get_user_info()

    # metadata
    pit_report.event = form.event.data
    pit_report.created_by = user_info["id"]

    # drivetrain
    pit_report.drivetrain_type = form.drivetrain_type.data
    if form.drivetrain_type_other.data:
      pit_report.drivetrain_type_other = form.drivetrain_type_other.data

    pit_report.wheel_type = form.wheel_type.data
    if form.wheel_type_other.data:
      pit_report.wheel_type_other = form.wheel_type_other.data
    pit_report.wheel_number = form.wheel_number.data

    pit_report.motor_type = form.motor_type.data
    if form.motor_type_other.data:
      pit_report.motor_type_other = form.motor_type_other.data

    pit_report.motor_number = form.motor_number.data

    pit_report.drivetrain_notes = form.drivetrain_notes.data

    # physical characteristics
    if form.weight_unit.data == "Kilograms":
      pit_report.weight = form.weight.data * 2.20462
    else:
      pit_report.weight = form.weight.data
    
    if form.dimensions_unit.data == "Centimeters":
      pit_report.height = form.height.data * 0.393701
      pit_report.width = form.height.data * 0.393701
      pit_report.length = form.length.data * 0.393701
    else:
      pit_report.height = form.height.data
      pit_report.width = form.height.data
      pit_report.length = form.length.data
    
    if form.speed_unit.data == "Meters Per Second":
      pit_report.speed_unit = form.speed_unit.data * 3.28084
    else:
      pit_report.speed_unit = form.speed_unit.data

    # auto
    pit_report.auto_move = form.auto_move.data
    pit_report.auto_collect_balls = form.auto_collect_balls.data
    pit_report.auto_score_bottom = form.auto_score_bottom.data
    pit_report.auto_score_outer = form.auto_score_outer.data
    pit_report.auto_score_inner = form.auto_score_inner.data
    if form.auto_consistency.data:
      pit_report.auto_consistency = form.auto_consistency.data
    pit_report.auto_prefered_position = form.auto_prefered_position.data

    # teleop
    pit_report.teleop_score_bottom = form.teleop_score_bottom.data
    pit_report.teleop_score_outer = form.teleop_score_outer.data
    pit_report.teleop_score_inner = form.teleop_score_inner.data
    if form.teleop_consistency.data:
      pit_report.teleop_consistency = form.teleop_consistency.data
    if form.teleop_ball_capacity.data:
      pit_report.teleop_ball_capacity = form.teleop_ball_capacity.data
    pit_report.teleop_prefered_position = form.teleop_prefered_position.data

    # control
    pit_report.control_panel_rotation = form.control_panel_rotation.data
    pit_report.control_panel_position = form.control_panel_position.data

    # hang
    pit_report.hang_able = form.hang_able.data
    pit_report.hang_level = form.hang_level.data
    pit_report.hang_prefered_position = form.hang_prefered_position.data
    if form.hang_consistency.data:
      pit_report.hang_consistency = form.hang_consistency.data
    pit_report.hang_time = form.hang_time.data
    pit_report.hang_active = form.hang_active.data

    # personnel
    if form.personnel_honesty.data:
      pit_report.personnel_honesty = form.personnel_honesty.data
    if form.personnel_answering.data:
      pit_report.personnel_answering = form.personnel_answering.data
    pit_report.personnel_notes = form.personnel_notes.data

    # notes
    pit_report.notes = form.notes.data

    # find team from form
    team = Team.query.filter_by(team_number=form.team_number.data).first()

    # if team doesn't exist, make it
    if not team:
      team = Team(
        team_number = form.team_number.data
      )

    # add pit report to team
    team.pit_reports.append(pit_report)

    db.session.commit()
    return(redirect(url_for("pit_scout.pit_report", team_number=team.team_number)))
  else:
    # metadata
    form.team_number.data = team.team_number
    form.event.data = pit_report.event

    # drivetrain
    form.drivetrain_type.data = pit_report.drivetrain_type
    form.drivetrain_type_other.data = pit_report.drivetrain_type_other
    form.wheel_type.data = pit_report.wheel_type
    form.wheel_type_other.data = pit_report.wheel_type_other
    form.wheel_number.data = pit_report.wheel_number
    form.motor_type.data = pit_report.motor_type
    form.motor_type_other.data = pit_report.motor_type_other
    form.motor_number.data = pit_report.motor_number
    form.drivetrain_notes.data = pit_report.drivetrain_notes

    # physical characteristics
    form.weight.data = pit_report.weight
    form.height.data = pit_report.height
    form.width.data = pit_report.width
    form.length.data = pit_report.length
    form.speed.data = pit_report.speed

    # auto
    form.auto_move.data = pit_report.auto_move
    form.auto_score_bottom.data = pit_report.auto_score_bottom
    form.auto_score_outer.data = pit_report.auto_score_outer
    form.auto_score_inner.data = pit_report.auto_score_inner
    form.auto_collect_balls.data = pit_report.auto_collect_balls
    form.auto_consistency.data = pit_report.auto_consistency
    form.auto_prefered_position.data = pit_report.auto_prefered_position
    print(form.auto_prefered_position.data)
    print(pit_report.auto_prefered_position)

    # teleop
    form.teleop_score_bottom.data = pit_report.teleop_score_bottom
    form.teleop_score_outer.data = pit_report.teleop_score_outer
    form.teleop_score_inner.data = pit_report.teleop_score_inner
    form.teleop_consistency.data = pit_report.teleop_consistency
    form.teleop_ball_capacity.data = pit_report.teleop_consistency
    form.teleop_prefered_position.data = pit_report.teleop_prefered_position

    # control panel
    form.control_panel_rotation.data = pit_report.control_panel_rotation
    form.control_panel_position.data = pit_report.control_panel_position

    # hang
    form.hang_able.data = pit_report.hang_able
    form.hang_level.data = pit_report.hang_level
    form.hang_prefered_position.data = pit_report.hang_prefered_position
    form.hang_consistency.data = pit_report.hang_consistency
    form.hang_time.data = pit_report.hang_time
    form.hang_active.data = pit_report.hang_active

    # personnel
    form.personnel_honesty.data = pit_report.personnel_honesty
    form.personnel_answering.data = pit_report.personnel_answering
    form.personnel_notes.data = pit_report.personnel_notes

    # notes
    form.notes.data = pit_report.notes

    return(render_template("pit_scout/edit_pit_report.html", form=form))

@pit_scout.route("/delete_pit_report/<int:pit_report_id>", methods=["POST"])
def delete_pit_report(pit_report_id):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  # get pit report info
  pit_report = PitReport.query.filter(PitReport.id == pit_report_id).first()

  db.session.delete(pit_report)
  db.session.commit()
  
  return(redirect(url_for("pit_scout.all_reports")))