import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the trained model and encoders
with open("rf_model.pkl", "rb") as model_file:
    rf_model = pickle.load(model_file)

with open("label_encoders.pkl", "rb") as encoder_file:
    label_encoders = pickle.load(encoder_file)

# Load dataset to extract state-district mapping
df = pd.read_csv("crop_production_filtered.csv")  # Ensure this file is available
state_district_mapping = df.groupby("State_Name")["District_Name"].unique().to_dict()

# Streamlit UI
st.title("Crop Production Prediction App 🌾")

# State Selection
state = st.selectbox("Select State", list(state_district_mapping.keys()))

# District Selection (Filtered based on selected State)
districts_for_selected_state = state_district_mapping[state]  # Get districts for selected state
district = st.selectbox("Select District", districts_for_selected_state)

# Other Inputs
season = st.selectbox("Select Season", label_encoders["Season"].classes_)
crop = st.selectbox("Select Crop", label_encoders["Crop"].classes_)
crop_year = st.number_input("Enter Crop Year", min_value=2000, max_value=2025, step=1)
area = st.number_input("Enter Area (in hectares)", min_value=0.1, step=0.1)

# Predict Button
if st.button("Predict Production"):
    try:
        # Encode user inputs
        encoded_input = np.array([
            label_encoders["State_Name"].transform([state])[0],
            label_encoders["District_Name"].transform([district])[0],
            label_encoders["Season"].transform([season])[0],
            label_encoders["Crop"].transform([crop])[0],
            crop_year,
            area
        ]).reshape(1, -1)

        # Make prediction
        predicted_production = rf_model.predict(encoded_input)[0]

        # Display result
        st.success(f"Predicted Production: {predicted_production:.2f} metric tons")
    except Exception as e:
        st.error(f"Error: {e}")
