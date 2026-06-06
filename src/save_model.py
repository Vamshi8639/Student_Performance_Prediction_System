import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_excel(
    "data/student_data.csv.xlsx"
)

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

X = df[
[
'Attendance',
'Assignment_Score',
'MET_Score',
'Project_Completed'
]
]

y = df[
'Placement_Status'
]

model = LogisticRegression()

model.fit(X,y)

joblib.dump(
    model,
    "models/placement_model.pkl"
)

print("Model Saved Successfully")