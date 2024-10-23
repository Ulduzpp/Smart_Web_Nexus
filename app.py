from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, UserMixin, current_user
import secrets
from model import predict_price
  

app = Flask(__name__)

# Configuring app
app.config['SECRET_KEY'] = secrets.token_hex(16)
# Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Heart_Disease.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heart_diagnosis.db'


# Initialize the database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# Define User Model for user tracking
class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),nullable=False,unique=True)
    password = db.Column(db.String(150),nullable=False)
    predictions = db.relationship('Prediction', backref='user', lazy=True)

# Define Prediction Model for storing inputs and results
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Store each feature input separately
    Age = db.Column(db.Float, nullable=False)
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

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pass = bcrypt.generate_password_hash(password).decode('utf_8')

        new_user = User(username = username,password = hashed_pass)
        db.session.add(new_user)
        db.session.commit()

        flash('Registeration was successful, please log in.','success')
        return redirect(url_for('login'))
    

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():  
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            session['username'] = user.username
            flash('Log in succesful!','success')
            return redirect(url_for('input_data'))
        else:
             flash('You must register!','danger') 
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('username')
    flash('You have been logged out!','info')
    return redirect(url_for('login'))

@app.route('/input' , methods=['GET', 'POST'])
@login_required
def input_data():
    if request.method == 'POST':
        try:
            # Retrieve and store individual feature inputs
            Age = float(request.form['age'])
            Sex = request.form['sex']
            ChestPain = request.form['ChestPain']
            RestingBloodPressure = float(request.form['RestingBloodPressure'])
            Cholesterol = float(request.form['Cholesterol'])
            FastingBloodSugar = request.form['FastingBloodSugar']
            RestingECG = request.form['RestingECG']
            MaxHeartRate = float(request.form['MaxHeartRate'])
            ExcerciseAngina = request.form['ExcerciseAngina']
            OldPeak = float(request.form['OldPeak'])
            STSlope = request.form['STSlope']
            nMajorVessels = request.form['nMajorVessels']
            Thalium = request.form['Thalium']
            
            

            # Make a prediction using the predict function
            features = [
                Age, Sex, ChestPain, RestingBloodPressure, Cholesterol, FastingBloodSugar, RestingECG
                ,MaxHeartRate, ExcerciseAngina, OldPeak, STSlope, nMajorVessels,Thalium
            ]
            result = predict_price(features)


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

            # Redirect to the result page with the prediction
            return render_template('result.html', result=result)

        except ValueError:
            flash("Invalid input. Please enter numeric values.", "danger")
            return render_template('input.html')

    return render_template('input.html')

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
    # Pass the predictions to the history template
    return render_template('history.html', predictions=predictions)


@app.errorhandler(403)
def forbidden(error):
    return render_template('error_403.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('error_404.html')


@app.errorhandler(500)
def internal_error(error):
    return render_template('error_500.html')


if __name__ == '__main__':
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)

 
    
