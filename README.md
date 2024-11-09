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


# Heart Disease Prediction Web Application

## Overview
The Heart Disease Prediction Web Application is designed to help users assess their likelihood of heart disease based on user-inputted health data.It leverages machine learning models to deliver accurate predictions and insights, allowing users to make informed health decisions.The app utilizes Flask for the backend, along with Bootstrap, HTML, and CSS for the frontend to create a responsive and user-friendly interface.

## Features

### 1. User Registration and Login Functionality:
- Secure user registration and authentication processes.
- Password hashing for enhanced security using Bcrypt.

### 2. User Profile with Prediction History:
- Personalized user profiles displaying previous predictions.
- Option for users to download their prediction history and insights as a report.

### 3. Responsive Design for Mobile and Desktop Views:
- Fully responsive interface optimized for both mobile and desktop users, ensuring accessibility across devices.
- Interactive elements that adapt to screen sizes for a seamless user experience.

### 4. Error Handling and User Feedback:
- User-friendly error messages and feedback for incorrect inputs, ensuring users understand what went wrong.
- Flash messages to notify users of successful actions (e.g., successful registration, login, etc.).

### 5. Data Security and Privacy:
- All user data is stored securely in the database.

### 6. Real-Time Predictions:
- Fast and efficient model predictions processed in real-time, providing users with immediate results.
### 7. Heart Disease Diagnosis Model

1. Project Overview

This project focuses on predicting heart disease using machine learning techniques. The model is trained on a dataset containing various health metrics, aiming to predict the presence of heart disease based on patient information. The notebook involves data preprocessing, exploratory data analysis (EDA), model training, evaluation, and saving the final model for deployment.

2. Data Preparation

2.1 Importing Libraries
   
The project utilizes several Python libraries, including:

Data Handling & Preprocessing: pandas, numpy, scipy

Data Visualization: matplotlib, seaborn, plotly

Modeling & Evaluation: scikit-learn, pickle

2.2 Loading the Dataset

The dataset used for this project is a heart disease dataset sourced from Kaggle. It contains 303 observations with 14 features including:

- Age: Age of the patient
- Sex: Gender (1 = Male, 0 = Female)
- ChestPain: Type of chest pain (0 = Typical angina, 1 = Atypical angina, 2 = Non-anginal pain, 3 = Asymptomatic)
- RestingBloodPressure: Resting blood pressure (mm Hg)
- Cholesterol: Serum cholesterol (mg/dl)
- FastingBloodSugar: Fasting blood sugar > 120 mg/dl (1 = True, 0 = False)
- RestingECG: Resting electrocardiographic results
- MaxHeartRate: Maximum heart rate achieved
- ExcerciseAngina: Exercise-induced angina (1 = Yes, 0 = No)
- OldPeak: ST depression induced by exercise relative to rest
- STSlope: The slope of the peak exercise ST segment
- nMajorVessels: Number of major vessels (0-3) colored by fluoroscopy
- Thalium: Thalassemia levels
- Status (Target): Presence of heart disease (1 = Disease, 0 = No Disease)

3. Data Preprocessing

3.1 Renaming Variables
   
The columns were renamed for better readability and interpretation. For example:

cp → ChestPain

trestbps → RestingBloodPressure

target → Status

3.2 Categorical Mapping

Categorical variables were transformed into more descriptive labels for better analysis:

Sex: Mapped to "Male" or "Female"

ChestPain: Mapped to descriptive labels (e.g., "Typical angina", "Atypical angina")

FastingBloodSugar: Converted to boolean

RestingECG, ExcerciseAngina, STSlope, and Thalium: Mapped to categorical labels.

3.3 Data Overview

The dataset was checked for:

Shape: (303 rows, 14 columns)

Data Types: Mix of integers, floats, and categorical variables

Missing Values: No missing values detected

4. Exploratory Data Analysis (EDA)

4.1 Statistical Summary

The dataset was summarized to identify trends:

Numerical Features: Age, RestingBloodPressure, Cholesterol, MaxHeartRate, OldPeak, nMajorVessels

Average Age: ~54 years

Average Cholesterol: ~246 mg/dl

Categorical Features: ChestPain, RestingECG, STSlope, etc.

Majority had "Typical angina" chest pain

Most patients did not experience exercise-induced angina

4.2 Univariate Analysis

Histogram and box plots were generated for continuous variables to observe distributions and detect outliers. For example:

The Age feature showed a slightly right-skewed distribution.

The Cholesterol feature contained some outliers based on the IQR method.

5. Model Building & Evaluation

5.1 Data Splitting

The dataset was split into training and test sets using an 80-20 split.

5.2 Model Structure and Training

The model used for heart disease prediction is a K-Nearest Neighbors (KNN) classifier. KNN is a simple, yet powerful algorithm that classifies data points based on their proximity to the nearest neighbors in the feature space.

The model's structure includes:

- Data Preprocessing: Feature scaling using StandardScaler to ensure that features are on the same scale.

- Model Selection: The KNN classifier was chosen for its simplicity and effectiveness in classification tasks.

- Hyperparameter Tuning: GridSearchCV was used to optimize the number of neighbors.

Model Evaluation:

Accuracy: Achieved a classification accuracy of approximately 85%.

Confusion Matrix: Displayed true positives, false positives, true negatives, and false negatives.

Classification Report: Showed precision, recall, F1-score for both classes (Heart Disease vs. No Disease).

5.3 Model Saving

The trained model was saved using the pickle module for future predictions

## Objective

The goal of this project is to collaboratively develop a smart web application that:
- Integrates a machine learning model for heart disease prediction.
- Implements user registration and authentication systems using a database.
- Containerizes the application with Docker and deploys it using Docker Swarm on a cloud-based host.

## Team Structure

The Nexus team consists of 5 members, each assigned specific tasks to contribute:

- FatemehHabibimoghaddam: **Frontend Developer**
- Ouldouz Pakpour: **Backend Developer**
- Sahar Abdi: **Database Engineer**
- Hanie Fazli: **Machine Learning Engineer**
- Hanie Fazli & Touba Derakhshandeh: **MLOps Engineers**

## Project Structure

Heart Disease Prediction Web Application
```bash
│   ├── assets
│   │   ├── dataset
│   │   ├── images
│   │   ├── heart_disease_diagnosis_model.ipynb
│   │   ├── heart_disease_diagnosis_model.py
│   ├── instance 
│   │   ├── Heart_Disease_Diagnosis.db
│   ├── static 
│   │   ├── css
│   │   │  └── style.css
│   │   ├── images
│   │   │  ├── Error_401.webp
│   │   │  ├── Error_403.webp
│   │   │  ├── Error_404.webp
│   │   │  ├── Error_500.webp
│   │   │  ├── Heart_Disease.webp
│   │   │  ├── No_Disease.webp
│   │   │  ├── Logo.webp
│   │   │  ├── smart_app.webp
│   ├── templates/
│   │   ├── base_error.html
│   │   ├── base.html
│   │   ├── error_401.html
│   │   ├── error_403.html
│   │   ├── error_404.html
│   │   ├── error_500.html
│   │   ├── history.html
│   │   ├── home.html
│   │   ├── input.html
│   │   ├── login.html
│   │   ├── profile.html
│   │   ├── register.html
│   │   └── result.html
│   ├── .gitignore
│   ├── app.py
│   ├── form.py
│   ├── heart_disease_diagnosis_model.pkl
│   ├── members.txt
│   ├── model.py 
│   ├── README.md
│   ├── requirements.txt
│   ├── Dockerfile
    └── docker-compose.yml
```

## Requirements
- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login
- Bcrypt
- Scikit-learn
- Docker
- Docker Compose


## Installation

1. Clone the repository

```bash
  git clone https://github.com/Ulduzpp/Smart_Web_Nexus.git
```

2. Navigate to the project directory

```bash
  cd Smart_Web_Nexus
```

3. Create a virtual environment

```bash
  python3 -m venv venv
```

4. Activate the virtual environment

```bash
  source venv/bin/activate
```

5. Install the required packages

```bash
  pip install -r requirements.txt
```

## Run Locally

1. Run the application

```bash
  python app.py
```

2. Open your web browser and go to http://127.0.0.1:5000.

## Demo

https://github.com/user-attachments/assets/782fc8a5-a77f-4b1a-8feb-819c627332a9
