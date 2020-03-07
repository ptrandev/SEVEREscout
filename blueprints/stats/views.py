from flask import Flask, Blueprint, render_template, url_for, redirect, request
from forms import TeamForm, TeamSearchForm
from models import Match, MatchReport, Bookmark, PitReport, AllianceSuggestion, TeamStats, Team
from app import db

import os
import requests
import google_auth

stats = Blueprint("stats", __name__, template_folder="templates")

@stats.route("/", methods=["GET"])
def all_stats():
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  form = TeamSearchForm(request.form)

  teams = Team.query.join(TeamStats).all()

  return(render_template("stats/all_stats.html", form=form, teams=teams))