import pickle
import warnings
warnings.filterwarnings('ignore')

# Load the saved model
with open('heart_diagnosis_disease_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

def predict_price(features):
    predictions = loaded_model.predict([features])
    if predictions[0] == 1:
        return "Heart Disease"
    else:
        return "No Disease"

if __name__ == '__main__':
    Age = int(input("Please Enter Your Age:\n"))
    Sex = str(input("Are you Male or Female [Male/Female]:\n"))
    Chest_Pain = str(input("Please Enter The Type of Your Chest Pain [Typical angina, Atypical angina, Non-anginal pain, Asymptomatic]:\n"))
    Trestbps = int(input("Please Enter Resting Blood Pressure(resting blood pressure (in mm Hg on admission to the hospital)) [0, 200]:\n"))
    Chol = int(input("Please Enter Cholesterol Measure [0, 603]:\n"))
    Fbs = str(input("Is Fasting Blood Sugar > 120 mg/dl? [True/False]:\n"))
    Restecg = str(input("Please Enter Resting Electrocardiographic Results [Normal, Abnormality, Hypertrophy]:\n"))
    Thalach = int(input("Please Enter your maximum heart rate [60, 202]:\n"))
    Exang = str(input("Is there exist exercise-include angina? [No/Yes]:\n"))
    Oldpeak = float(input("Please Enter ST depression induced by exercise relative to rest [-2.6, 6.2]:\n"))
    Slope = str(input("Please Enter  the slope of the peak exercise ST segment [Upsloping, Flat, Downsloping]:\n"))
    Ca = int(input("Please Enter the number of major vessels (0-4) colored by fluoroscopy:\n"))
    Thal = str(input("Please Enter Patient's Thal level [Normal/Fixed defect/Reversible defect/Not described]:\n"))
    features = []
    # adding age
    features.append(Age)
    # adding sex
    if Sex == "Female":
        features.append(0)
    elif Sex == "Male":
        features.append(1)
    # adding chest pain type
    if Chest_Pain == "Typical angina":
        features.append(0)
    elif Chest_Pain == "Atypical angina":
        features.append(1)
    elif Chest_Pain == "Non-anginal pain":
        features.append(2)
    elif Chest_Pain == "Asymptomatic":
        features.append(3)
    # adding Resting Blood Pressure
    features.append(Trestbps)
    features.append(Chol)
    if Fbs == "True":
        features.append(1)
    elif Fbs == "False":
        features.append(0)
    if Restecg == "Normal":
        features.append(0)
    elif Restecg == "Abnormality":
        features.append(1)
    elif Restecg == "Hypertrophy":
        features.append(2)
    features.append(Thalach)
    if Exang == "No":
        features.append(0)
    elif Exang == "Yes":
        features.append(1)
    features.append(Oldpeak)
    if Slope == "Upsloping":
        features.append(0)
    elif Slope == "Flat":
        features.append(1)
    elif Slope == "Downsloping":
        features.append(2)
    features.append(Ca)
    if Thal == "Normal":
        features.append(0)
    elif Thal == "Fixed defect":
        features.append(1)
    elif Thal == "Reversible defect":
        features.append(2)
    elif Thal == "Not described":
        features.append(3)
    print(features)
    
    # Example
    # 63, Male, Asymptomatic, 145, 233, True, Normal, 150, No, 2.3, Upsloping, 0, Fixed defect
    # features = [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1] #target=1 false
    # 69, Female, Asymptomatic, 140, 239, False, Abnormality, 151, No, 1.8, Downsloping, 2, Reversible defect
    # features = [69, 0, 3, 140, 239, 0, 1, 151, 0, 1.8, 2, 2, 2] # target=1 false
    # 37, Male, Non-anginal pain, 130, 250, False, Abnormality, 187, No, 3.5, Upsloping, 0, Reversible defect
    # features = [37, 1, 2, 130, 250, 0, 1, 187, 0, 3.5, 0, 0, 2] # target=1 false
    # features = [41, 0, 1, 130, 204, 0, 0, 172, 0, 1.4, 2, 0, 2] # target=1 true
    # features = [71, 0, 1, 160, 302, 0, 1, 162, 0, 0.4, 2, 2, 2] # target=1 true
    # features = [35, 1, 0, 120, 198, 0, 1, 130, 1, 1.6, 1, 0, 3] # target=0 true
    # features = [52, 1, 0, 125, 212, 0, 1, 168, 0, 1, 2, 2, 3] # target=0 true
    # features = [67, 0, 0, 106, 223, 0, 1, 142, 0, 0.3, 2, 2, 2] # target=1 true
    # features = [60, 1, 2, 140, 185, 0, 0, 155, 0, 3, 1, 0, 2] # target=0 true
    # features = [42, 0, 0, 102, 265, 0, 0, 122, 0, 0.6, 1, 0, 2] # target=1 true
    # features = [51, 0, 0, 130, 305, 0, 1, 142, 1, 1.2, 1, 0, 3] # target=0 true
    # features = [39, 1, 0, 118, 219, 0, 1, 140, 0, 1.2, 1, 0, 3] # target=0 true
    features = [68, 1, 0, 144, 193, 1, 1, 141, 0, 3.4, 1, 2, 3] # target=0 true
    print(predict_price(features= features))