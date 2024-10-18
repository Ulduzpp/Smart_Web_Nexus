# Step 1| Import Libraries
# 1. to handel the data
import pandas as pd
import numpy as np
# 2. To Viusalize the data
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from scipy.stats import boxcox

# 3. To preprocess the data
from sklearn.preprocessing import StandardScaler
# 4. Machine Learning
from sklearn.model_selection import train_test_split,GridSearchCV, cross_val_score
# 5. For Classification task.
from sklearn.neighbors import KNeighborsClassifier
# 6. Metrics
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
# 7. Save Model
import pickle
# 8. Ignore warnings
import warnings
warnings.filterwarnings('ignore')

# Step 2 | Read Dataset
df = pd.read_csv("./assets/dataset/heart.csv")
# print the first 5 rows of the dataset
print(df.head())

# Step 3 | Dataset Overview & Preparation
## Step 3.1 | Rename Variables
# Renamed name of variables to have a better understanding while working on dataset:
df.rename(columns={
    "age":"Age",
    "sex":"Sex",
    "cp":"ChestPain",
    "trestbps":"RestingBloodPressure",
    "chol":"Cholesterol",
    "fbs":"FastingBloodSugar",
    "restecg":"RestingECG",
    "thalach":"MaxHeartRate",
    "exang":"ExcerciseAngina",
    "oldpeak":"OldPeak",
    "slope":"STSlope",
    "ca":"nMajorVessels",
    "thal":"Thalium",
    "target":"Status"
}, inplace=True)
#Changed the integer values of some variables to categorical values based on description of variables:
mappings = {
    'Sex': {
        0: "Female",
        1: "Male"
    },
    'ChestPain': {
        0: "Typical angina",
        1: "Atypical angina",
        2: "Non-anginal pain",
        3: "Asymptomatic"
    },
    "FastingBloodSugar": {
        0:False,
        1:True
    },
    "RestingECG": {
        0:"Normal",
        1:"Abnormality",
        2:"Hypertrophy"
    },
    "ExcerciseAngina": {
        0:"No",
        1:"Yes"
    },
    "STSlope": {
        0:"Upsloping",
        1:"Flat",
        2:"Downsloping"
    },
    "Thalium": {
        0:"Normal",
        1:"Fixed defect",
        2:"Reversible defect",
        3:"Not described"
    },
    "Status": {
        0:"No Disease",
        1:"Heart Disease"
    }
}
def map_values(x, mapping):
    return mapping.get(x, x)
df_copy = df.copy()
for feature, mapping in mappings.items():
    df_copy[feature] = df_copy[feature].map(lambda x: map_values(x, mapping))
    df_copy[feature] = df_copy[feature].astype(object)
print("_" * 100)
print(df.head())
print("_" * 100)
print(df_copy.head())
## Step 3.2 | Basic Information
print("_" * 100)
print(df_copy.info())
print("_" * 100)
print(df_copy.shape)
## Step 3.3 | Statistical Summary
stats_heart_df = df_copy.copy()
# Statistical summary of *********** Numerical Features ************
print("_" * 100)
print("*********** Numerical Features ************")
print(stats_heart_df.describe().T)
# Statistical summary of *********** Categorical Features ************
print("_" * 100)
print("*********** Categorical Features ************")
print(stats_heart_df.describe(include="object").T)
# Step 4 | Exploratary Data Analysis (EDA)
heart_df_eda = df_copy.copy()
def box_hist_plot(feature):
    plt.rcParams['axes.facecolor'] = '#D6F3FF'

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))  # 1 row, 2 columns

    sns.histplot(heart_df_eda[feature], kde=True, color='#45b1e8', ax=axes[0])

    mean_value = heart_df_eda[feature].mean()
    median_value = heart_df_eda[feature].median()
    mode_value = heart_df_eda[feature].mode().values[0] 
    std_value = heart_df_eda[feature].std()
    min_value = heart_df_eda[feature].min()
    max_value = heart_df_eda[feature].max()

    axes[0].axvline(mean_value, color='b', linestyle='-', linewidth=2, label=f'Mean: {mean_value:.2f}')
    axes[0].axvline(median_value, color='r', linestyle='-', linewidth=2, label=f'Median: {median_value:.2f}')
    axes[0].axvline(mode_value, color='m', linestyle='-', linewidth=2, label=f'Mode: {mode_value:.2f}')
    axes[0].axvline(mean_value + std_value, color='b', linestyle='dashed', linewidth=2, label=f'Std +: {std_value:.2f}')
    axes[0].axvline(mean_value - std_value, color='b', linestyle='dashed', linewidth=2, label=f'Std -: {std_value:.2f}')
    axes[0].axvline(min_value, color='orange', linestyle='--', linewidth=2, label=f'Min: {min_value:.2f}')
    axes[0].axvline(max_value, color='orange', linestyle='--', linewidth=2, label=f'Max: {max_value:.2f}')

    axes[0].set_title(f"Histogram")
    axes[0].set_xlabel(feature)
    axes[0].set_ylabel("Density")
    axes[0].legend()

    sns.boxplot(x=heart_df_eda[feature], ax=axes[1], color='#45b1e8')
    axes[1].axvline(mean_value, color='b', linestyle='-', linewidth=2)
    axes[1].axvline(median_value, color='r', linestyle='-', linewidth=2)
    axes[1].axvline(mode_value, color='m', linestyle='-', linewidth=2)
    axes[1].axvline(mean_value + std_value, color='b', linestyle='dashed', linewidth=2)
    axes[1].axvline(mean_value - std_value, color='b', linestyle='dashed', linewidth=2)
    axes[1].axvline(min_value, color='orange', linestyle='--', linewidth=2)
    axes[1].axvline(max_value, color='orange', linestyle='--', linewidth=2)
    axes[1].set_title("Box Plot")
    axes[1].set_xlabel(feature)

    plt.tight_layout()
    plt.title(f"{feature} Histogram and Box Plot")
    plt.savefig(f'./assets/images/{feature}_hist_boxplot.png')
    plt.show()

# find outliers using IQR method
def find_outliers(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier_condition = (data < lower_bound) | (data > upper_bound)
    outliers = data[outlier_condition]
    
    return outliers, lower_bound, upper_bound
outliers = {}
## Step 4.1 | Univariate Analysis
def skewness_dist(df, variable):
    skewness = df[variable].skew()

    print(f"Skewness of the {variable} variable: {skewness:.3f}")

    if skewness > 0:
        print("The distribution is right-skewed.")
    elif skewness < 0:
        print("The distribution is left-skewed.")
    else:
        print("The distribution is approximately symmetric.")
def bar_donut_chart(variable):
    colors = ['#6CB4EE', '#318CE7', '#6495ED', '#87CEFA'] 

    category_counts = heart_df_eda[variable].value_counts()

    fig, axs = plt.subplots(1, 2, figsize=(14, 4)) 

    bars = axs[0].barh(category_counts.index, category_counts.values, color=colors)
    axs[0].set_title(f'{variable} Distribution', fontsize=16)
    axs[0].set_xlabel('Count')
    axs[0].set_ylabel(f'{variable} Types')

    for bar, value in zip(bars, category_counts.values):
        width = bar.get_width()
        axs[0].text(width, bar.get_y() + bar.get_height() / 2, '%d' % int(width),
                    ha='left', va='center', color='black', fontsize=10)

    status_counts = heart_df_eda[variable].value_counts()

    wedges, texts, autotexts = axs[1].pie(status_counts, labels=status_counts.index, colors=colors, autopct='%1.1f%%', startangle=140)

    centre_circle = plt.Circle((0,0),0.70,fc='white')
    plt.gca().add_artist(centre_circle)

    axs[1].axis('equal')

    plt.tight_layout()
    plt.title(f'{variable} Bar and Donut Chart')
    plt.savefig(f'./assets/images/{variable}_donut_chart.png')
    plt.show()

# Feature: Age
box_hist_plot("Age")
print("_" * 100)
skewness_dist(heart_df_eda, "Age")
#Outliers of Age variable
age_outliers, age_lower_bound, age_upper_bound = find_outliers(heart_df_eda['Age'])
print("Lower Bound:", age_lower_bound)
print("Upper Bound:", age_upper_bound)
print("Outliers:", len(age_outliers))
outliers.update({"Age":len(age_outliers)})
#There are no outliers in Age variable.
# Feature: Sex
bar_donut_chart("Sex")
# Feature: ChestPain
bar_donut_chart("ChestPain")
# Feature: RestingBloodPressure
box_hist_plot("RestingBloodPressure")
print("_" * 100)
skewness_dist(heart_df_eda, "RestingBloodPressure")
#Outliers of Resting Blood Pressure column:
rbp_outliers, rbp_lower_bound, rbp_upper_bound = find_outliers(heart_df_eda['RestingBloodPressure'])
print("Lower Bound:", rbp_lower_bound)
print("Upper Bound:", rbp_upper_bound)
print("Outliers:", len(rbp_outliers))
outliers.update({"RestingBloodPressure":len(rbp_outliers)})
# Feature: Cholesterol
box_hist_plot("Cholesterol")
print("_" * 100)
skewness_dist(heart_df_eda, "Cholesterol")
ch_outliers, ch_lower_bound, ch_upper_bound = find_outliers(heart_df_eda['Cholesterol'])
print("Lower Bound:", ch_lower_bound)
print("Upper Bound:", ch_upper_bound)
print("Outliers:", len(ch_outliers))
outliers.update({"Cholesterol":len(ch_outliers)})
# Feature: FastingBloodSugar
bar_donut_chart("FastingBloodSugar")
# Feature: RestingECG
bar_donut_chart("RestingECG")
# Feature: MaxHeartRate
box_hist_plot("MaxHeartRate")
print("_" * 100)
skewness_dist(heart_df_eda, "MaxHeartRate")
ecg_outliers, ecg_lower_bound, ecg_upper_bound = find_outliers(heart_df_eda['MaxHeartRate'])
print("Lower Bound:", ecg_lower_bound)
print("Upper Bound:", ecg_upper_bound)
print("Outliers':", len(ecg_outliers))
outliers.update({"MaxHeartRate":len(ecg_outliers)})
# Feature: ExcerciseAngina
bar_donut_chart("ExcerciseAngina")
# Feature: OldPeak
box_hist_plot("OldPeak")
print("_" * 100)
skewness_dist(heart_df_eda, "OldPeak")
op_outliers, op_lower_bound, op_upper_bound = find_outliers(heart_df_eda['OldPeak'])
print("Lower Bound:", op_lower_bound)
print("Upper Bound:", op_upper_bound)
print("Outliers':", len(op_outliers))
outliers.update({"OldPeak":len(op_outliers)})
# Feature: STSlope
bar_donut_chart("STSlope")
# Feature: nMajorVessels
bar_donut_chart("nMajorVessels")
# Feature: Thalium
bar_donut_chart("Thalium")
# Feature: Status
bar_donut_chart("Status")
print(outliers)
## Step 4.2 | Bivariate Analysis
numerical_features = ['Age', 'RestingBloodPressure', 'Cholesterol', 'MaxHeartRate', 'OldPeak']
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
for i, feature in enumerate(numerical_features):
    row = i // 3
    col = i % 3
    ax = axes[row, col]
    sns.histplot(data=heart_df_eda, x=feature, hue='Status', kde=True, fill=True, ax=ax)
    ax.set_title(f'Distribution of {feature} by Status')
    ax.set_xlabel(feature)
    ax.set_ylabel('Density')
axes[1, 2].remove()
plt.tight_layout()
plt.savefig(f'./assets/images/bivariat_numerical_feature_chart.png')
plt.show()

#Binary & Categorical Variables
categorical_features = ['Sex', 'ChestPain', 'FastingBloodSugar', 'RestingECG', 'ExcerciseAngina', 'STSlope', 'Thalium', 'nMajorVessels']
num_features = len(categorical_features)
num_rows = (num_features - 1) // 3 + 1
num_cols = min(num_features, 3)
fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(14, 14))
for i, feature in enumerate(categorical_features):
    row = i // 3
    col = i % 3
    ax = axes[row, col]

    sns.countplot(data=heart_df_eda, x=feature, hue='Status', ax=ax, palette='Blues')
    ax.set_title(f'Count of {feature} by Status')
    ax.set_xlabel(feature)
    ax.set_ylabel('Count')
    ax.tick_params(axis='x', rotation=20)

    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 5), 
                    textcoords='offset points',
                    color='black')

for i in range(num_rows):
    for j in range(num_cols):
        if i * 3 + j >= num_features:
            fig.delaxes(axes[i, j])

plt.tight_layout()
plt.savefig(f'./assets/images/bivariat_categorical_feature_chart.png')
plt.show()

# Step 5 | Preprocessing
## Step 5.1 | Handling Outliers
outliers_df = pd.DataFrame(list(outliers.items()), columns=['Variable', 'Outliers'])
print("_" * 100)
print(outliers_df)
def box_cox_transform(heart_df):
    transformed_df = heart_df.copy()
    features_to_transform = ["Age", "RestingBloodPressure", "Cholesterol", "MaxHeartRate", "OldPeak"]

    for feature in features_to_transform:
        if np.any(heart_df[feature] <= 0):
            min_value = abs(heart_df[feature].min()) + 1
            heart_df[feature] += min_value
        transformed_feature, lambda_value = boxcox(heart_df[feature])
        transformed_df[feature] = transformed_feature
    return transformed_df

def plot_transform(heart_df, transformed_df, variable):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 6))

    sns.boxplot(x=heart_df[variable], ax=axes[0, 0], color='#00308F') 
    axes[0, 0].set_title(f"Original {variable}")

    sns.boxplot(x=transformed_df[variable], ax=axes[0, 1], color='#7CB9E8') 
    axes[0, 1].set_title(f"Transformed {variable}")

    sns.histplot(heart_df[variable], ax=axes[1, 0], kde=True, color='#00308F')  
    axes[1, 0].set_title(f"Original {variable} Distribution")

    sns.histplot(transformed_df[variable], ax=axes[1, 1], kde=True, color='#7CB9E8') 
    axes[1, 1].set_title(f"Transformed {variable} Distribution")

    plt.tight_layout()
    plt.savefig(f'./assets/images/{variable}_after_transformed_hist_boxplot.png')
    plt.show()
transformed_df = box_cox_transform(df_copy)
# Age variable 
plot_transform(df_copy, transformed_df, 'Age')
print("_" * 100)
skewness_dist(heart_df_eda, "Age")
skewness_dist(transformed_df, "Age")
#Max Heart Rate variable
plot_transform(df_copy, transformed_df, 'MaxHeartRate')
print("_" * 100)
skewness_dist(heart_df_eda, "MaxHeartRate")
skewness_dist(transformed_df, "MaxHeartRate")
ecg_outliers_bc, ecg_lower_bound_bc, ecg_upper_bound_bc = find_outliers(transformed_df['MaxHeartRate'])
print("Lower Bound:", ecg_lower_bound_bc)
print("Upper Bound:", ecg_upper_bound_bc)
print("Outliers:", len(ecg_outliers_bc))
#Resting Blood Pressure variable 
plot_transform(df_copy, transformed_df, 'RestingBloodPressure')
print("_" * 100)
skewness_dist(heart_df_eda, "RestingBloodPressure")
skewness_dist(transformed_df, "RestingBloodPressure")
rbp_outliers_bc, rbp_lower_bound_bc, rbp_upper_bound_bc = find_outliers(transformed_df['RestingBloodPressure'])
print("Lower Bound:", rbp_lower_bound_bc)
print("Upper Bound:", rbp_upper_bound_bc)
print("Outliers:", len(rbp_outliers_bc))
#Cholesterol variable 
plot_transform(df_copy, transformed_df, 'Cholesterol')
print("_" * 100)
skewness_dist(heart_df_eda, "Cholesterol")
skewness_dist(transformed_df, "Cholesterol")
ch_outliers_bc, ch_lower_bound_bc, ch_upper_bound_bc = find_outliers(transformed_df['Cholesterol'])
print("Lower Bound:", ch_lower_bound_bc)
print("Upper Bound:", ch_upper_bound_bc)
print("Outliers:", len(ch_outliers_bc))
# Old Peak variable 
plot_transform(df_copy, transformed_df, 'OldPeak')
print("_" * 100)
skewness_dist(heart_df_eda, "OldPeak")
skewness_dist(transformed_df, "OldPeak")
op_outliers_bc, op_lower_bound_bc, op_upper_bound_bc = find_outliers(transformed_df['OldPeak'])
print("Lower Bound:", op_lower_bound_bc)
print("Upper Bound:", op_upper_bound_bc)
print("Outliers:", len(op_outliers_bc))
transformed = transformed_df.copy()
## Step 5.2 | Missing Values
print("_" * 100)
print("Missing Values")
print(df.isnull().sum())
## Step 5.3 | Duplicated Values
duplicated_rows = df.duplicated()
print("_" * 100)
print(df[duplicated_rows])
print("_" * 100)
print(transformed[duplicated_rows])
df.drop(index=164, axis=0, inplace=True)
transformed.drop(index=164, axis=0, inplace=True)

# Step 6 | Feature Scaling
X = df.drop(["Status"], axis=1)  
y = df["Status"] 
col = list(df.columns.drop("Status"))
sc = StandardScaler()
X[col] = sc.fit_transform(X[col])
print("_" * 100)
print(X.head())
#Splitting the data into the training and testing set  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state= 42, shuffle= True)
print("_" * 100)
print("Shape of Train sets:", X_train.shape)
print("Shape of Test sets:", X_test.shape)
print("Shape of Train set Labels", y_train.shape)
print("Shape of Test set Labels",y_test.shape)
print("_" * 100)
print("Train Label:\n",pd.DataFrame(y_train).value_counts())
print("_" * 100)
print("Test Label:\n",pd.DataFrame(y_test).value_counts())

# Step 7 | Modeling
clf_knn=KNeighborsClassifier()
parametrs_knn={'n_neighbors':[3,5,7, 9, 11], 'metric':['euclidean','manhattan','chebyshev'], 'weights': ['uniform', 'distance']}
grid_clf_knn=GridSearchCV(clf_knn, parametrs_knn, cv=5, n_jobs=-1)
grid_clf_knn.fit(X_train, y_train)
# Conditional check to confirm model training and best estimator selection
if grid_clf_knn.best_estimator_:
    # Save the trained model to a file
    with open('heart_diagnosis_disease_model.pkl', 'wb') as f:
        pickle.dump(grid_clf_knn.best_estimator_, f)
    print("Model saved successfully.")
    best_model_knn=grid_clf_knn.best_estimator_
    y_pred_knn=best_model_knn.predict(X_test)
else:
    print("Model training was not successful; no model to save.")  

ac_knn = accuracy_score(y_test, y_pred_knn)
cr_knn = classification_report(y_test, y_pred_knn)
print("Accuracy score for model " f'{best_model_knn} : ',ac_knn)
print("-" * 100)
print("classification_report for model " f'{best_model_knn} : \n',cr_knn)
# Cross-validation scores for model generalization check

cv_scores = cross_val_score(best_model_knn, X, y, cv=5)
print("Cross-Validation Scores:", cv_scores)
print("Average Cross-Validation Score:", cv_scores.mean())
cm_rnf = confusion_matrix(y_test, y_pred_knn)
# Create the heatmap for confusion matrix
fig = go.Figure(data=go.Heatmap(
                   z=cm_rnf,  # Confusion matrix values
                   x=[False, True],  # Labels for the x-axis (predicted)
                   y=[False, True],  # Labels for the y-axis (actual)
                   hoverongaps=False,
                   colorscale='Oranges'))
# Update layout
fig.update_layout(
    title="Confusion Matrix for Heart Model",
    xaxis_title="Predicted Label",
    yaxis_title="True Label",
    coloraxis_colorbar=dict(title="Count"),
)
# Save the confusion matrix plot as a PNG file
fig.write_image('./assets/images/cm_heart_model.png')
# Show the plot
fig.show()