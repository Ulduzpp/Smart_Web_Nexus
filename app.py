from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user,UserMixin
import secrets
from form import InputForm  
from model import predict_disease
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  
from datetime import datetime


app = Flask(__name__)

# Configuring app
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Heart_Disease_Diagnosis.db'

#Ensure SQLAlchemy is used to connect the Flask app to the database.
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#User credentials 
#and 
#Create tables: To store registration details.
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    predictions = db.relationship('PredictionHistory', backref='user', lazy=True)
    #Ensure that proper data validation and security measures
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

     
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # Write backend logic to query the database for user authentication
    def user_authentication(username):
        return User.query.filter_by(username=username).first()


class PredictionHistory(db.Model):
    __tablename__ = 'prediction_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String, nullable=False)
    chest_pain = db.Column(db.String, nullable=False)
    resting_blood_pressure = db.Column(db.Integer, nullable=False)
    cholesterol = db.Column(db.Integer, nullable=False)
    fasting_blood_sugar = db.Column(db.String, nullable=False)
    resting_ecg = db.Column(db.String, nullable=False)
    max_heart_rate = db.Column(db.Integer, nullable=False)
    excercise_angina = db.Column(db.String, nullable=False)
    old_peak = db.Column(db.Float, nullable=False)
    st_slope = db.Column(db.String, nullable=False)
    n_major_vessels = db.Column(db.Integer, nullable=False) 
    thalium = db.Column(db.String, nullable=False)
    result = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    def __init__(self, user_id, age, sex, chest_pain, resting_blood_pressure, cholesterol,
                 fasting_blood_sugar, resting_ecg, max_heart_rate, excercise_angina,
                 old_peak, st_slope, n_major_vessels, thalium, result):
        self.user_id = user_id
        self.age = age
        self.sex = sex
        self.chest_pain = chest_pain
        self.resting_blood_pressure = resting_blood_pressure
        self.cholesterol = cholesterol
        self.fasting_blood_sugar = fasting_blood_sugar
        self.resting_ecg = resting_ecg
        self.max_heart_rate = max_heart_rate
        self.excercise_angina = excercise_angina
        self.old_peak = old_peak
        self.st_slope = st_slope
        self.n_major_vessels = n_major_vessels
        self.thalium = thalium
        self.result = result

    def save_prediction(features, user_id, prediction_result):
        new_prediction = PredictionHistory(
            user_id=user_id,
            age=features['age'],
            sex=features['sex'],
            chest_pain=features['chest_pain'],
            resting_blood_pressure=features['resting_blood_pressure'],
            cholesterol=features['cholesterol'],
            fasting_blood_sugar=features['fasting_blood_sugar'],
            resting_ecg=features['resting_ecg'],
            max_heart_rate=features['max_heart_rate'],
            excercise_angina=features['excercise_angina'],
            old_peak=features['old_peak'],
            st_slope=features['st_slope'],
            n_major_vessels=features['n_major_vessels'],
            thalium=features['thalium'],
            result=prediction_result
        )
    
        db.session.add(new_prediction)
        db.session.commit()  # Don't forget to commit the session!

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():  
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    return redirect(url_for('login'))

@app.route('/input', methods=['GET', 'POST'])
@login_required
def input_data():
    return render_template('input.html')

@app.route('/result')
@login_required
def result():
    return render_template('result.html')

@app.route('/history')
@login_required
def history():
     return render_template('history.html')

@app.errorhandler(401)
def invalid_credentials(error):
    return render_template('error_401.html'), 401

@app.errorhandler(403)
def forbidden(error):
    return render_template('error_403.html'), 403

@app.errorhandler(404)
def not_found(error):
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error_500.html'), 500

if __name__ == '__main__':
    #Design and set up a SQLite (or other) database to store user data 
    with app.app_context():
          db.create_all()
    app.run(debug=True)
