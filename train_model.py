from sklearn.ensemble import RandomForestClassifier
import joblib

X = [
    [18,1,0,1,0],
    [20,1,0,1,0],
    [25,1,0,2,0],
    [90,0,1,5,1],
    [100,0,1,6,1],
    [120,0,1,8,1],
    [80,0,1,4,1],
    [30,1,0,2,0]
]

y = [0,0,0,1,1,1,1,0]

model = RandomForestClassifier(n_estimators=100)

model.fit(X,y)

joblib.dump(model,"model.pkl")

print("Model Trained Successfully!")