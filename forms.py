from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, IntegerField, BooleanField, SelectMultipleField, TextAreaField, FloatField, SelectField, MultipleFileField
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from wtforms.widgets.html5 import NumberInput

#import models
#from wtforms_alchemy import ModelForm

class PitReportForm(FlaskForm):
  # metadata
  team_number = IntegerField("Team Number", validators=([DataRequired()]))
  event = SelectField("Event", choices=[
    ("Week 3: NE District North Shore", "Week 3: NE District North Shore"),
    ("Week 5: NE District Southern NH", "Week 5: NE District Southern NH")])
  # drivetrain
  drivetrain_type = SelectField("Drivetrain Type", choices=[("Kit of Parts", "Kit of Parts"), ("West Coast", "West Coast"), ("Mechanum", "Mechanum"), ("Omni", "Omni"), ("Swerve", "Swerve"), ("Tank Tread", "Tank Tread"), ("Other", "Other")])
  drivetrain_type_other = StringField("Drivetrain Type Other")
  wheel_type = SelectMultipleField("Wheel Type", choices=[("Kit of Parts", "Kit of Parts"), ("Colson", "Colson"), ("Pneumatic", "Pneumatic"), ("Omni", "Omni"), ("Mechanum", "Mechanum"), ("Tank Tread", "Tank Tread"), ("Other", "Other")])
  wheel_type_other = StringField("Wheel Type Other")
  wheel_number = IntegerField("Wheel Number", validators=([Optional()]))
  motor_type = SelectMultipleField("Motor Type", choices=[("Falcon", "Falcon"), ("Cim", "Cim"), ("MiniCim", "MiniCim"), ("Neo", "Neo"), ("Other", "Other")])
  motor_type_other = StringField("Motor Type Other")
  motor_number = IntegerField("Motor Number", validators=([Optional()]))
  drivetrain_notes = TextAreaField("Drivetrain Notes")
  # physical characteristics
  weight = FloatField("Weight", validators=([Optional()]))
  weight_unit = SelectField("Weight Unit", choices=[("Pounds", "Pounds"), ("Kilograms", "Kilograms")])
  dimensions_unit = SelectField("Dimensions Unit", choices=[("Inches", "Inches"), ("Centimeters", "Centimeters")])
  height = FloatField("Height", validators=([Optional()]))
  width = FloatField("Width", validators=([Optional()]))
  length = FloatField("Length", validators=([Optional()]))
  speed_unit = SelectField("Speed Unit", choices=[("Feet Per Second", "Feet Per Second"), ("Meters Per Second", "Meters Per Second")])
  speed = FloatField("Speed", validators=([Optional()]))
  # auto
  auto_move = BooleanField("Move Past Line")
  auto_score_bottom = BooleanField("Score Bottom")
  auto_score_outer = BooleanField("Score Outer")
  auto_score_inner = BooleanField("Score Inner")
  auto_collect_balls = BooleanField("Collect Balls")
  auto_consistency = SelectField("Consistency", choices=[(0, "N/A"), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], coerce=int)
  auto_prefered_position = SelectMultipleField("Prefered Position",
                                       choices=[("Far Left", "Far Left"),
                                                ("Left", "Left"),
                                                ("Center", "Center"),
                                                ("Right", "Right"),
                                                ("Far Right", "Far Right")])
  # teleop
  teleop_score_bottom = BooleanField("Score Botton")
  teleop_score_outer = BooleanField("Score Outer")
  teleop_score_inner = BooleanField("Score Inner")
  teleop_consistency = SelectField("Consistency", choices=[(0,"N/A"), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], coerce=int)
  teleop_ball_capacity = SelectField("Ball Capacity", choices=[(0,"N/A"), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], coerce=int)
  teleop_prefered_position = TextField("Prefered Position")
  # control panel
  control_panel_rotation = BooleanField("Rotation")
  control_panel_position = BooleanField("Position")
  # hang
  hang_able = BooleanField("Able")
  hang_level = BooleanField("Level")
  hang_prefered_position = SelectMultipleField("Prefered Position", choices=[("Far Left", "Far Left"), ("Left", "Left"), ("Center", "Center"), ("Right", "Right"), ("Far Right", "Far Right")])
  hang_consistency = SelectField("Consistency", choices=[(0,"N/A"), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], coerce=int)
  hang_time = FloatField("Time", validators=([Optional()]))
  hang_active = BooleanField("Active")
  # personnel
  personnel_honesty = SelectField("Honesty", choices=[(0,"N/A"), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], coerce=int)
  personnel_answering = SelectField("Knew Answers", choices=[(0,"N/A"), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], coerce=int)
  personnel_notes = TextAreaField("Personnel Notes")
  # notes
  notes = TextAreaField("Notes")
  # submit
  submit = SubmitField("Submit Team")
  
class PitPhotosForm(FlaskForm):
  photos = MultipleFileField("Robots Photos")
  submit = SubmitField("Submit Photos")

class MatchReportForm(FlaskForm):
  # metadata
  team_number = IntegerField("Team Number", validators=([DataRequired()]))
  match = IntegerField("Match", widget=NumberInput(), validators=([NumberRange(min=1)]))
  event = SelectField("Event", choices=[("Week 3: NE District North Shore", "Week 3: NE District North Shore"), ("Week 5: NE District Southern NH", "Week 5: NE District Southern NH")])
  alliance = SelectField("Alliance", choices=[("Blue", "Blue"), ("Red", "Red")])
  station = SelectField("Station", choices=[(1, 1), (2, 2), (3, 3)], coerce=int)
  # auto
  auto_move = BooleanField("Move")
  auto_score_bottom = IntegerField("Score Bottom", widget=NumberInput(), validators=([NumberRange(min=0)]), default=0)
  auto_score_upper = IntegerField("Score Upper", widget=NumberInput(), validators=([NumberRange(min=0)]), default=0)
  auto_collect_balls = BooleanField("Collected Balls")
  # teleop
  teleop_score_bottom = IntegerField("Score Bottom", widget=NumberInput(), validators=([NumberRange(min=0)]), default=0)
  teleop_score_upper = IntegerField("Score Upper", widget=NumberInput(), validators=([NumberRange(min=0)]), default=0)
  teleop_attempts = IntegerField("Attempts", widget=NumberInput(), validators=([NumberRange(min=0)]), default=0)
  # control panel
  control_panel_rotation = BooleanField("Rotation")
  control_panel_position = BooleanField("Position")
  # hang
  hang_able = BooleanField("Able")
  hang_level = BooleanField("Level")
  hang_position = SelectField("Position", choices=[("Far Left", "Far Left"), ("Left", "Left"), ("Center", "Center"), ("Right", "Right"), ("Far Right", "Far Right")])
  hang_active = BooleanField("Active")
  # defense
  defense_performance = SelectField("Performance (1-5)", choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], coerce=int) 
  defense_penalities = IntegerField("Penalites", widget=NumberInput(), validators=([NumberRange(min=0)]), default=0)
  # comms
  connection_issues = BooleanField("Connection Issues")
  brownouts = BooleanField("Brownouts")
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
  score_bottom = BooleanField("Score Bottom")
  score_outer = BooleanField("Score Outer")
  score_inner = BooleanField("Score Inner")
  control_panel = BooleanField("Control Panel")
  auto_move = BooleanField("Move Past Line")
  auto_score_bottom = BooleanField("Score Bottom")
  auto_score_outer = BooleanField("Score Outer")
  auto_score_inner = BooleanField("Score Inner")
  notes = TextAreaField("Notes")
  submit = SubmitField("Submit Team")

class TeamSearchForm(FlaskForm):
  team_number = IntegerField("Team Number", validators=([DataRequired()]))
  submit = SubmitField("Search Team")