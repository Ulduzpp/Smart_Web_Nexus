from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, UserMixin, current_user, login_user, logout_user
import secrets
from form import InputForm  
from model import predict_disease

app = Flask(__name__)

# Configuring app
app.config['SECRET_KEY'] = secrets.token_hex(16)
# Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Heart_Disease_Diagnosis.db'

login_manager = LoginManager()
login_manager.init_app(app)

# Initialize the database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User loader for login management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Ensure user_id is converted to int

# Define User Model for user tracking
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    
    # Active user status
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship to Prediction
    predictions = db.relationship('Prediction', backref='user', lazy=True)

    # Override the get_id method to return the user ID as a string
    def get_id(self):
        return str(self.id)

# Define Prediction Model for storing inputs and results
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Store each feature input separately
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String, nullable=False)
    chest_pain = db.Column(db.String, nullable=False)
    resting_blood_pressure = db.Column(db.Float, nullable=False)
    cholesterol = db.Column(db.Float, nullable=False)
    fasting_blood_sugar = db.Column(db.String, nullable=False)
    resting_ecg = db.Column(db.String, nullable=False)
    max_heart_rate = db.Column(db.Float, nullable=False)
    exercise_angina = db.Column(db.String, nullable=False)
    old_peak = db.Column(db.Float, nullable=False)
    st_slope = db.Column(db.String, nullable=False)
    n_major_vessels = db.Column(db.String, nullable=False)
    thalium = db.Column(db.String, nullable=False)
    
    # Store the result 
    result = db.Column(db.String(50), nullable=False)
    
    # Timestamp (when the prediction was made)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Link prediction to the user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pass = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('You have registered before!', 'danger')
            return render_template('login.html')

        new_user = User(username=username, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration was successful, please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():  
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user:
            # Check if the password matches the hashed password in the database
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)  # Use Flask-Login's login_user function
                flash('Log in successful!', 'success')
                return redirect(url_for('input_data'))
            else:
                flash('Invalid username or password!', 'danger')
        else:
            flash('Username not found! Please register first.', 'warning')
            return redirect(url_for('register'))

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Use Flask-Login's logout_user function
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

@app.route('/input', methods=['GET', 'POST'])
@login_required
def input_data():
    form = InputForm()  # Create an instance of the form
    if request.method == 'POST':
        if form.validate_on_submit():  # Check if the form is submitted and valid
            try:
                # Retrieve and store individual feature inputs
                age = form.age.data
                sex = form.sex.data
                chest_pain = form.ChestPain.data
                resting_blood_pressure = form.RestingBloodPressure.data
                cholesterol = form.Cholesterol.data
                fasting_blood_sugar = form.FastingBloodSugar.data
                resting_ecg = form.RestingECG.data
                max_heart_rate = form.MaxHeartRate.data
                exercise_angina = form.ExcerciseAngina.data
                old_peak = form.OldPeak.data
                st_slope = form.STSlope.data
                n_major_vessels = form.nMajorVessels.data
                thalium = form.Thalium.data

                # Make a prediction using the predict function
                features = [
                    age, sex, chest_pain, resting_blood_pressure, cholesterol, fasting_blood_sugar, resting_ecg,
                    max_heart_rate, exercise_angina, old_peak, st_slope, n_major_vessels, thalium
                ]
                result = predict_disease(features)

                # Store the inputs and prediction result in the database
                prediction = Prediction(
                    age=age,
                    sex=sex,
                    chest_pain=chest_pain,
                    resting_blood_pressure=resting_blood_pressure,
                    cholesterol=cholesterol,
                    fasting_blood_sugar=fasting_blood_sugar,
                    resting_ecg=resting_ecg,
                    max_heart_rate=max_heart_rate,
                    exercise_angina=exercise_angina,
                    old_peak=old_peak,
                    st_slope=st_slope,
                    n_major_vessels=n_major_vessels,
                    thalium=thalium,
                    result=result,
                    user_id=current_user.id  # Assuming the user is logged in
                )
                db.session.add(prediction)
                db.session.commit()

                # Prepare input data to pass to the result template
                input_data = {
                    'age': age,
                    'sex': sex,
                    'chest_pain': chest_pain,
                    'trestbps': resting_blood_pressure,
                    'chol': cholesterol,
                    'fbs': fasting_blood_sugar,
                    'restecg': resting_ecg,
                    'thalach': max_heart_rate,
                    'exang': exercise_angina,
                    'oldpeak': old_peak,
                    'slope': st_slope,
                    'ca': n_major_vessels,
                    'thal': thalium
                }

                # Redirect to the result page with the prediction
                return render_template('result.html', input_data=input_data, result=result)

            except ValueError:
                flash("Invalid input. Please enter numeric values.", "danger")
                return render_template('input.html', form=form)

    return render_template('input.html', form=form)

@app.route('/result')
@login_required
def result():
    result = request.args.get('result')  # Get result from query parameter
    return render_template('result.html')

@app.route('/profile')
@login_required
def profile():
    # Fetch the predictions made by the current user
    predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.date_created.desc()).all()
    # Pass the predictions to the profile template
    return render_template('profile.html', predictions=predictions)

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
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)