# form.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class InputForm(FlaskForm):
    age = IntegerField('Age (18-100)', validators=[DataRequired(), NumberRange(min=18, max=100)])
    sex = SelectField('Sex', choices=[('1', 'Male'), ('0', 'Female')], validators=[DataRequired()])
    chest_pain = SelectField('Chest Pain Type', choices=[('0', 'Typical angina'), ('1', 'Atypical angina'), ('2', 'Non-anginal pain'), ('3', 'Asymptomatic')], validators=[DataRequired()])
    resting_blood_pressure = IntegerField('Resting Blood Pressure (0-200 mm Hg)', validators=[DataRequired(), NumberRange(min=0, max=200)])
    cholesterol = IntegerField('Cholesterol (0-603)', validators=[DataRequired(), NumberRange(min=0, max=603)])
    fasting_blood_sugar = SelectField('Fasting Blood Sugar > 120 mg/dl', choices=[('1', 'True'), ('0', 'False')], validators=[DataRequired()])
    resting_ecg = SelectField('Resting Electrocardiographic Results', choices=[('0', 'Normal'), ('1', 'Abnormality'), ('2', 'Hypertrophy')], validators=[DataRequired()])
    max_heart_rate = IntegerField('Max Heart Rate Achieved (60-202)', validators=[DataRequired(), NumberRange(min=60, max=202)])
    exercise_angina = SelectField('Exercise-Induced Angina', choices=[('0', 'No'), ('1', 'Yes')], validators=[DataRequired()])
    old_peak = FloatField('ST Depression (-2.6 to 6.2)', validators=[DataRequired(), NumberRange(min=-2.6, max=6.2)])
    st_slope = SelectField('Slope of the ST Segment', choices=[('0', 'Upsloping'), ('1', 'Flat'), ('2', 'Downsloping')], validators=[DataRequired()])
    n_major_vessels = IntegerField('Major Vessels (0-4)', validators=[DataRequired(), NumberRange(min=0, max=4)])
    thalium = SelectField('Thalassemia', choices=[('0', 'Normal'), ('1', 'Fixed defect'), ('2', 'Reversible defect'), ('3', 'Not described')], validators=[DataRequired()])
    submit = SubmitField('Submit')