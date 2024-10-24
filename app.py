from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user 
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#2_ Ensure SQLAlchemy is used to connect the Flask app to the database.
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) 


#1_ Design and set up a SQLite (or other) database to store user data 
with app.app_context():
    db.create_all()


#1_1 User credentials 
# and 
# #3_1 Create tables: To store registration details.

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

   
    # 5_ Ensure that proper data validation and security measures
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

     
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class PredictionHistory(db.Model):
    __tablename__ = 'prediction_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    input_data = db.Column(db.String, nullable=False)
    prediction_result = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('predictions', lazy=True))

#4_ Write backend logic to query the database for user authentication and save model predictions
@app.route('/register', methods=['POST'])
def register():
     
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    
    new_user = User(username=username, email=email)
    new_user.set_password(password)  
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

 
@app.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    
    user = User.query.filter_by(username=username).first()

    
    if user and user.check_password(password):
        login_user(user)  
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid login credentials"}), 401


@app.route('/save_prediction', methods=['POST'])
@login_required  
def save_prediction():
    data = request.get_json()
    input_data = data.get('input_data')
    prediction_result = data.get('prediction_result')

    
    new_prediction = PredictionHistory(
        user_id=current_user.id, 
        input_data=input_data,
        prediction_result=prediction_result
    )
    db.session.add(new_prediction)
    db.session.commit()

    return jsonify({"message": "Prediction saved successfully"}), 201

if __name__ == '__main__':
    #1_ Design and set up a SQLite (or other) database to store user data 
    with app.app_context():
         db.create_all()
    app.run(debug=True)
