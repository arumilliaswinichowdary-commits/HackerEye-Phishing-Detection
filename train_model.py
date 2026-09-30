import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from feature_extraction import extract_features

print("=" * 50)
print("HackerEye AI Model Training Started...")
print("=" * 50)

# ---------------- LOAD DATASET ----------------

print("Loading dataset...")

df = pd.read_csv("dataset.csv")

print("Original Dataset Shape:", df.shape)

# Use only 50,000 rows for faster training
df = df.sample(n=50000, random_state=42)

print("Training Dataset Shape:", df.shape)

# ---------------- FEATURE EXTRACTION ----------------

print("Extracting URL features...")

X = df["URL"].apply(extract_features)

X = pd.DataFrame(X.tolist())

print("Feature Extraction Completed!")

# ---------------- LABELS ----------------

print("Preparing labels...")

y = df["Label"].map({
    "good": 0,
    "bad": 1
})

# ---------------- TRAIN TEST SPLIT ----------------

print("Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ---------------- MODEL ----------------

print("Training Random Forest Model...")

model = RandomForestClassifier(
    n_estimators=50,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Model Training Completed!")

# ---------------- EVALUATION ----------------

pred = model.predict(X_test)
accuracy = accuracy_score(y_test, pred)

print("=" * 50)
print(f"Accuracy : {accuracy:.4f}")
print(f"Features : {model.n_features_in_}")
print("=" * 50)

# ---------------- SAVE MODEL ----------------

joblib.dump(model, "model_small.pkl", compress=3)

print("Model Saved Successfully!")
print("=" * 50)
print("Training Finished Successfully!")
print("=" * 50)