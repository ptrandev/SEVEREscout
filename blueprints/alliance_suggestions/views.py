from flask import Flask, Blueprint, render_template, url_for, redirect, request
from models import User, AllianceSuggestion, Team
from forms import TeamSearchForm
from app import db

import os
import requests
import google_auth

alliance_suggestions = Blueprint("alliance_suggestions", __name__, template_folder="templates")

@alliance_suggestions.route("/")
def display_suggestions():
  form = TeamSearchForm()

  alliance_suggestions_1 = AllianceSuggestion.query.filter(AllianceSuggestion.pick_number == 1).all()
  alliance_suggestions_2 = AllianceSuggestion.query.filter(AllianceSuggestion.pick_number == 2).all()

  return(render_template("/alliance_suggestions/display_suggestions.html", form=form, alliance_suggestions_1=alliance_suggestions_1, alliance_suggestions_2=alliance_suggestions_2))

@alliance_suggestions.route("/suggest_team/<int:team_number>/<int:pick_number>", methods=["POST"])
def suggest_team(team_number, pick_number):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  user_info = google_auth.get_user_info()

  user = User.query.filter(User.user_id==user_info["id"]).first()
  team = Team.query.filter_by(team_number=team_number).first()

  if not team:
    team = Team(
      team_number = team_number
    )

    db.session.add(team)

  alliance_suggestion = AllianceSuggestion.query.filter(AllianceSuggestion.team_id == team.id, AllianceSuggestion.pick_number == pick_number).first()

  if alliance_suggestion:
    db.session.delete(alliance_suggestion)
    db.session.commit()
  else:
    alliance_suggestion = AllianceSuggestion(team_id=team.id, user_id=user.id, pick_number=pick_number)

    db.session.add(alliance_suggestion)
    db.session.commit()

  return(redirect(url_for("team.profile", team_number=team_number)))

@alliance_suggestions.route("/team_accepted/<int:team_number>/<int:pick_number>", methods=["POST"])
def team_accepted(team_number, pick_number):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  user_info = google_auth.get_user_info()

  user = User.query.filter(User.user_id==user_info["id"]).first()
  team = Team.query.filter_by(team_number=team_number).first()

  alliance_suggestion = AllianceSuggestion.query.filter(AllianceSuggestion.team_id == team.id, AllianceSuggestion.pick_number == pick_number).first()

  # toggle alliance suggestion based on state
  if alliance_suggestion.accepted == True:
    alliance_suggestion.accepted = False
  else:
    alliance_suggestion.accepted = True

  alliance_suggestion.denied = False
  alliance_suggestion.already_selected = False

  db.session.commit()

  return(redirect(url_for("alliance_suggestions.display_suggestions")))

@alliance_suggestions.route("/team_denied/<int:team_number>/<int:pick_number>", methods=["POST"])
def team_denied(team_number, pick_number):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  user_info = google_auth.get_user_info()

  user = User.query.filter(User.user_id==user_info["id"]).first()
  team = Team.query.filter_by(team_number=team_number).first()

  alliance_suggestion = AllianceSuggestion.query.filter(AllianceSuggestion.team_id == team.id, AllianceSuggestion.pick_number == pick_number).first()

  # toggle alliance suggestion based on state
  if alliance_suggestion.denied == True:
    alliance_suggestion.denied = False
  else:
    alliance_suggestion.denied = True

  alliance_suggestion.accepted = False
  alliance_suggestion.already_selected = False

  db.session.commit()

  return(redirect(url_for("alliance_suggestions.display_suggestions")))

@alliance_suggestions.route("/team_already_selected/<int:team_number>/<int:pick_number>", methods=["POST"])
def team_already_selected(team_number, pick_number):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  user_info = google_auth.get_user_info()

  user = User.query.filter(User.user_id==user_info["id"]).first()
  team = Team.query.filter_by(team_number=team_number).first()

  alliance_suggestion = AllianceSuggestion.query.filter(AllianceSuggestion.team_id == team.id, AllianceSuggestion.pick_number == pick_number).first()

  # toggle alliance suggestion based on state
  if alliance_suggestion.already_selected == False:
    alliance_suggestion.already_selected = True
  else:
    alliance_suggestion.already_selected = False
  
  alliance_suggestion.accepted = False
  alliance_suggestion.denied = False

  db.session.commit()

  return(redirect(url_for("alliance_suggestions.display_suggestions")))