from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, IntegerField, BooleanField, SelectMultipleField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from wtforms.widgets.html5 import NumberInput

#import models
#from wtforms_alchemy import ModelForm

class TeamPitForm(FlaskForm):
  team_number = IntegerField("Team Number", validators=([DataRequired()]))
  notes = TextAreaField("Notes")
  # auto
  auto_move = BooleanField("Move Past Line")
  auto_score_lower = BooleanField("Score Lower")
  auto_score_outer = BooleanField("Score Outer")
  auto_score_inner = BooleanField("Score Inner")
  auto_collect_balls = BooleanField("Collect Balls")
  auto_consistency = IntegerField("Consistency")
  # drivetrain configuration
  drivetrain_type = StringField("Drivetrain Type")
  wheel_type = StringField("Wheel Type")
  motor_type = StringField("Motor Type")
  drivetrain_notes = TextAreaField("Drivetrain Notes")
  # physical characteristics
  weight = FloatField("Weight")
  height = FloatField("Height")
  width = FloatField("Width")
  length = FloatField("Length")
  speed = FloatField("Speed")
  # teleop
  teleop_score_lower = BooleanField("Score Lower")
  teleop_score_outer = BooleanField("Score Outer")
  teleop_score_inner = BooleanField("Score Inner")
  teleop_consistency = BooleanField("Consistency")
  # control panel
  control_panel_rotation = BooleanField("Rotation")
  control_panel_position = BooleanField("Position")
  # hang
  hang_able = BooleanField("Able")
  hang_level = BooleanField("Level")
  hang_prefered_postition = BooleanField("Prefered Position")
  hang_consistency = BooleanField("Consistency")
  hang_time = BooleanField("Time")
  # personnel
  personnel_honest = IntegerField("Honesty")
  personnel_answer = IntegerField("Knew Answers")

class MatchReportForm(FlaskForm):
  # metadata
  team_number = IntegerField("Team Number", validators=([DataRequired()]))
  match = IntegerField("Match", widget=NumberInput(), validators=([NumberRange(min=1)]))
  alliance = SelectField("Alliance", choices=[("Blue", "Blue"), ("Red", "Red")])
  station = IntegerField("Station", widget=NumberInput(), validators=([NumberRange(min=1, max=3)]))
  # auto
  auto_move = BooleanField("Move")
  auto_score_lower = IntegerField("Score Lower", widget=NumberInput(), validators=([NumberRange(min=0)]))
  auto_score_upper = IntegerField("Score Upper", widget=NumberInput(), validators=([NumberRange(min=0)]))
  auto_collect_balls = BooleanField("Collected Balls")
  # teleop
  teleop_score_lower = IntegerField("Score Lower", widget=NumberInput(), validators=([NumberRange(min=0)]))
  teleop_score_upper = IntegerField("Score Upper", widget=NumberInput(), validators=([NumberRange(min=0)]))
  teleop_attempts = IntegerField("Attempts", widget=NumberInput(), validators=([NumberRange(min=0)]))
  teleop_consistency = TextAreaField("Consistency")
  # control panel
  control_panel_rotation = BooleanField("Rotation")
  control_panel_position = BooleanField("Position")
  # hang
  hang_able = BooleanField("Able")
  hang_level = BooleanField("Level")
  hang_position = SelectField("Position", choices=[("Far Left", "Far Left"), ("Left", "Left"), ("Center", "Center"), ("Right", "Right"), ("Far Right", "Far Right")])
  hang_active = BooleanField("Active")
  # defense
  defense_performance = IntegerField("Performance (1-5)", widget=NumberInput(), validators=([NumberRange(min=1, max=5)])) 
  defense_penalities = IntegerField("Penalites", widget=NumberInput(), validators=([NumberRange(min=0)]))
  # comms
  connection_issues = IntegerField("Connection Issues")
  brownouts = IntegerField("Brownouts")
  emergency_stop = BooleanField("Emergency Stop")
  # notes
  notes = TextAreaField("Notes")
  # submit
  submit = SubmitField("Submit Team")

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