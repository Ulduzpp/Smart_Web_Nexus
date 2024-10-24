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
    
    # You can add additional fields for account status if needed
    is_active = db.Column(db.Boolean, default=True)  # Active user status
    is_authenticated = db.Column(db.Boolean, default=False)  # Authentication status
    predictions = db.relationship('Prediction', backref='user', lazy=True)
    # Override the get_id method to return the user ID as a string
    def get_id(self):
        return str(self.id)

# Define Prediction Model for storing inputs and results
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Store each feature input separately
    Age = db.Column(db.Integer, nullable=False)
    Sex = db.Column(db.String, nullable=False)
    ChestPain = db.Column(db.String, nullable=False)
    RestingBloodPressure = db.Column(db.Float, nullable=False)
    Cholesterol = db.Column(db.Float, nullable=False)
    FastingBloodSugar = db.Column(db.String, nullable=False)
    RestingECG = db.Column(db.String, nullable=False)
    MaxHeartRate = db.Column(db.Float, nullable=False)
    ExcerciseAngina = db.Column(db.String, nullable=False)
    OldPeak = db.Column(db.Float, nullable=False)
    STSlope = db.Column(db.String, nullable=False)
    nMajorVessels = db.Column(db.String, nullable=False)
    Thalium = db.Column(db.String, nullable=False)
    
    # Store the result 
    result = db.Column(db.String(50), nullable=False)
    
    # Timestamp (when the prediction was made)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Link prediction to the user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='predictions')
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
                # Set user as authenticated
                user.is_authenticated = True
                db.session.commit()
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
                Age = form.age.data
                Sex = form.sex.data
                ChestPain = form.ChestPain.data
                RestingBloodPressure = form.RestingBloodPressure.data
                Cholesterol = form.Cholesterol.data
                FastingBloodSugar = form.FastingBloodSugar.data
                RestingECG = form.RestingECG.data
                MaxHeartRate = form.MaxHeartRate.data
                ExcerciseAngina = form.ExcerciseAngina.data
                OldPeak = form.OldPeak.data
                STSlope = form.STSlope.data
                nMajorVessels = form.nMajorVessels.data
                Thalium = form.Thalium.data

                # Make a prediction using the predict function
                features = [
                    Age, Sex, ChestPain, RestingBloodPressure, Cholesterol, FastingBloodSugar, RestingECG,
                    MaxHeartRate, ExcerciseAngina, OldPeak, STSlope, nMajorVessels, Thalium
                ]
                result = predict_disease(features)

                # Store the inputs and prediction result in the database
                prediction = Prediction(
                    Age=Age,
                    Sex=Sex,
                    ChestPain=ChestPain,
                    RestingBloodPressure=RestingBloodPressure,
                    Cholesterol=Cholesterol,
                    FastingBloodSugar=FastingBloodSugar,
                    RestingECG=RestingECG,
                    MaxHeartRate=MaxHeartRate,
                    ExcerciseAngina=ExcerciseAngina,
                    OldPeak=OldPeak,
                    STSlope=STSlope,
                    nMajorVessels=nMajorVessels,
                    Thalium=Thalium,
                    result=result,
                    user_id=current_user.id  # Assuming the user is logged in
                )
                db.session.add(prediction)
                db.session.commit()

                # Prepare input data to pass to the result template
                input_data = {
                    'age': Age,
                    'sex': Sex,
                    'chest_pain': ChestPain,
                    'trestbps': RestingBloodPressure,
                    'chol': Cholesterol,
                    'fbs': FastingBloodSugar,
                    'restecg': RestingECG,
                    'thalach': MaxHeartRate,
                    'exang': ExcerciseAngina,
                    'oldpeak': OldPeak,
                    'slope': STSlope,
                    'ca': nMajorVessels,
                    'thal': Thalium
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
def invalid_creswntials(error):
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
