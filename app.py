import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Linux Log Anomaly Detection",
    page_icon="🚨",
    layout="wide"
)

# Title
st.title("🚨 Linux Server Log Anomaly Detection System")
st.markdown("---")

# Load Model
try:
    model = joblib.load("server_log_anomaly_model.pkl")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Log CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Show Dataset
    st.subheader("📄 Uploaded Dataset")
    st.dataframe(df.head())

    # Required Columns
    required_columns = [
        "attempts",
        "port",
        "hour",
        "day_of_week"
    ]

    # Check Missing Columns
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        st.error(f"Missing Columns: {missing}")
        st.stop()

    # Features
    X = df[required_columns]

    # Prediction
    predictions = model.predict(X)

    df["anomaly"] = predictions

    # User Friendly Labels
    df["Result"] = df["anomaly"].map({
        1: "Normal",
        -1: "Suspicious"
    })

    # Summary
    normal_count = (df["anomaly"] == 1).sum()
    anomaly_count = (df["anomaly"] == -1).sum()

    st.subheader("📊 Detection Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Normal Records", normal_count)
    col2.metric("Anomalies Detected", anomaly_count)

    anomaly_percentage = (anomaly_count / len(df)) * 100
    col3.metric("Anomaly %", f"{anomaly_percentage:.2f}%")

    # Anomalies Table
    st.subheader("🚨 Anomalous Records")

    anomalies = df[df["anomaly"] == -1]

    if len(anomalies) > 0:
        st.dataframe(anomalies)
    else:
        st.success("No anomalies detected.")

    # Visualization
    st.subheader("📈 Visualization")

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

    # Download Report
    csv = anomalies.to_csv(index=False)

    st.download_button(
        label="⬇ Download Anomaly Report",
        data=csv,
        file_name="anomaly_report.csv",
        mime="text/csv"
    )

else:
    st.info("Upload a CSV file to start anomaly detection.")
