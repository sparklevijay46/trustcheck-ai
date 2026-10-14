
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# 1. Load dataset
print("Loading dataset...")

df = pd.read_csv("data/jobs.csv")

# 2. Select text columns that exist in the dataset
text_columns = [
    "title",
    "location",
    "department",
    "company_profile",
    "description",
    "requirements",
    "benefits",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function"
]

# Replace missing text with empty strings
for column in text_columns:
    df[column] = df[column].fillna("").astype(str)

# Combine the job fields
df["job_text"] = df[text_columns].agg(" ".join, axis=1)

# 3. Prepare target labels
df = df.dropna(subset=["fraudulent"])
df = df[df["fraudulent"].isin([0, 1])]

X = df["job_text"]
y = df["fraudulent"].astype(int)

print("Dataset shape:", df.shape)
print("Legitimate jobs:", int((y == 0).sum()))
print("Fraudulent jobs:", int((y == 1).sum()))

# 4. Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 5. Build the machine-learning pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            max_features=50000,
            ngram_range=(1, 2),
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42
        )
    )
])

# 6. Train
print("\nTraining model...")
model.fit(X_train, y_train)
print("Training completed!")

# 7. Evaluate
print("\nEvaluating model...")
predictions = model.predict(X_test)

print(
    "\nAccuracy:",
    f"{accuracy_score(y_test, predictions) * 100:.2f}%"
)

print("\nClassification report:")
print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Legitimate", "Fraudulent"],
        zero_division=0
    )
)

print("Confusion matrix:")
print(confusion_matrix(y_test, predictions, labels=[0, 1]))

# 8. Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/fake_job_detector.pkl")

print("\nModel saved successfully!")
print("File: models/fake_job_detector.pkl")
