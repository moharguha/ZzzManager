# sleep_tracker_app.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt

# CSV file to store logs
LOG_FILE = "sleep_log.csv"

# Create file if not exists
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["Date", "Start", "End", "Hours"]).to_csv(LOG_FILE, index=False)

# Load data
df = pd.read_csv(LOG_FILE)

# Global variable for sleep start
if "sleep_time" not in st.session_state:
    st.session_state.sleep_time = None

st.title("😴 Sleep Tracker App")

# ---------------- Buttons ---------------- #
if st.button("🌙 Start Sleep"):
    st.session_state.sleep_time = datetime.now()
    st.success(f"Sleep started at {st.session_state.sleep_time.strftime('%H:%M:%S')}")

if st.button("🌞 End Sleep"):
    if st.session_state.sleep_time is None:
        st.warning("Start sleep first!")
    else:
        wake_time = datetime.now()
        hours = (wake_time - st.session_state.sleep_time).total_seconds() / 3600

        # Save to CSV
        new_row = {
            "Date": wake_time.strftime("%Y-%m-%d"),
            "Start": st.session_state.sleep_time.strftime("%H:%M:%S"),
            "End": wake_time.strftime("%H:%M:%S"),
            "Hours": round(hours, 2)
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(LOG_FILE, index=False)

        st.success(f"🌞 You slept {hours:.2f} hours")

        if hours < 7:
            st.error("⚠️ Less than 7 hours! Try to sleep earlier tonight.")

        # Reset
        st.session_state.sleep_time = None

# ---------------- Show Stats ---------------- #
st.subheader("📊 Last 7 Sleep Records")

if df.empty:
    st.info("No data yet. Start tracking your sleep!")
else:
    last7 = df.tail(7)
    st.dataframe(last7)

    avg = df["Hours"].mean()
    st.write(f"**Average sleep duration:** {avg:.2f} hrs")

    # Plot graph
    fig, ax = plt.subplots()
    ax.plot(last7["Date"], last7["Hours"], marker="o", linestyle="-", color="b")
    ax.axhline(7, color="r", linestyle="--", label="Recommended 7 hrs")
    ax.set_title("Sleep Duration (Last 7 Days)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Hours Slept")
    ax.legend()
    st.pyplot(fig)

st.markdown("---")
st.caption("⚠️ This is a demo app, not a medical tool. Consult a doctor for sleep issues.")