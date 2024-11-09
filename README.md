Sahar-Abdi
Database Schema and Model Details

We have used Flask, SQLAlchemy, and Bcrypt to create an SQLite database. This database includes two tables:
1. User: To store user information and authentication.
2. PredictionHistory: To store predictions made for each user.

Table: users
Field	Type	Description
id	Integer (Primary Key)	Unique identifier for each user
username	String (Unique, Not Null)	User's unique username
email	String (Unique, Not Null)	User's unique email address
password_hash	String (Not Null)	Hashed password for security

Relationships:
- One-to-Many: Relationship with the prediction_history table (each user can have multiple predictions).
Explanation:
- id: The unique identifier for a user.
- username: The username, which must be unique.
- email: The user's email, which must be unique.
- password_hash: Hashed password for added security.

Table: prediction_history
Field	Type	Description
id	Integer (Primary Key)	Unique identifier for each prediction
user_id	Integer (Foreign Key from users.id)	Reference to the user who made the prediction
age	Integer (Not Null)	Age of the patient
sex	String (Not Null)	Gender of the patient
chest_pain	String (Not Null)	Type of chest pain
resting_blood_pressure	Integer (Not Null)	Resting blood pressure
cholesterol	Integer (Not Null)	Cholesterol level
fasting_blood_sugar	String (Not Null)	Fasting blood sugar level
resting_ecg	String (Not Null)	Resting electrocardiographic results
max_heart_rate	Integer (Not Null)	Maximum heart rate achieved
exercise_angina	String (Not Null)	Exercise-induced angina
old_peak	Float (Not Null)	ST depression induced by exercise
st_slope	String (Not Null)	Slope of the ST segment
n_major_vessels	Integer (Not Null)	Number of major vessels
thalium	String (Not Null)	Thallium stress test result
result	String (Not Null)	Prediction result (e.g., "Positive" or "Negative")
Timestamp	DateTime (Default: Current Time)	Time when the prediction was made


Relationships:
- Foreign Key: Relationship with the users table (each prediction belongs to a specific user).

Explanation:
- user_id: The ID of the user who made the prediction.
- age, sex, chest_pain, and other fields: Input data for the prediction.
- result: The prediction outcome (e.g., "Positive" or "Negative").
- timestamp: The time when the prediction was saved.


Model Classes

User Model:
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    predictions = db.relationship('PredictionHistory', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


PredictionHistory Model:
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
    exercise_angina = db.Column(db.String, nullable=False)
    old_peak = db.Column(db.Float, nullable=False)
    st_slope = db.Column(db.String, nullable=False)
    n_major_vessels = db.Column(db.Integer, nullable=False)
    thalium = db.Column(db.String, nullable=False)
    result = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


Conclusion:
- The users table is used for managing user login, registration, and authentication.
- The prediction_history table stores the results of predictions made by users.
- The One-to-Many relationship allows each user to have multiple predictions associated with them.


