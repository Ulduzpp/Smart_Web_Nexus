import pickle
import warnings
warnings.filterwarnings('ignore')

# Load the saved model
with open('heart_diagnosis_disease_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

def preprocess(features):
    features_processed = list()
    # adding age
    features_processed.append(features['Age'])
    # adding sex
    if features['Sex'] == "Female":
        features_processed.append(0)
    elif features['Sex'] == "Male":
        features_processed.append(1)
    # adding chest pain type
    if features['Chest_Pain'] == "Typical angina":
        features_processed.append(0)
    elif features['Chest_Pain'] == "Atypical angina":
        features_processed.append(1)
    elif features['Chest_Pain'] == "Non-anginal pain":
        features_processed.append(2)
    elif features['Chest_Pain'] == "Asymptomatic":
        features_processed.append(3)
    # adding Resting Blood Pressure
    features_processed.append(features['Trestbps'])
    features_processed.append(features['Chol'])
    if features['Fbs'] == "True":
        features_processed.append(1)
    elif features['Fbs'] == "False":
        features_processed.append(0)
    if features['Fbs'] == "Normal":
        features_processed.append(0)
    elif features['Fbs'] == "Abnormality":
        features_processed.append(1)
    elif features['Fbs'] == "Hypertrophy":
        features_processed.append(2)
    features_processed.append(features['Thalach'])
    if features['Exang'] == "No":
        features_processed.append(0)
    elif features['Exang'] == "Yes":
        features_processed.append(1)
    features_processed.append(features['Oldpeak'])
    if features['Slope'] == "Upsloping":
        features_processed.append(0)
    elif features['Slope'] == "Flat":
        features_processed.append(1)
    elif features['Slope'] == "Downsloping":
        features_processed.append(2)
    features_processed.append(features['Ca'])
    if features['Thal'] == "Normal":
        features_processed.append(0)
    elif features['Thal'] == "Fixed defect":
        features_processed.append(1)
    elif features['Thal'] == "Reversible defect":
        features_processed.append(2)
    elif features['Thal'] == "Not described":
        features_processed.append(3)
    print(f"Before PreProcessing:\n{features}")
    print(f"After PreProcessing:\n{features_processed}")
    return features_processed

def predict_disease(features_dict):
    features = list()
    features = preprocess(features_dict)
    predictions = loaded_model.predict([features])
    if predictions[0] == 1:
        return "Heart Disease"
    else:
        return "No Disease"


if __name__ == '__main__':
    Age = int(input("Please Enter Your Age:\n"))
    Sex = str(input("Are you Male or Female [Male, Female]:\n"))
    Chest_Pain = str(input("Please Enter The Type of Your Chest Pain [Typical angina, Atypical angina, Non-anginal pain, Asymptomatic]:\n"))
    Trestbps = int(input("Please Enter Resting Blood Pressure(resting blood pressure (in mm Hg on admission to the hospital)) [0, 200]:\n"))
    Chol = int(input("Please Enter Cholesterol Measure [0, 603]:\n"))
    Fbs = str(input("Is Fasting Blood Sugar > 120 mg/dl? [True, False]:\n"))
    Restecg = str(input("Please Enter Resting Electrocardiographic Results [Normal, Abnormality, Hypertrophy]:\n"))
    Thalach = int(input("Please Enter your maximum heart rate [60, 202]:\n"))
    Exang = str(input("Is there exist exercise-include angina? [No, Yes]:\n"))
    Oldpeak = float(input("Please Enter ST depression induced by exercise relative to rest [-2.6, 6.2]:\n"))
    Slope = str(input("Please Enter  the slope of the peak exercise ST segment [Upsloping, Flat, Downsloping]:\n"))
    Ca = int(input("Please Enter the number of major vessels (0-4) colored by fluoroscopy:\n"))
    Thal = str(input("Please Enter Patient's Thal level [Normal, Fixed defect, Reversible defect, Not described]:\n"))
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
    #  sample 1:
    # 63, Male, Asymptomatic, 145, 233, True, Normal, 150, No, 2.3, Upsloping, 0, Fixed defect
    # features = [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1] #target=1 false
    # sample 2
    # 69, Female, Asymptomatic, 140, 239, False, Abnormality, 151, No, 1.8, Downsloping, 2, Reversible defect
    # features = [69, 0, 3, 140, 239, 0, 1, 151, 0, 1.8, 2, 2, 2] # target=1 false
    # sample 3
    # 37, Male, Non-anginal pain, 130, 250, False, Abnormality, 187, No, 3.5, Upsloping, 0, Reversible defect
    # features = [37, 1, 2, 130, 250, 0, 1, 187, 0, 3.5, 0, 0, 2] # target=1 false
    # sample 4
    # 41, Female, Atypical angina, 130, 204, False, Normal, 172, No, 1.4, Downsloping, 0, Reversible defect
    # features = [41, 0, 1, 130, 204, 0, 0, 172, 0, 1.4, 2, 0, 2] # target=1 true
    # sample 5
    # 71, Female, Atypical angina, 160, 302, False, Abnormality, 162, No, 0.4, Downsloping, 2, Reversible defect
    # features = [71, 0, 1, 160, 302, 0, 1, 162, 0, 0.4, 2, 2, 2] # target=1 true
    # sample 6
    # 35, Male, Typical angina, 120, 198, False, Abnormality, 130, Yes, 1.6, Flat, 0, Not described
    # features = [35, 1, 0, 120, 198, 0, 1, 130, 1, 1.6, 1, 0, 3] # target=0 true
    # sample 7
    # 52, Male, Typical angina, 125, 212, False, Abnormality, 168, No, 1, Downsloping, 2, Not described
    # features = [52, 1, 0, 125, 212, 0, 1, 168, 0, 1, 2, 2, 3] # target=0 true
    # sample 8
    # 67, Female, Typical angina, 106, 223, False, Abnormality, 142, No, 0.3, Downsloping, 2, Reversible defect
    # features = [67, 0, 0, 106, 223, 0, 1, 142, 0, 0.3, 2, 2, 2] # target=1 true
    # sample 9
    # 60, Male, Non-anginal pain, 140, 185, False, Normal, 155, No, 3, Flat, 0, Reversible defect
    # features = [60, 1, 2, 140, 185, 0, 0, 155, 0, 3, 1, 0, 2] # target=0 true
    # sample 10
    # 42, Female, Typical angina, 102, 265, False, Normal, 122, No, 0.6, Flat, 0, Reversible defect
    # features = [42, 0, 0, 102, 265, 0, 0, 122, 0, 0.6, 1, 0, 2] # target=1 true
    # sample 11
    # 51, Female, Typical angina, 130, 305, False, Abnormality, 142, Yes, 1.2, Flat, 0, Not described
    # features = [51, 0, 0, 130, 305, 0, 1, 142, 1, 1.2, 1, 0, 3] # target=0 true
    # sample 12
    # 39, Male, Typical angina, 118, 219, False, Abnormality, 140, No, 1.2, Flat, 0, Not described
    # features = [39, 1, 0, 118, 219, 0, 1, 140, 0, 1.2, 1, 0, 3] # target=0 true
    # sample 13
    # 68, Male, Typical angina, 144, 193, True, Abnormality, 141, No, 3.4, Flat, 2, Not described
    # features = [68, 1, 0, 144, 193, 1, 1, 141, 0, 3.4, 1, 2, 3] # target=0 true
    print(predict_disease(features= features))