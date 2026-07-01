import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Linux Log Anomaly Detection",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Linux Server Log Anomaly Detection System")
st.markdown("---")

# -------------------------------------------------
# Load Model
# -------------------------------------------------

try:
    model = joblib.load("server_log_anomaly_model.pkl")
    st.success("✅ Model Loaded Successfully")
except Exception as e:
    st.error(f"❌ Error Loading Model:\n\n{e}")
    st.stop()

# -------------------------------------------------
# Upload CSV
# -------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Server Log CSV File",
    type=["csv"]
)

if uploaded_file is None:
    st.info("📂 Please upload a CSV file to begin.")
    st.stop()

# -------------------------------------------------
# Read Dataset
# -------------------------------------------------

try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Unable to read CSV:\n\n{e}")
    st.stop()

st.subheader("📄 Uploaded Dataset")

st.dataframe(df.head())

st.write("Shape:", df.shape)

# -------------------------------------------------
# Required Columns
# -------------------------------------------------

required_columns = [
    "attempts",
    "port",
    "hour",
    "weekday"
]

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(f"❌ Missing Columns: {missing_columns}")
    st.stop()

# -------------------------------------------------
# Prediction
# -------------------------------------------------

X = df[required_columns]

try:
    predictions = model.predict(X)
except Exception as e:
    st.error(f"Prediction Error:\n\n{e}")
    st.stop()

df["anomaly"] = predictions

df["Result"] = df["anomaly"].map({
    1: "Normal",
    -1: "Suspicious"
})

# -------------------------------------------------
# Summary
# -------------------------------------------------

normal_count = (df["anomaly"] == 1).sum()
anomaly_count = (df["anomaly"] == -1).sum()

anomaly_percentage = (anomaly_count / len(df)) * 100

st.subheader("📊 Detection Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Normal Records", normal_count)
col2.metric("Anomalies", anomaly_count)
col3.metric("Anomaly %", f"{anomaly_percentage:.2f}%")

# -------------------------------------------------
# Anomalous Records
# -------------------------------------------------

st.subheader("🚨 Suspicious Records")

anomalies = df[df["anomaly"] == -1]

if anomalies.empty:
    st.success("✅ No anomalies detected.")
else:
    st.dataframe(anomalies)

# -------------------------------------------------
# Visualization
# -------------------------------------------------

st.subheader("📈 Anomaly Visualization")

fig = px.scatter(
    df,
    x="hour",
    y="attempts",
    color="Result",
    hover_data=df.columns,
    title="Anomaly Detection Results"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Download Report
# -------------------------------------------------

csv = anomalies.to_csv(index=False)

st.download_button(
    label="⬇ Download Anomaly Report",
    data=csv,
    file_name="anomaly_report.csv",
    mime="text/csv"
)
