import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
page_title="Linux Log Anomaly Detection",
page_icon="🚨",
layout="wide"
)

st.title("🚨 Linux Server Log Anomaly Detection System")

st.markdown("---")

# Load Model

model = joblib.load("model.pkl")

uploaded_file = st.file_uploader(
"Upload Log CSV File",
type=["csv"]
)

if uploaded_file is not None:

```
df = pd.read_csv(uploaded_file)

st.subheader("📄 Uploaded Dataset")
st.dataframe(df.head())

required_columns = [
    "attempts",
    "port",
    "hour",
    "day_of_week"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"Missing Columns: {missing}")
    st.stop()

X = df[required_columns]

predictions = model.predict(X)

df["anomaly"] = predictions

normal_count = (df["anomaly"] == 1).sum()
anomaly_count = (df["anomaly"] == -1).sum()

st.subheader("📊 Detection Summary")

col1, col2 = st.columns(2)

col1.metric(
    "Normal Records",
    normal_count
)

col2.metric(
    "Anomalies Detected",
    anomaly_count
)

st.subheader("🚨 Anomalous Records")

anomalies = df[df["anomaly"] == -1]

st.dataframe(anomalies)

st.subheader("📈 Visualization")

fig = px.scatter(
    df,
    x="hour",
    y="attempts",
    color=df["anomaly"].astype(str),
    title="Anomaly Detection"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

csv = anomalies.to_csv(index=False)

st.download_button(
    label="⬇ Download Anomaly Report",
    data=csv,
    file_name="anomaly_report.csv",
    mime="text/csv"
)
```

else:
st.info("Upload a CSV file to start anomaly detection.")
