from flask import Flask, render_template, redirect, url_for, request, session, flash, abort
from flask_login import LoginManager, login_required, login_user, logout_user,UserMixin
import secrets
from form import InputForm  
from model import predict_disease
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  
from datetime import datetime
from flask import send_file
import pandas as pd
from io import BytesIO


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


# login_required method
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            abort(401)
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # User Authentication and query to database
        user_exists = User.user_authentication(username= username)
        # Just for testing error_500 handling
        email_exists = User.query.filter_by(email=email).first()
        if user_exists:
                flash('Username already exists. Please choose a different one.', 'danger')
                return redirect(url_for('register'))
        elif email_exists:
            flash('Email already registered. Please choose a different one.', 'danger')
            abort(500)
        else:
            new_user = User(username= username, email= email, password_hash= password)
            # hashing password
            new_user.set_password(password= password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration was successful, Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():  
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # User Authentication and query to database
        user = User.user_authentication(username= username)
        email_user = User.query.filter_by(email=username).first()
        # Login with username or email
        if user :
            if user.check_password(password):
                # password is correct
                session['username'] = user.username
                session['email'] = user.email
                session['user_id'] = user.id
                flash('Log in successful!', 'success')
                return redirect(url_for('profile'))
            else:
                # password is incorrect
                flash('Incorrect password. Please try again.', 'warning')
        elif email_user:
            if email_user.check_password(password):
                # password is correct
                session['username'] = email_user.username
                session['email'] = email_user.email
                session['user_id'] = email_user.id
                flash('Log in successful!', 'success')
                return redirect(url_for('profile'))
            else:
                # password is incorrect
                flash('Incorrect password. Please try again.', 'warning')
        else:
            # The user does not exist
            flash('Username not found. Please register first.', 'danger')
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    # Count total predictions made by the user
    total_predictions = PredictionHistory.query.filter_by(user_id=session['user_id']).count()

    # Count predictions labeled as "Heart Disease" and "No Disease"
    heart_disease_count = PredictionHistory.query.filter_by(user_id=session['user_id'], result='Heart Disease').count()
    no_disease_count = PredictionHistory.query.filter_by(user_id=session['user_id'], result='No Disease').count()

    # Pass all counts to the template
    return render_template(
        'profile.html', 
        total_predictions=total_predictions,
        heart_disease_count=heart_disease_count,
        no_disease_count=no_disease_count
    )

@app.route('/logout')
def logout():
    session.pop('username')
    flash('You have been logged out!','info')
    return redirect(url_for('home'))

@app.route('/input', methods=['GET', 'POST'])
@login_required
def input_data():
    form = InputForm()
    if form.validate_on_submit():
        features = {
            'age': form.age.data,
            'sex': form.sex.data,
            'chest_pain': form.chest_pain.data,
            'resting_blood_pressure': form.resting_blood_pressure.data,
            'cholesterol': form.cholesterol.data,
            'fasting_blood_sugar': form.fasting_blood_sugar.data,
            'resting_ecg' : form.resting_ecg.data,
            'max_heart_rate': form.max_heart_rate.data,
            'excercise_angina': form.excercise_angina.data,
            'old_peak': form.old_peak.data,
            'st_slope': form.st_slope.data,
            'n_major_vessels': form.n_major_vessels.data,
            'thalium': form.thalium.data
        }

        prediction = predict_disease(features)

        # Save the prediction to the database
        if 'user_id' in session:
            PredictionHistory.save_prediction(features= features, user_id= session['user_id'], prediction_result= prediction)

        # Store the result in the session
        session['features'] = features
        session['result'] = prediction

        return redirect(url_for('result'))

    return render_template('input.html', form= form)

@app.route('/result')
@login_required
def result():
    features = session.get('features')
    result = session.get('result')  # Get result from query parameter
    if result is None:
        # Handle case where result is not provided, redirect back to input or an error page
        flash('No result available. Please input the data first.', 'warning')
        return redirect(url_for('input_data'))
    return render_template('result.html', result= result, features= features)

@app.route('/history')
@login_required
def history():
    # Fetch the predictions made by the current user
    predictions = PredictionHistory.query.filter_by(user_id=session['user_id']).order_by(PredictionHistory.timestamp.desc()).all()
    # Pass the predictions to the history template
    return render_template('history.html', predictions=predictions, username= session['username'])

#Route to download the prediction history report for a specific user.
@app.route('/download_report')
@login_required
def download_report():
    # Fetch the user's prediction history from the database
    predictions = PredictionHistory.query.filter_by(user_id=session['user_id']).all()
    
    # Convert the prediction data to a DataFrame
    data = {
        'Date': [pred.timestamp.strftime('%Y-%m-%d %H:%M:%S') for pred in predictions],  # Format the date
        'Age': [pred.age for pred in predictions],
        'Sex': [pred.sex for pred in predictions],
        'Chest Pain': [pred.chest_pain for pred in predictions],
        'Resting BP': [pred.resting_blood_pressure for pred in predictions],
        'Cholesterol': [pred.cholesterol for pred in predictions],
        'Fasting Blood Sugar': [pred.fasting_blood_sugar for pred in predictions],
        'Resting ECG': [pred.resting_ecg for pred in predictions],
        'Max Heart Rate': [pred.max_heart_rate for pred in predictions],
        'Exercise Angina': [pred.excercise_angina for pred in predictions],
        'Old Peak': [pred.old_peak for pred in predictions],
        'ST Slope': [pred.st_slope for pred in predictions],
        'Major Vessels': [pred.n_major_vessels for pred in predictions],
        'Thalium': [pred.thalium for pred in predictions],
        'Prediction': [pred.result for pred in predictions],
    }
    
    df = pd.DataFrame(data)
    
    # Create a CSV in memory
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    # Send the CSV file as a response
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='prediction_history.csv')

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
    app.run(host="0.0.0.0", port=5000)
