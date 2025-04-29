import pandas as pd
import os
import joblib

# Load model
def load_model(path="models/threat_classifier.pkl"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No model found at {path}")
    model = joblib.load(path)
    return model

# Load scored logs
def load_logs(path="data/processed/scored_event_logs_predictor.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No scored logs found at {path}")
    df = pd.read_csv(path)
    return df

# Make predictions
def predict_threats(df, model):
    # Features the model expects
    X = df[['risk_score', 'hour_of_day', 'is_bot']]
    
    # Predict
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]  # Probability of attack
    
    # Attach predictions to dataframe
    df['predicted_attack'] = predictions
    df['attack_probability'] = probabilities
    
    return df

# Save predicted results
def save_predictions(df, path="data/processed/predicted_event_logs.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ Predictions saved to {path}")

# Create csv filr to save the predictions > 0.5
def generate_alerts(df, threshold_risk=0.6, threshold_prob=0.5, alert_path="data/processed/threat_alerts.csv"):
    alerts = df[
        (df['risk_score'] >= threshold_risk) | 
        (df['attack_probability'] >= threshold_prob)
    ]
    
    if not alerts.empty:
        alerts.to_csv(alert_path, index=False)
        print(f"🚨 {len(alerts)} Threat Alerts generated and saved to {alert_path}")
    else:
        print("✅ No high-risk threats detected.")
    

# Main run
if __name__ == "__main__":
    model = load_model()
    df_logs = load_logs()
    df_predicted = predict_threats(df_logs, model)
    save_predictions(df_predicted)
    generate_alerts(df_predicted)
