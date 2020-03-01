from flask import Flask, Blueprint, render_template, url_for, redirect, request
from models import Bookmark
from app import db

import os
import requests
import google_auth

bookmarks = Blueprint("bookmarks", __name__, template_folder="templates")

@bookmarks.route("/")
def display_bookmarks():
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))
  
  bookmarks = Bookmark.query.all()

  return(render_template("bookmarks/bookmarks.html", bookmarks=bookmarks))

@bookmarks.route("/bookmark_team/<int:team_number>", methods=["POST"])
def bookmark_team(team_number):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  #user_info = google_auth.get_user_info()

  bookmark = Bookmark.query.filter(Bookmark.team_number == team_number).first()

  if bookmark:
    db.session.delete(bookmark)
    db.session.commit()
  else:
    #bookmark = Bookmark(team_number=team_number, created_by=user_info["id"])

    bookmark = Bookmark(team_number=team_number, created_by="424242")

    db.session.add(bookmark)
    db.session.commit()

  return(redirect(url_for("team.profile", team_number=team_number)))