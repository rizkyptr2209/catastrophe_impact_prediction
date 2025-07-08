import streamlit as st
import streamlit as st
import joblib
import pandas as pd
import numpy as np
import datetime

# --- Load Assets ---
model = joblib.load("pickle files/model_rf_tuned.pkl")
scaler = joblib.load("pickle files/minmax_scaler.pkl")
feature_columns = joblib.load("pickle files/feature_columns.pkl")

# --- User Interface ---
st.title("Catastrophe Casualties on Economy Prediction")
st.markdown("Fill in the details below:")

# --- Categorical Options ---
disaster_types = ["Earthquake", "Flood", "Hurricane", "Tornado", "Wildfire"]
locations = ["Brazil", "China", "India", "Indonesia", "Japan", "USA"]

# --- Basic User Inputs ---
col1, col2 = st.columns(2)
with col1:
    selected_date = st.date_input("Date of Event", value=datetime.date.today())
    hour = st.slider("Hour (0-23)", 0, 23)
    if hour >= 12:
        hour -= 12
        time = "PM"
    else:
        time = "AM"
    st.write("Predicting the disaster impact occurs on", selected_date, "at", hour, time)
with col2:
    magnitude = st.number_input("Magnitude", min_value=0.0, max_value= 10.0, value=0.0)
    fatalities = st.number_input("Fatalities", min_value=0, value=0, step=1)

col3, col4 = st.columns(2)
with col3:
    # --- Lag and Rolling Inputs ---
    lag_1 = st.number_input("Lag 1 (0 - 1,000,000,000)", min_value=0.0, max_value=1000000000.0, value=0.0)
    lag_7 = st.number_input("Lag 7 (0 - 1,000,000,000)", min_value=0.0, max_value=1000000000.0, value=0.0)
    rolling_mean_7 = st.number_input("Rolling Mean (7 days)", min_value=0.0, value=0.0)
    rolling_std_7 = st.number_input("Rolling Std (7 days)", min_value=0.0, value=0.0)
with col4:
# --- Categorical Inputs ---
    disaster_type = st.selectbox("Disaster Type", disaster_types)
    location = st.selectbox("Location", locations)

# --- Input Validation (Warn and Skip Prediction if Invalid) ---
required_inputs = [magnitude, fatalities, hour, lag_1, lag_7, rolling_mean_7, rolling_std_7]
if any(pd.isnull(required_inputs)):
    st.warning("⚠️ Please fill out all required fields before making a prediction.")
else:
    if st.button("Predict"):

        # --- Feature Engineering ---
        dayofweek = selected_date.weekday() + 1
        dayofmonth = selected_date.day
        month = selected_date.month
        is_night = int(hour < 6 or hour >= 18)
        is_weekend = int(dayofweek in [6, 7])

        # --- Prepare Numerical Features ---
        num_raw = pd.DataFrame([{
            "Magnitude": float(magnitude),
            "Fatalities": float(fatalities),
            "hour": float(hour),
            "lag_1": float(lag_1),
            "lag_7": float(lag_7),
            "rolling_mean_7": float(rolling_mean_7),
            "rolling_std_7": float(rolling_std_7),
        }])

        if num_raw.isnull().values.any():
            st.error("❌ Some input values are missing or invalid. Please check all fields.")
        else:
            # --- Create Input Template ---
            input_data = pd.DataFrame(np.zeros((1, len(feature_columns))), columns=feature_columns).astype(float)

            # --- Fill Scaled Values ---
            scaled = scaler.transform(num_raw)
            for i, col in enumerate(num_raw.columns):
                input_data[col] = scaled[0, i]

            # --- Add Time Features ---
            input_data["is_night"] = is_night
            input_data["dayofweek"] = dayofweek
            input_data["is_weekend"] = is_weekend
            input_data["dayofmonth"] = dayofmonth
            input_data["month"] = month

            # --- One-Hot Encoding ---
            col_disaster = f"Disaster_Type_{disaster_type}"
            col_location = f"Location_{location}"
            if col_disaster in input_data.columns:
                input_data[col_disaster] = 1
            if col_location in input_data.columns:
                input_data[col_location] = 1

            # --- Predict and Display Result ---
            prediction = model.predict(input_data)[0]
            st.success(f"Economy Value Lost Prediction: $ **{prediction:.2f}**")