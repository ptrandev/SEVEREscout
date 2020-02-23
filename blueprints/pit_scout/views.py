from flask import Flask, Blueprint, render_template, url_for, redirect, request
from forms import TeamPitForm
from models import TeamPit, Auto
from app import db

import os
import requests
import google_auth

pit_scout = Blueprint("pit_scout", __name__, template_folder="templates")

@pit_scout.route("/pit_scout")
def display_teams():
  return(render_template("pit_scout/display_teams.html"))

@pit_scout.route("/pit_scout/add", defaults={"team_number": None},
                 methods=["GET", "POST"])
@pit_scout.route("/pit_scout/add/<int:team_number>", methods=["GET", "POST"])
def add_team(team_number):
  
  form = TeamPitForm(request.form)
  
  if request.method == "POST" and form.validate():
    team = TeamPit(
      team_number = form.team_number.data
    )

    auto = Auto(
      move = form.auto_move.data,
      score_lower = form.auto_score_lower.data,
      score_outer = form.auto_score_outer.data,
      score_inner =  form.auto_score_inner.data,
      collect_balls = form.auto_collect_balls.data,
      consistency = form.auto_consistency.data
    )

    team.auto = auto

    db.session.add(team)
    db.session.add(auto)
    db.session.commit()
    
    return(redirect(url_for("pit_scout.display_teams")))

  return(render_template("pit_scout/add_team.html", form=form))