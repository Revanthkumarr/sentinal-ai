import pandas as pd
import os

# Load cleaned logs
def load_clean_logs(path="data/processed/cleaned_event_logs.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No cleaned logs found at {path}")
    df = pd.read_csv(path)
    return df

# Risk scoring function
def calculate_risk(df):
    scores = []
    for index, row in df.iterrows():
        risk = 0

        # Rule 1: Login at night (00:00 - 05:00) => +0.4 risk
        if row['hour_of_day'] <= 5:
            risk += 0.4
        
        # Rule 2: Login failed => +0.3 risk
        if row['login_successful'] == 0:
            risk += 0.3
        
        # Rule 3: User agent is bot => +0.3 risk
        if row['is_bot'] == 1:
            risk += 0.3

        # Cap risk at 1
        risk = min(risk, 1.0)
        
        scores.append(risk)

    df['risk_score'] = scores
    return df

# Save scored logs
def save_scored_logs(df, path="data/processed/scored_event_logs_predictor.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ Risk scored logs saved to {path}")

# Main run
if __name__ == "__main__":
    df_clean = load_clean_logs()
    df_scored = calculate_risk(df_clean)
    save_scored_logs(df_scored)
