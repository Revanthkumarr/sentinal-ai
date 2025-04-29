import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load scored logs
def load_scored_logs(path="data/processed/scored_event_logs.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No scored logs found at {path}")
    df = pd.read_csv(path)
    return df

# Model Training
def train_threat_classifier(df):
    # Feature columns
    X = df[['risk_score', 'hour_of_day', 'is_bot']]
    y = df['attack_flag']

    # Split into train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model
    model = LogisticRegression(class_weight='balanced')
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print("\n=== Model Evaluation ===")
    print(classification_report(y_test, y_pred))

    return model

# Save model
def save_model(model, path="models/threat_classifier.pkl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"✅ Model saved to {path}")

# Main run
if __name__ == "__main__":
    df_scored = load_scored_logs()
    model = train_threat_classifier(df_scored)
    save_model(model)
