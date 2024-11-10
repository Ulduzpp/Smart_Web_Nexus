# ❤️ Heart Disease Prediction Web Application ❤️

### 📖 Overview
The **Heart Disease Prediction Web Application** helps users predict their risk of heart disease using machine learning models. The app is built using **Flask**, **SQLAlchemy**, **Bcrypt**, and is deployed with **Docker**. It offers a user-friendly interface for inputting health data, viewing prediction results, and managing profiles.

## 🚀 Access the App
 Access the live version: [http://188.121.99.111:5000](http://188.121.99.111:5000)

---

## ✅ Features
1. **User Registration and Authentication**
   - Secure registration and login functionality.
   - Password hashing for added security using Bcrypt.

2. **User Profile and Prediction History**
   - View personalized prediction history.
   - Option to download past predictions as reports.

3. **Real-Time Predictions**
   - Immediate prediction results based on user-inputted health data.

4. **Responsive Design**
   - Optimized for both desktop and mobile users.

5. **Error Handling**
   - Clear error messages and feedback for incorrect inputs.
   - Flash messages for successful actions like registration and login.

6. **Data Security and Privacy**
   - Secure storage of user data using an SQLite database.
   - Encrypted passwords for user accounts.

---

## 🎯 Objective
The project's goal is to collaboratively develop a web application that:
- Utilizes machine learning for heart disease prediction.
- Implements user registration and authentication systems using a database.
- Containerizes the application with Docker and deploys it using Docker Swarm on a cloud-based host for scalability.

---

## ✅ Project Structure
```
Heart Disease Prediction Web Application
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
---

## Dataset and Model

### Dataset Details
The **dataset** used for training the model is sourced from [Kaggle's Heart Disease Dataset](https://www.kaggle.com/datasets/yasserh/heart-disease-dataset). It includes **303 observations** with **14 features**, such as:

- **Age**: Patient's age
- **Sex**: Gender (1 = Male, 0 = Female)
- **Chest Pain Type**: 
  - 0 = Typical angina
  - 1 = Atypical angina
  - 2 = Non-anginal pain
  - 3 = Asymptomatic
- **Resting Blood Pressure**: Measurement in mm Hg
- **Cholesterol**: Serum cholesterol in mg/dl
- **Fasting Blood Sugar**: >120 mg/dl (1 = True, 0 = False)
- **Resting ECG**: Electrocardiographic results
- **Max Heart Rate**: Maximum heart rate achieved
- **Exercise-Induced Angina**: (1 = Yes, 0 = No)
- **Old Peak**: ST depression induced by exercise relative to rest
- **ST Slope**: Slope of the peak exercise ST segment
- **Number of Major Vessels**: (0-3) colored by fluoroscopy
- **Thallium Stress Test Results**: (1 = Normal, 2 = Fixed Defect, 3 = Reversible Defect)
- **Target**: Presence of heart disease (1 = Disease, 0 = No Disease)

### Data Preprocessing and Feature Engineering
- **Renamed columns** for better readability.
- **Categorical Mapping** for variables:
  - Sex mapped to "Male" or "Female".
  - Chest Pain categorized into descriptive labels.
  - Resting ECG, Exercise-Induced Angina, and Thallium levels mapped to categorical descriptions.
- **Scaling**: StandardScaler was applied to normalize features.

### Exploratory Data Analysis (EDA)
- **Univariate Analysis**: Histograms and box plots for distribution analysis.
- **Insights**:
  - Most patients were aged around 54.
  - Majority had typical chest pain.
  - Significant correlation found between chest pain type and heart disease presence.

### Model Building
We trained a **K-Nearest Neighbors (KNN)** classifier using scikit-learn. This simple yet effective model classifies patients based on their proximity to similar cases in the dataset.KNN is a simple, yet powerful algorithm that classifies data points based on their proximity to the nearest neighbors in the feature space.

- **Data Splitting**: 80% training, 20% testing.
- **Hyperparameter Tuning**: Used GridSearchCV to optimize the number of neighbors.
- **Model Accuracy**: Achieved an accuracy of ~85%.

### Model Evaluation
- **Confusion Matrix**: Used to visualize the model's performance.
- **Classification Report**: Displays precision, recall, and F1-score for both classes (Heart Disease vs. No Disease).
- **Model Saving**: The trained model was saved using `pickle` for deployment.

---

## 🛢️ Database Schema and Models

### Tables
1. **Users Table**
   - Stores user information and authentication details.
   - Fields:
     - `id`: Unique identifier (Primary Key)
     - `username`: Unique username
     - `email`: Unique email address
     - `password_hash`: Hashed password
   - **Relationship**: One-to-many relationship with `prediction_history`.

2. **PredictionHistory Table**
   - Stores predictions made by each user.
   - Fields:
     - `id`: Unique identifier (Primary Key)
     - `user_id`: Foreign key referencing the `users` table
     - `age`, `sex`, `chest_pain`, `resting_blood_pressure`, `cholesterol`, etc.: User inputs for predictions
     - `result`: Prediction outcome ("Positive" or "Negative")
     - `timestamp`: Time when the prediction was made

### Model Classes
```python
# User Model
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

# PredictionHistory Model
class PredictionHistory(db.Model):
    __tablename__ = 'prediction_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String, nullable=False)
    chest_pain = db.Column(db.String, nullable=False)
    # Other fields here...
    result = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
```

---

## Requirements
- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login
- Bcrypt
- Scikit-learn
- Docker
- Docker Compose

---

---

## Installation Instructions

### Prerequisites
- **Python 3.x**
- **Docker** and **Docker Compose**

### 👉 Step 1: Clone the Repository
```bash
git clone https://github.com/Ulduzpp/Smart_Web_Nexus.git
cd Smart_Web_Nexus
```

### 👉 Step 2: Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 👉 Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### 👉 Step 4: Run the Application(locally)
```bash
python app.py
```
- Open your browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🐳 Docker Deployment

### Build and Run Docker Container
1. **Build the Docker Image**
   ```bash
   docker build -t smart_web_nexus .
   ```
2. **Run the Docker Container**
   ```bash
   docker run -p 5000:5000 smart_web_nexus
   ```

---

## Team Members
| Role                     | Name                           |
|--------------------------|--------------------------------|
| Frontend Developer       | Fatemeh Habibimoghaddam        |
| Backend Developer        | Ouldouz Pakpour                |
| Database Engineer        | Sahar Abdi                     |
| Machine Learning Engineer| Hanie Fazli                    |
| Docker & MLOps Engineers | Touba Derakhshandeh & Hanie Fazli |

---



## Contributing
We welcome contributions to improve this project! Please fork the repository and submit a pull request.

---

## Demo

https://github.com/user-attachments/assets/a4d073bc-39ef-41a6-bb9f-dfa9a30e7ab2

---
