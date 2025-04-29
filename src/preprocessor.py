import pandas as pd
import os

# Load raw logs
def load_raw_logs(path="data/raw/event_logs_predictor.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No raw logs found at {path}")
    df = pd.read_csv(path)
    return df

# Preprocessing function
def preprocess_logs(df):
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Extract hour of day
    df['hour_of_day'] = df['timestamp'].dt.hour
    
    # Create is_bot feature based on user agent
    df['is_bot'] = df['user_agent'].apply(lambda x: 1 if x.lower() == 'bot' else 0)
    
    # Drop rows with missing critical fields (optional)
    df.dropna(subset=['source_ip', 'destination_ip', 'user_agent', 'login_successful', 'attack_flag'], inplace=True)
    
    return df

# Save processed logs
def save_processed_logs(df, path="data/processed/cleaned_event_logs_preditor.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ Cleaned logs saved to {path}")

# Main run
if __name__ == "__main__":
    df_raw = load_raw_logs()
    df_clean = preprocess_logs(df_raw)
    save_processed_logs(df_clean)
