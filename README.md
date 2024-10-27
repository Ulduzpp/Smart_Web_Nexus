# Heart Disease Prediction Web Application

## Overview
The Heart Disease Prediction Web Application is designed to help users assess their likelihood of heart disease based on user-inputted health data.
It leverages machine learning models to deliver accurate predictions and insights, allowing users to make informed health decisions.The app utilizes Flask for the backend, along with Bootstrap, HTML, and CSS for the frontend to create a responsive and user-friendly interface.


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


## Objective

The goal of this project is to collaboratively develop a smart web application that:
- Integrates a machine learning model for heart disease prediction.
- Implements user registration and authentication systems using a database.
- Containerizes the application with Docker and deploys it using Docker Swarm on a cloud-based host.


## Team Structure

The Nexus team consists of 5 members, each assigned specific tasks to contribute:

- Part 1: Frontend Development (Team Member 1: FatemehHabibimoghaddam)
- Role: **Frontend Developer**
- Part 2: Backend Development and Authentication (Team Member 2: Ouldouz Pakpour)
- Role: **Backend Developer**
- Part 3: Database Integration (Team Member 3: Sahar_Abdi)
- Role: **Database Engineer**
- Part 4: Machine Learning Model (Team Member 4: Hanie Fazli)
- Role: **Machine Learning Engineer**
- Part 5: Containerization and Deployment (Team Members 4 & 5: Hanie Fazli & Touba Derakhshandeh)
- Role: **MLOps Engineer Engineer**


## Project Structure
Heart Disease Prediction Web Application
- │   ├── assets
- │   │   ├── dataset
- │   │   ├── images
- │   │   ├── heart_disease_diagnosis_model.ipynb
- │   │   ├── heart_disease_diagnosis_model.py
- │   ├── instance 
- │   │   ├── Heart_Disease_Diagnosis.db
- │   ├── static 
- │   │   ├── css
- │   │   │  └── style.css
- │   │   ├── images
- │   │   │  ├── Error_401.webp
- │   │   │  ├── Error_403.webp
- │   │   │  ├── Error_404.webp
- │   │   │  ├── Error_500.webp
- │   │   │  ├── Heart_Disease.webp
- │   │   │  ├── No_Disease.webp
- │   │   │  ├── Logo.webp
- │   │   │  ├── smart_app.webp
- │   ├── templates/
- │   │   ├── base_error.html
- │   │   ├── base.html
- │   │   ├── error_401.html
- │   │   ├── error_403.html
- │   │   ├── error_404.html
- │   │   ├── error_500.html
- │   │   ├── history.html
- │   │   ├── home.html
- │   │   ├── input.html
- │   │   ├── login.html
- │   │   ├── profile.html
- │   │   ├── register.html
- │   │   └── result.html
- │   ├── .gitignore
- │   ├── app.py
- │   ├── form.py
- │   ├── heart_disease_diagnosis_model.pkl
- │   ├── members.txt
- │   ├── model.py 
- │   ├── README.md
- │   ├── requirements.txt
- │   ├── Dockerfile
    └── docker-compose.yml


### Requirements
- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login
- Bcrypt
- Scikit-learn
- Docker
- Docker Compose

 
## Installation

1. Clone the repository:
git clone https://github.com/Ulduzpp/Smart_Web_Nexus.git

2. Navigate to the project directory:
cd heart-disease-prediction-app

3. Install the required packages:
pip install -r requirements.txt


## Usage

1. Run the application:
python app.py

2. Open your web browser and go to http://127.0.0.1:5000.
