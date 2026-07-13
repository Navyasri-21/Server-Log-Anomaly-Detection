# Server-Log-Anomaly-Detection
# 🛡️ Server Log Anomaly Detection Using Machine Learning

## 📌 Project Overview

Server logs contain valuable information about system activities, user authentication, network requests, and application events. As organizations generate thousands of log entries every day, manually identifying suspicious activities such as brute-force login attempts, unauthorized access, or abnormal server behavior becomes extremely difficult.

This project implements an **unsupervised machine learning approach** to automatically detect anomalous server log events using the **Isolation Forest** algorithm. The system analyzes login patterns and network-related information to identify unusual behavior without requiring labeled training data.

---

## 🎯 Problem Statement

Large-scale servers continuously generate authentication and access logs. Monitoring these logs manually is time-consuming and inefficient, often causing security incidents to go unnoticed.

The objective of this project is to:

- Analyze Linux authentication logs.
- Learn normal login behavior.
- Detect unusual login patterns automatically.
- Help system administrators identify suspicious activities for further investigation.

---

# 🚀 Features

- Data preprocessing and cleaning
- Exploratory Data Analysis (EDA)
- Timestamp feature engineering
- Categorical feature encoding
- Unsupervised anomaly detection using Isolation Forest
- Detection of suspicious login activities
- Model serialization using Joblib
- FastAPI deployment for real-time prediction
- Export of anomaly detection results

---

# 📂 Dataset

Dataset Used:

**Linux Authentication Logs with Multiple Anomalies**

Dataset contains information such as:

- Timestamp
- Source IP Address
- City
- Username
- Service
- Number of Login Attempts
- Login Status
- Port
- Protocol

These features simulate real-world Linux authentication logs containing both normal and suspicious activities.

---

# 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Isolation Forest
- Joblib
- FastAPI
- Uvicorn

---

# 📁 Project Structure

```
Server-Log-Anomaly-Detection/

│
├── data/
│   └── linux_auth_logs_multiple_anomalies.csv
│
├── notebooks/
│   └── Server_Log_Anomaly_Detection.ipynb
│
├── models/
│   └── server_log_anomaly_model.pkl
│
├── api/
│   └── app.py
│
├── results/
│   └── server_log_results.csv
│
├── requirements.txt
│
└── README.md
```

---

# 🔄 Project Workflow

```
Dataset Collection
        │
        ▼
Data Cleaning
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Feature Engineering
        │
        ▼
Label Encoding
        │
        ▼
Isolation Forest Training
        │
        ▼
Anomaly Detection
        │
        ▼
Result Analysis
        │
        ▼
Model Saving
        │
        ▼
FastAPI Deployment
```

---

# 📊 Exploratory Data Analysis

The following analyses were performed:

- Dataset overview
- Missing value analysis
- Duplicate record detection
- Statistical summary
- Login attempts distribution
- Login status distribution
- Service analysis
- Hour-wise login analysis
- Outlier detection using Boxplots
- Feature correlation analysis

---

# ⚙️ Feature Engineering

Timestamp column was converted into useful numerical features:

- Hour
- Day
- Month
- Day of Week

Categorical columns were encoded using Label Encoding:

- Source IP
- City
- Username
- Service
- Status
- Protocol

Final features used:

```
source_ip
city
username
service
attempts
status
port
protocol
hour
day_of_week
```

---

# 🤖 Machine Learning Model

Algorithm Used:

**Isolation Forest**

Why Isolation Forest?

- Designed specifically for anomaly detection.
- Does not require labeled data.
- Efficient on large datasets.
- Identifies unusual observations by isolating anomalies.

Model Parameters

```
IsolationForest(
    contamination=0.05,
    random_state=42
)
```

Prediction Output

```
1   → Normal Activity

-1  → Anomaly Detected
```

---

# 📈 Results

The trained model successfully identified suspicious login activities based on:

- High number of login attempts
- Unusual login timings
- Rare combinations of service and protocol
- Suspicious login behavior
- Abnormal access patterns

Each detected record is assigned an anomaly label:

```
1  → Normal

-1 → Anomaly
```

---

# 🌐 API Deployment

FastAPI was used to deploy the trained model.

Run the API

```
uvicorn app:app --reload
```

Open API Documentation

```
http://127.0.0.1:8000/docs
```

Example Request

```json
{
    "source_ip":10,
    "city":2,
    "username":5,
    "service":1,
    "attempts":35,
    "status":0,
    "port":22,
    "protocol":1,
    "hour":3,
    "day_of_week":6
}
```

Example Response

```json
{
    "prediction": -1,
    "result": "Anomaly Detected"
}
```

---

# 📷 Sample Visualizations

- Login Attempts Distribution
- Login Attempts Boxplot
- Login Status Distribution
- Login Activity by Hour
- Top Suspicious Users
- Top Suspicious IP Addresses
- Anomaly Distribution

---

# 📌 Future Improvements

- Real-time log streaming
- Explainable AI using SHAP
- Interactive Streamlit Dashboard
- Docker containerization
- Cloud deployment (AWS/Azure/GCP)
- Automatic alert generation
- Integration with SIEM platforms

---

# 🎓 Learning Outcomes

Through this project, I gained practical experience in:

- Data preprocessing
- Exploratory Data Analysis
- Feature Engineering
- Unsupervised Machine Learning
- Isolation Forest Algorithm
- Anomaly Detection
- Model Deployment using FastAPI
- API Development
- Model Serialization
- Cybersecurity Analytics

---

# 📚 Requirements

```
pandas
numpy
matplotlib
seaborn
scikit-learn
joblib
fastapi
uvicorn
pydantic
```

Install

```
pip install -r requirements.txt
```

---

# 👨‍💻 Author

**Navya Sri Ginjupalli**

B.Tech – Artificial Intelligence & Data Science

Interested in:
- Data Science
- Machine Learning
- Artificial Intelligence

---

## ⭐ If you found this project useful, consider giving it a star!
