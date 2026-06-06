import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df = pd.read_excel(
    "data/student_data.csv.xlsx"
)

# Convert text to numbers

df['Project_Completed'] = df[
    'Project_Completed'
].map({
    'Yes':1,
    'No':0
})

df['Placement_Status'] = df[
    'Placement_Status'
].map({
    'Placed':1,
    'Not Placed':0
})

# Features

X = df[
[
'Attendance',
'Assignment_Score',
'MET_Score',
'Project_Completed'
]
]

# Target

y = df['Placement_Status']

# Split Data

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model

model = LogisticRegression()

model.fit(
    X_train,
    y_train
)

# Predict

y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("Model Trained Successfully")

print("Accuracy:")

print(round(
    accuracy*100,
    2
),"%")
import pandas as pd

student = pd.DataFrame(
    [[90,85,88,1]],
    columns=[
        'Attendance',
        'Assignment_Score',
        'MET_Score',
        'Project_Completed'
    ]
)

result = model.predict(student)