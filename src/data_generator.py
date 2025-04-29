import random
import pandas as pd
from datetime import datetime, timedelta

# Configuration
NUM_EVENTS = 1000  # How many events to generate
ATTACK_PROBABILITY = 0.05  # 5% of events are attacks

# Sample IP address generator
def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

# Sample user agents
USER_AGENTS = ['Chrome', 'Firefox', 'Edge', 'Safari', 'Bot']

# Generate events
def generate_event_logs(num_events=NUM_EVENTS):
    logs = []
    current_time = datetime.now()
    
    for _ in range(num_events):
        time_delta = timedelta(seconds=random.randint(10, 600))  # 10 seconds to 10 minutes gap
        current_time += time_delta

        event = {
            'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
            'source_ip': random_ip(),
            'destination_ip': random_ip(),
            'user_agent': random.choice(USER_AGENTS),
            'login_successful': random.choices([1, 0], weights=[0.95, 0.05])[0],  # Most logins succeed
            'attack_flag': random.choices([1, 0], weights=[ATTACK_PROBABILITY, 1-ATTACK_PROBABILITY])[0]
        }
        logs.append(event)
    
    return pd.DataFrame(logs)

# Save to CSV
def save_logs(df, path="data/raw/event_logs_predictor.csv"):
    df.to_csv(path, index=False)
    print(f"✅ Generated {len(df)} logs and saved to {path}")

# Main run
if __name__ == "__main__":
    df = generate_event_logs()
    save_logs(df)
