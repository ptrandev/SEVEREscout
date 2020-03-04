import functools
import sass
import json
import os

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

template_folder = "templates"
static_folder = "static"

sass.compile(dirname=('static/scss/main/', 'static/css/'))

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://phillip:phillip@localhost:5432/severescout"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import google_auth

from blueprints.home.views import home
from blueprints.pit_scout.views import pit_scout
from blueprints.match_scout.views import match_scout
from blueprints.team.views import team
from blueprints.bookmarks.views import bookmarks

app.register_blueprint(google_auth.app)
app.register_blueprint(home)
app.register_blueprint(team, url_prefix="/team")
app.register_blueprint(pit_scout, url_prefix="/pit_scout")
app.register_blueprint(match_scout, url_prefix="/match_scout")
app.register_blueprint(bookmarks, url_prefix="/bookmarks")

if __name__ == '__main__':
    app.run(debug=True)