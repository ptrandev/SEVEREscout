from flask import Flask

template_folder = "../templates"

app = Flask(__name__, template_folder=template_folder)

from routes.home.views import home
app.register_blueprint(home)