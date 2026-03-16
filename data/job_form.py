from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    team_leader = IntegerField("ID team leader", validators=[DataRequired()])
    job = StringField("Job", validators=[DataRequired()])
    work_size = IntegerField("Duration", validators=[DataRequired()])
    collaborators = StringField("ID Collaborators")
    is_finished = BooleanField("Is finished")
    
    submit = SubmitField("Submit")