from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, NumberRange

class InputForm(FlaskForm):
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=1, max=100, message="Age must be integer and between 29 and 79")])
    
    # Gender is now using descriptive values
    sex = SelectField('Gender', choices=[('', 'Select'), ('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    
    # Chest pain using descriptive values
    chest_pain = SelectField('Chest Pain', choices=[
        ('', 'Select'),
        ('Typical angina', 'Typical angina'),
        ('Atypical angina', 'Atypical angina'),
        ('Non-anginal pain', 'Non-anginal pain'),
        ('Asymptomatic', 'Asymptomatic')], validators=[DataRequired()])
    
    resting_blood_pressure = IntegerField('Resting Blood Pressure', validators=[InputRequired(), NumberRange(min=0, max=200, message="Resting Blood Pressure must be integer and between 0 and 200")])
    
    cholesterol = IntegerField('Cholesterol Measure', validators=[InputRequired(), NumberRange(min=0, max=603, message="Cholesterol Measure must be integer and between 0 and 603")])
    
    # Fasting blood sugar using descriptive values
    fasting_blood_sugar = SelectField('Fasting Blood Sugar', choices=[('', 'Select'), ('True', 'True'), ('False', 'False')], validators=[DataRequired()])
    
    resting_ecg = SelectField('Resting Electrocardiographic Result', choices=[
        ('', 'Select'),
        ('Normal', 'Normal'),
        ('Abnormality', 'Abnormality'),
        ('Hypertrophy', 'Hypertrophy')], validators=[DataRequired()])
    
    max_heart_rate = IntegerField('Max Heart Rate', validators=[InputRequired(), NumberRange(min=60, max=202, message="Max Heart Rate must be integer and between 60 and 202")])
    
    excercise_angina = SelectField('Exercise Angina', choices=[('', 'Select'), ('No', 'No'), ('Yes', 'Yes')], validators=[DataRequired()])
    
    old_peak = FloatField('Old Peak', validators=[InputRequired(), NumberRange(min=-2.6, max=6.2, message="Old Peak could be float and between -2.6 and 6.2")])
    
    st_slope = SelectField('ST Slope', choices=[
        ('', 'Select'),
        ('Upsloping', 'Upsloping'),
        ('Flat', 'Flat'),
        ('Downsloping', 'Downsloping')], validators=[DataRequired()])
    
    n_major_vessels = IntegerField('Number of Major Vessels', validators=[InputRequired(), NumberRange(min=0, max=4, message="Number of Major Vessels must be integer and between 0 and 4")])
    
    thalium = SelectField('Thalium', choices=[
        ('', 'Select'),
        ('Normal', 'Normal'),
        ('Fixed defect', 'Fixed defect'),
        ('Reversible defect', 'Reversible defect'),
        ('Not described', 'Not described')], validators=[DataRequired()])
    
    submit = SubmitField('Predict')