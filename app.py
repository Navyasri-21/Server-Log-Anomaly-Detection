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
# Load Model + Encoders
# -------------------------------------------------
try:
    model = joblib.load("server_log_anomaly_model.pkl")
    encoders = joblib.load("encoders.pkl")
    onehot_encoder = encoders["onehot_encoder"]
    scaler = encoders["standard_scaler"]
    st.success("✅ Model & Encoders Loaded Successfully")
except Exception as e:
    st.error(f"❌ Error Loading Model/Encoders:\n\n{e}")
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
# Required RAW Columns (before feature engineering)
# -------------------------------------------------
required_raw_columns = [
    "timestamp",
    "city",
    "service",
    "attempts",
    "status",
    "port",
    "protocol"
]
missing_columns = [
    col for col in required_raw_columns if col not in df.columns
]
if missing_columns:
    st.error(f"❌ Missing Columns: {missing_columns}")
    st.stop()

# -------------------------------------------------
# Feature Engineering (must match training notebook exactly)
# -------------------------------------------------
try:
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.day
    df["month"] = df["timestamp"].dt.month
    df["weekday"] = df["timestamp"].dt.dayofweek

    categorical_cols = ["city", "service", "status", "protocol"]

    encoded = onehot_encoder.transform(df[categorical_cols])
    encoded_df = pd.DataFrame(
        encoded,
        columns=onehot_encoder.get_feature_names_out(categorical_cols)
    )

    model_df = df.drop(columns=categorical_cols + ["timestamp"])
    # drop any leftover cols not used in training, if present
    for extra_col in ["source_ip", "username"]:
        if extra_col in model_df.columns:
            model_df = model_df.drop(columns=[extra_col])

    model_df = pd.concat(
        [model_df.reset_index(drop=True), encoded_df.reset_index(drop=True)],
        axis=1
    )

    # Scale using the SAME scaler fitted during training
    scaled = scaler.transform(model_df)
    X = pd.DataFrame(scaled, columns=model_df.columns)

except Exception as e:
    st.error(f"Feature Engineering Error:\n\n{e}")
    st.stop()

# -------------------------------------------------
# Prediction
# -------------------------------------------------
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
    hover_data=[c for c in df.columns if c not in ["timestamp"]],
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
