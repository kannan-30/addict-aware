"""
Antigravity - Addict Aware
ML Model: Random Forest for Addiction Prediction

Trains and manages the Random Forest classifier for predicting
digital addiction levels (Low / Medium / High).
"""
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

MODEL_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(MODEL_DIR, 'addiction_model.pkl')
ENCODER_PATH = os.path.join(MODEL_DIR, 'label_encoder.pkl')
DATASET_PATH = os.path.join(MODEL_DIR, 'addiction_dataset.csv')

# Feature columns
FEATURES = ['screen_time', 'phone_pickups', 'social_media_time']
TARGET = 'addiction_level'


def train_model():
    """
    Train the Random Forest model on the addiction dataset.
    Returns model performance metrics.
    """
    # Load dataset
    if not os.path.exists(DATASET_PATH):
        from models.generate_dataset import generate_dataset
        generate_dataset()

    df = pd.read_csv(DATASET_PATH)

    # Prepare features and labels
    X = df[FEATURES].values
    le = LabelEncoder()
    y = le.fit_transform(df[TARGET])

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=le.classes_, output_dict=True)

    # Save model and encoder
    joblib.dump(model, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)

    metrics = {
        'accuracy': round(accuracy * 100, 2),
        'report': report,
        'samples_used': len(df),
        'trained_at': datetime.utcnow().isoformat(),
        'feature_importance': dict(zip(FEATURES, model.feature_importances_.tolist()))
    }

    print(f"[✓] Model trained — Accuracy: {metrics['accuracy']}%")
    print(f"    Feature Importance: {metrics['feature_importance']}")

    return metrics


def predict_addiction(screen_time, phone_pickups, social_media_time):
    """
    Predict addiction level for given user inputs.

    Args:
        screen_time: Hours per day on screens
        phone_pickups: Number of phone pickups per day
        social_media_time: Hours per day on social media

    Returns:
        dict with addiction_level, addiction_score, probabilities
    """
    # Load model
    if not os.path.exists(MODEL_PATH):
        print("[!] Model not found. Training now...")
        train_model()

    model = joblib.load(MODEL_PATH)
    le = joblib.load(ENCODER_PATH)

    # Prepare input
    features = np.array([[screen_time, phone_pickups, social_media_time]])

    # Predict
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    # Decode label
    addiction_level = le.inverse_transform([prediction])[0]

    # Calculate addiction score (0-100)
    # Weighted: High probability → higher score
    class_names = le.classes_.tolist()
    score_weights = {'Low': 20, 'Medium': 55, 'High': 90}
    addiction_score = sum(
        probabilities[i] * score_weights.get(class_names[i], 50)
        for i in range(len(class_names))
    )
    addiction_score = round(min(100, max(0, addiction_score)), 1)

    return {
        'addiction_level': addiction_level,
        'addiction_score': addiction_score,
        'probabilities': {
            class_names[i]: round(probabilities[i] * 100, 2)
            for i in range(len(class_names))
        }
    }


def get_model_info():
    """Get information about the current trained model"""
    if not os.path.exists(MODEL_PATH):
        return {'status': 'not_trained', 'message': 'Model has not been trained yet.'}

    model = joblib.load(MODEL_PATH)
    le = joblib.load(ENCODER_PATH)

    return {
        'status': 'trained',
        'n_estimators': model.n_estimators,
        'max_depth': model.max_depth,
        'classes': le.classes_.tolist(),
        'feature_importance': dict(zip(FEATURES, model.feature_importances_.tolist())),
        'n_features': model.n_features_in_
    }


if __name__ == '__main__':
    # Train and test
    metrics = train_model()
    print("\n--- Test Predictions ---")
    print("Low user:", predict_addiction(1.5, 15, 0.5))
    print("Medium user:", predict_addiction(5.0, 55, 2.5))
    print("High user:", predict_addiction(10.0, 100, 6.0))
