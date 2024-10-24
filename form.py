from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    sex = StringField('Sex', validators=[DataRequired()])
    ChestPain = StringField('Chest Pain', validators=[DataRequired()])
    RestingBloodPressure = IntegerField('Resting Blood Pressure', validators=[DataRequired()])
    Cholesterol = IntegerField('Cholesterol', validators=[DataRequired()])
    FastingBloodSugar = StringField('Fasting Blood Sugar', validators=[DataRequired()])
    RestingECG = StringField('Resting ECG', validators=[DataRequired()])
    MaxHeartRate = IntegerField('Max Heart Rate', validators=[DataRequired()])
    ExcerciseAngina = StringField('Exercise Angina', validators=[DataRequired()])
    OldPeak = FloatField('Old Peak', validators=[DataRequired()])
    STSlope = StringField('ST Slope', validators=[DataRequired()])
    nMajorVessels = IntegerField('Number of Major Vessels', validators=[DataRequired()])
    Thalium = StringField('Thalium', validators=[DataRequired()])
    submit = SubmitField('Submit')