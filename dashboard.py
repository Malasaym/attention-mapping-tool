import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_autorefresh import st_autorefresh
import time
DATA_FILE = "data/attention_log.csv"

st.title("Offline Human Attention Mapping Dashboard")

st_autorefresh(interval=60000,key="refresh")
try:
    df = pd.read_csv(DATA_FILE)
except:
    st.warning("Run tracker.py first to collect data.")
    st.stop()


#df["timestamp"] = pd.to_datetime(df["timestamp"])
df = pd.read_csv(DATA_FILE)

# Remove duplicate header rows
df = df[df["timestamp"] != "timestamp"]

# Convert timestamps safely
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Drop rows with invalid timestamps
df = df.dropna(subset=["timestamp"])
df["minute"] = df["timestamp"].dt.floor("20s")


st.subheader("Attention Heatmap Over Time")

heatmap_data = df.groupby(
    ["minute", "attention_state"]
).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(10,5))

sns.heatmap(
    heatmap_data.T,
    cmap="viridis",
    linewidths=0.5,
    ax=ax
)

ax.set_xlabel("Time")
ax.set_ylabel("Attention State")

st.pyplot(fig)


st.subheader("Focus Fragmentation")

switch_count = (df["event"] == "window_switch").sum()

st.write("Window switches detected:", switch_count)

if switch_count > 20:
    st.warning("High attention fragmentation")

elif switch_count > 10:
    st.info("Moderate attention fragmentation")

else:
    st.success("Low attention fragmentation")


import numpy as np

st.subheader("GitHub-Style Attention Activity")

df["date"] = df["timestamp"].dt.date

daily_activity = df.groupby("date").size()

date_range = pd.date_range(daily_activity.index.min(), daily_activity.index.max())

daily_activity = daily_activity.reindex(date_range, fill_value=0)

values = daily_activity.values

weeks = int(np.ceil(len(values) / 7))

grid = np.zeros((7, weeks))

for i, val in enumerate(values):
    row = i % 7
    col = i // 7
    grid[row, col] = val

fig2, ax2 = plt.subplots(figsize=(10,3))

sns.heatmap(
    grid,
    cmap="YlGn",
    linewidths=1,
    linecolor="white",
    cbar=False,
    ax=ax2
)

ax2.set_title("Daily Attention Activity")
ax2.set_xlabel("Week")
ax2.set_ylabel("Day")

st.pyplot(fig2)


st.subheader("Raw Interaction Data")

st.dataframe(df)
st.subheader("application use")
app_usage=df["window"].value_counts().head(20)
st.bar_chart(app_usage)