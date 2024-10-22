from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import login_required, UserMixin, current_user
import secrets
  

app = Flask(__name__)

# Configuring app
app.config['SECRET_KEY'] = secrets.token_hex(16)
# Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heart.db'

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
            

            # Make a prediction using the predict function
            

            # Interpret the result
            

            # Store the inputs and prediction result in the database
            

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

@app.route('/history')
@login_required
def history():
    # Fetch the predictions made by the current user
    predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.date_created.desc()).all()
    # Pass the predictions to the history template
    return render_template('history.html', predictions=predictions)

if __name__ == '__main__':
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, ssl_context='adhoc')

 
    