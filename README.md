# Heart Disease Prediction Web Application

## Overview
The Heart Disease Prediction Web Application is designed to help users assess their likelihood of heart disease based on user-inputted health data.It leverages machine learning models to deliver accurate predictions and insights, allowing users to make informed health decisions.The app utilizes Flask for the backend, along with Bootstrap, HTML, and CSS for the frontend to create a responsive and user-friendly interface.

## Access the App
Open http://http://188.121.99.111:5000 in your browser to access the app.

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

## Docker
### 1. Clone the repository
- https://github.com/Ulduzpp/Smart_Web_Nexus.git
- cd Smart_Web_Nexus
### 2. Build the docker image
- docker build -t smart_web_nexus .
### 3. Run the docker container
- docker run -p 5000:5000 smart_web_nexus

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
- Touba Derakhshandeh: **Dockerization**
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
