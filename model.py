import pickle

# Load the saved model
with open('heart_diagnosis_disease_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

def predict_price(features):
    predictions = loaded_model.predict([features])
    return predictions[0]

if __name__ == '__main__':
    Age = int(input("Please Enter Your Age:\n"))
    Sex = str(input("Are you Male or Female [Male/Fmale]:\n"))
    Chest_Pain = str(input("Please Enter The Type of Your Chest Pain [Typical Angina, Atypical Angina, Non-Anginal, Asymptomatic]:\n"))
    Trestbps = int(input("Please Enter Resting Blood Pressure(resting blood pressure (in mm Hg on admission to the hospital)) [0, 200]:\n"))
    Chol = int(input("Please Enter Cholesterol Measure [0, 603]:\n"))
    Fbs = str(input("Is Fasting Blood Sugar > 120 mg/dl? [True/False]:\n"))
    Restecg = str(input("Please Enter Resting Electrocardiographic Results [Normal, Stt abnormality, Hypertrophy]:\n"))
    # Thalach