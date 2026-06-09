import joblib

model = joblib.load("model.pkl")

print("Features expected:", model.n_features_in_)