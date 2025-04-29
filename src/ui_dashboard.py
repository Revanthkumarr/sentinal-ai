import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load Data
def load_data():
    path = "data/processed/predicted_event_logs.csv"
    if not os.path.exists(path):
        st.error("No predicted events found. Please run predictions first!")
        return None
    return pd.read_csv(path)

def load_alerts():
    path = "data/processed/threat_alerts.csv"
    if not os.path.exists(path):
        return pd.DataFrame()  # Return empty if no alerts
    return pd.read_csv(path)

# Streamlit UI
st.set_page_config(page_title="Sentinel AI Threat Monitoring", layout="wide")
st.title("🛡️ Sentinel AI Threat Monitoring Dashboard")

# Load data
df_events = load_data()
df_alerts = load_alerts()

if df_events is not None:
    # KPIs
    total_events = len(df_events)
    total_attacks_predicted = df_events['predicted_attack'].sum()
    high_risk_events = len(df_events[df_events['risk_score'] >= 0.6])
    
    st.metric(label="🔢 Total Events Processed", value=total_events)
    st.metric(label="🚨 Attacks Predicted", value=total_attacks_predicted)
    st.metric(label="⚡ High Risk Events", value=high_risk_events)

    st.divider()

    # Risk color styling function
def color_risk(val):
    if val >= 0.7:
        color = 'background-color: red; color: white'
    elif val >= 0.4:
        color = 'background-color: orange; color: black'
    else:
        color = 'background-color: lightgreen; color: black'
    return color

# Show Event Logs with color coding
st.subheader("📜 Event Logs (Risk Level Color Coded)")
styled_df = df_events[['timestamp', 'source_ip', 'destination_ip', 'risk_score', 'attack_probability', 'predicted_attack']].style.applymap(color_risk, subset=['risk_score'])
st.dataframe(styled_df, use_container_width=True)

# Send email button
if not df_alerts.empty:
    if st.button("📩 Send Threat Alert Email Now"):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # Email setup
        sender_email = "your_email@gmail.com"
        sender_password = "your_app_password"
        receiver_email = "receiver_email@gmail.com"
        
        subject = f"🚨 Sentinel AI Threat Alert - {len(df_alerts)} Events Detected"

        body = "High-risk events detected:\n\n"
        body += df_alerts[['timestamp', 'source_ip', 'risk_score', 'attack_probability']].head(10).to_string(index=False)
        body += "\n\nPlease check immediately."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            st.success("✅ Email alert sent successfully!")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")

# Risk Distribution Chart
st.subheader("📊 Risk Score Distribution")

fig, ax = plt.subplots(figsize=(5, 3))
df_events['risk_score'].hist(bins=10, edgecolor='black', ax=ax)
ax.set_xlabel('Risk Score')
ax.set_ylabel('Number of Events')
ax.set_title('Distribution of Risk Scores')
st.pyplot(fig)


st.sidebar.subheader("📥 Upload Custom Event Logs")

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df_events = pd.read_csv(uploaded_file)
    st.success("✅ Custom event logs loaded!")


#     st.divider()

#     # Threat Alerts Section
#     st.subheader("🚨 Active Threat Alerts")

#     if not df_alerts.empty:
#         st.dataframe(df_alerts[['timestamp', 'source_ip', 'risk_score', 'attack_probability']], use_container_width=True)
#     else:
#         st.success("✅ No active high-risk threats at this time!")
# else:
#     st.warning("Please generate prediction logs to view dashboard.")
