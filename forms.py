from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, IntegerField, BooleanField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

class TeamForm(FlaskForm):
  team_number = IntegerField("Team Number", validators=([DataRequired()]))
  drivetrain = StringField("Drivetrain")
  weight = IntegerField("Weight", validators=([Optional()]))
  hang = BooleanField("Hangs")
  balanced = BooleanField("Balanced")
  score_lower = BooleanField("Score Lower")
  score_outer = BooleanField("Score Outer")
  score_inner = BooleanField("Score Inner")
  control_panel = BooleanField("Control Panel")
  auto_move = BooleanField("Move Past Line")
  auto_score_lower = BooleanField("Score Lower")
  auto_score_outer = BooleanField("Score Outer")
  auto_score_inner = BooleanField("Score Inner")
  notes = TextAreaField("Notes")
  submit = SubmitField("Submit Team")

class TeamSearchForm(FlaskForm):
  team_number = IntegerField("Team Number", validators=([DataRequired()]))
  submit = SubmitField("Search Team")