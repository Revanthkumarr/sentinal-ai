import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import os

# Function to send email
def send_threat_alerts(alerts_path="data/processed/threat_alerts.csv"):
    if not os.path.exists(alerts_path):
        print("✅ No threats to alert.")
        return
    
    df_alerts = pd.read_csv(alerts_path)
    if df_alerts.empty:
        print("✅ No threats to alert.")
        return
    
    # Email Setup
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password_here"  # Note: Use App Passwords for Gmail
    receiver_email = "receiver_email@gmail.com"

    subject = f"🚨 Sentinel AI Threat Alert - {len(df_alerts)} Events Detected"

    # Create email body
    body = "Dear Security Team,\n\n"
    body += f"{len(df_alerts)} high-risk security events were detected by Sentinel AI.\n\n"
    body += "Summary of threats:\n"
    body += df_alerts[['timestamp', 'source_ip', 'risk_score', 'attack_probability']].head(10).to_string(index=False)
    body += "\n\nPlease review immediately.\n\nSentinel AI Security System."

    # Create email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Send Email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # SMTP for Gmail
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("✅ Email Alert Sent Successfully! {msg}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Main
if __name__ == "__main__":
    send_threat_alerts()
