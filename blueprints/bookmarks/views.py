from flask import Flask, Blueprint, render_template, url_for, redirect, request
from models import Bookmark, User
from forms import TeamSearchForm
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

  form = TeamSearchForm()

  user_info = google_auth.get_user_info()
  user = User.query.filter(User.user_id==user_info["id"]).first()

  all_bookmarks = Bookmark.query.filter(db.not_(Bookmark.user_id == user.id)).join(User).all()
  user_bookmarks = Bookmark.query.filter(Bookmark.user_id == user.id).join(User).all()

  return(render_template("bookmarks/display_bookmarks.html", all_bookmarks=all_bookmarks, user_bookmarks=user_bookmarks, form=form))

@bookmarks.route("/bookmark_team/<int:team_number>", methods=["POST"])
def bookmark_team(team_number):
  # check if logged in w/ google
  if not google_auth.is_logged_in():
    return(redirect(url_for("google_auth.login")))

  user_info = google_auth.get_user_info()

  user = User.query.filter(User.user_id==user_info["id"]).first()

  bookmark = Bookmark.query.filter(Bookmark.team_number == team_number, Bookmark.user_id == user.id).first()

  if bookmark:
    db.session.delete(bookmark)
    db.session.commit()
  else:
    bookmark = Bookmark(team_number=team_number, user_id=user.id)

    db.session.add(bookmark)
    db.session.commit()

  return(redirect(url_for("team.profile", team_number=team_number)))