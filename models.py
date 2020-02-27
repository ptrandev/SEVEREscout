from app import db
from sqlalchemy.sql import func

class TeamPit(db.Model):
    __tablename__ = "team_pit"
    id = db.Column(db.Integer, primary_key=True)
    # metadata
    team_number = db.Column(db.Integer)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    created_by = db.Column(db.Integer)
    # drivetrain
    drivetrain_type = db.Column(db.String)
    wheel_type = db.Column(db.String)
    wheel_number = db.Column(db.Integer)
    motor_type = db.Column(db.String)
    motor_number = db.Column(db.String)
    drivetrain_notes = db.Column(db.String)
    # physical characteristics
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    width = db.Column(db.Float)
    length = db.Column(db.Float)
    speed = db.Column(db.Float)
    # auto
    auto_move = db.Column(db.Boolean)
    auto_score_lower = db.Column(db.Boolean)
    auto_score_outer = db.Column(db.Boolean)
    auto_score_inner = db.Column(db.Boolean)
    auto_collect_balls = db.Column(db.Boolean)
    auto_consistency = db.Column(db.Integer)
    auto_prefered_position = db.Column(db.String)
    # teleop
    teleop_score_lower = db.Column(db.Boolean)
    teleop_score_outer = db.Column(db.Boolean)
    teleop_score_inner = db.Column(db.Boolean)
    teleop_consistency = db.Column(db.Integer)
    teleop_prefered_position = db.Column(db.String)
    # control panel
    control_panel_rotation = db.Column(db.Boolean)
    control_panel_postition = db.Column(db.Boolean)
    # hang
    hang_able = db.Column(db.Boolean)
    hang_level = db.Column(db.Boolean)
    hang_prefered_position = db.Column(db.String)
    hang_consistency = db.Column(db.Integer)
    hang_time = db.Column(db.Float)
    hang_active = db.Column(db.Boolean)
    # personnel
    personnel_honest = db.Column(db.Integer)
    personnel_answer = db.Column(db.Integer)
    personnel_notes = db.Column(db.String)
    # event
    event = db.Column(db.String)
    # notes
    notes = db.Column(db.String)

class Match(db.Model):
    __tablename__ = "match"
    id = db.Column(db.Integer, primary_key=True)
    match = db.Column(db.Integer)
    match_reports = db.relationship("MatchReport", backref="match", lazy=True)

class MatchReport(db.Model):
    __tablename__ = "match_report"
    id = db.Column(db.Integer, primary_key=True)
    # match relationship
    match_id = db.Column(db.Integer, db.ForeignKey("match.id"), nullable=False)
    # metadata
    team_number = db.Column(db.Integer)
    alliance = db.Column(db.String)
    station = db.Column(db.Integer)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    created_by = db.Column(db.String)
    # auto
    auto_move = db.Column(db.Boolean)
    auto_score_lower = db.Column(db.Integer)
    auto_score_upper = db.Column(db.Integer)
    auto_collect_balls = db.Column(db.Boolean)
    auto_points = db.Column(db.Integer)
    # teleop
    teleop_score_lower = db.Column(db.Integer)
    teleop_score_upper = db.Column(db.Integer)
    teleop_points = db.Column(db.Integer)
    teleop_attempts = db.Column (db.Integer)
    teleop_success_rate = db.Column(db.Float)
    # control panel
    control_panel_rotation = db.Column(db.Boolean)
    control_panel_position = db.Column(db.Boolean)
    control_panel_points = db.Column(db.Integer)
    # hang
    hang_able = db.Column(db.Boolean)
    hang_level = db.Column(db.Boolean)
    hang_position = db.Column(db.String)
    hang_active = db.Column(db.Boolean)
    hang_points = db.Column(db.Integer)
    # defense
    defense_performance = db.Column(db.Integer)
    defense_penalties = db.Column(db.Integer)
    # comms
    connection_issues = db.Column(db.Boolean)
    brownouts = db.Column(db.Boolean)
    emergency_stop = db.Column(db.Boolean)
    #notes
    notes = db.Column(db.String)

"""
class TeamPit(db.Model):
    __tablname__ = "team_pit"
    id = db.Column(db.Integer, primary_key=True)
    team_number = db.Column(db.Integer)
    auto = db.relationship("Auto", back_populates="team_pit")
    drivetrain_configuration_id = db.Column(db.Integer,
                                            db.ForeignKey("drivetrain_configuration.id"))
    drivetrain_configuration = db.relationship("drivetrain_configuration", backref="team_pit")
    physical_characteristics_id = db.Column(db.Integer,
                                         db.ForeignKey("physical_characteristics.id"))
    physical_characteristics = db.relationship("physical_characteristics", backref="team_pit")
    teleop_id = db.Column(db.Integer, db.ForeignKey("teleop.id"))
    teleop = db.relationship("teleop", backref="team_pit")
    hang_id = db.Column(db.Integer, db.ForeignKey("hang.id"))
    hang = db.relationship("hang", backref="team_pit")
    personnel_id = db.Column(db.Integer, db.ForeignKey("personnel.id"))
    personnel = db.relationship("personnel", backref="team_pit")
    control_panel_id = db.Column(db.Integer, db.ForeignKey("control_panel.id"))
    control_panel = db.relationship("control_panel", backref="team_pit")
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    event = db.relationship("event", backref="team_pit")
    notes = db.Column(db.String)

    def __repr__(self):
        return(self.id)

class DrivetrainType(db.Model):
    __tablename__ = "drivetrain_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return(self.id)

class WheelType(db.Model):
    __tablename__ = "wheel_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return(self.id)

class MotorType(db.Model):
    __tablename__ = "motor_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return(self.id)

class DrivetrainConfiguration(db.Model):
    __tablename__ = "drivetrain_configuration"
    id = db.Column(db.Integer, primary_key=True)
    drivetrain_type_id = db.Column(db.Integer, db.ForeignKey("drivetrain_type.id"))
    drivetrain_type = db.relationship("drivetrain_type")
    wheel_type_id = db.Column(db.Integer, db.ForeignKey("wheel_type.id"))
    wheel_type = db.relationship("wheel_type")
    motor_type_id = db.Column(db.Integer, db.ForeignKey("motor_type.id"))
    motor_type = db.relationship("motor_type")
    notes = db.Column(db.String)
    team_pit_id = db.Column(db.Integer, db.ForeignKey("team_pit.id"))

    def __repr__(self):
        return(self.id)

class PhysicalCharacteristics(db.Model):
    __tablename__ = "physical_characteristics"
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    width = db.Column(db.Float)
    length = db.Column(db.Float)
    speed = db.Column(db.Float)
    team_pit_id = db.Column(db.Integer, db.ForeignKey("team_pit.id"))

    def __repr__(self):
        return(self.id)

class Auto(db.Model):
    __tablename__ = "auto"
    id = db.Column(db.Integer, primary_key=True)
    move = db.Column(db.Boolean)
    score_lower = db.Column(db.Boolean)
    score_outer = db.Column(db.Boolean)
    score_inner = db.Column(db.Boolean)
    collect_balls = db.Column(db.Boolean)
    consistency = db.Column(db.Integer)
    starting_position = db.Column(db.String)
    team_pit_id = db.Column(db.Integer, db.ForeignKey("team_pit.id"))
    team_pit = db.relationship("Parent", back_populates="children")

    def __repr__(self):
        return(self.id)

class Teleop(db.Model):
    __tablename__ = "teleop"
    id = db.Column(db.Integer, primary_key=True)
    score_lower = db.Column(db.Boolean)
    score_outer = db.Column(db.Boolean)
    score_inner = db.Column(db.Boolean)
    consistency = db.Column(db.Integer)
    shooting_position db.Column(db.String)
    team_pit_id = db.Column(db.Integer, db.ForeignKey("team_pit.id"))

    def __repr__(self):
        return(self.id)

class ControlPanel(db.Model):
    __tablename__ = "control_panel"
    id = db.Column(db.Integer, primary_key=True)
    rotation = db.Column(db.Boolean)
    postition = db.Column(db.Boolean)
    team_pit_id = db.Column(db.Integer, db.ForeignKey("team_pit.id"))

    def __repr__(self):
        return(self.id)

class Hang(db.Model):
    __tablename__ = "hang"
    id = db.Column(db.Integer, primary_key=True)
    able = db.Column(db.Boolean)
    level = db.Column(db.Boolean)
    prefered_position = db.Column(db.String)
    consistency = db.Column(db.Integer)
    time = db.Column(db.Float)
    active = db.Column(db.Boolean)
    team_pit_id = db.Column(db.Integer, db.ForeignKey("team_pit.id"))

    def __repr__(self):
        return(self.id)

class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    team_pit_id = db.Column(db.Integer, db.ForeignKey("team_pit.id"))

    def __repr__(self):
        return(self.id)

class Personnel(db.Model):
    __tablename__ = "personnel"
    id = db.Column(db.Integer, primary_key=True)
    honest = db.Column(db.Integer)
    answer = db.Column(db.Integer)
    notes = db.Column(db.String)
    team_pit_id = db.Column(db.Integer, db.ForeignKey("team_pit.id"))

    def __repr__(self):
        return(self.id)

class Match(db.Model):
    __tablename__ = "match"
    id = db.Column(db.Integer, primary_key=True)
    auto = db.Column(db.Integer,
                                            db.ForeignKey("drivetrain_configuration.id"))
    drivetrain_configuration = db.relationship("drivetrain_configuration", backref="team_pit")
    notes = db.Column(db.String)

class TeamMatch(db.Model):
    __tablename__ = "team_match"
    id = db.Column(db.Integer, primary_key=True)
    team_number = db.Column(db.Integer)
    notes = db.Column(db.String)

class Alliance(db.Model):
    __tablename__ = "alliance"
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String)

class Station(db.Model):
    __tablename__ = "station"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)

class AutoPoints(db.Model):
    __tablename__ = "auto_points"
    id = db.Column(db.Integer, primary_key=True)
    move = db.Column(db.Boolean)
    score_lower = db.Column(db.Integer)
    score_upper = db.Column(db.Integer)
    collect_balls = db.Column(db.Boolean)
    points = db.Column(db.Integer)

class TeleopPoints(db.Model):
    __tablename__ = "auto_points"
    id = db.Column(db.Integer, primary_key=True)
    score_lower = db.Column(db.Integer)
    score_upper = db.Column(db.Integer)
    points = db.Column(db.Integer)
    attempts = db.Column (db.Integer)

class ControlPanelPoints(db.Model):
    __tablename__ = "control_panel_points"
    id = db.Column(db.Integer, primary_key=True)
    rotation = db.Column(db.Boolean)
    position = db.Column(db.Boolean)

class HangPoints(db.Model):
    __tablename__ = "hang_points"
    id = db.Column(db.Integer, primary_key=True)
    able = db.Column(db.Boolean)
    level = db.Column(db.Boolean)
    position = db.Column(db.String)
    active = db.Column(db.Boolean)

class Defense(db.Model):
    __tablename__ = "defense"
    id = db.Column(db.Integer, primary_key=True)
    performance = db.Column(db.Integer)
    penalties = db.Column(db.Integer)

class Comms(db.Model):
    __tablename__ = "comms"
    id = db.Column(db.Integer, primary_key=True)
    connection_issues = db.Column(db.Integer)
    brownouts = db.Column(db.Integer)
    emergency_stop = db.Column(db.Integer)
"""