import streamlit as st
from api import fetch_model


regression_model = fetch_model(model_type="regression")

st.set_page_config(page_title="Burnout Predictor 🔥", page_icon="🔥")

mental_health = st.selectbox("Mental Health Status", ["Critical", "Needs attention","Healthy"])
mental_health = {"Critical": 0, "Needs attention": 1, "Healthy": 2}[mental_health]

stress_level = st.selectbox("Stress Level Last 14 Days", ["High", "Moderate","Low"])
stress_level = {"High": 0, "Moderate": 1, "Low": 2}[stress_level]

chronic_stress = st.selectbox("Chronic Stress", ["No", "Yes"])
chronic_stress = {"No": [1, 0], "Yes": [0, 1]}[chronic_stress]

sleep_quality = st.selectbox("Sleep Quality Last 14 Days", ["Poor", "Average", "Good", "Excellent"])
sleep_quality = {"Poor": 0, "Average": 1, "Good": 2, "Excellent": 3}[sleep_quality]

work_hours_per_week = st.number_input("Work Hours Per Week", min_value=0, max_value=85, value=0, step=1)

screen_time_hours = st.number_input("Screen Time Hours Per Day", min_value=0, max_value=18, value=0, step=1)

meditation_minutes = st.number_input("Meditation Minutes Per Day", min_value=0, max_value=240, value=0, step=1)

sleep_hours = st.number_input("Sleep Hours Per Night", min_value=2, max_value=12, value=2, step=1)

physical_activity_hours = st.number_input("Physical Activity Hours Per Week", min_value=0, max_value=13, value=0, step=1)

data = [
    mental_health,
    stress_level,
    work_hours_per_week,
    screen_time_hours,
    meditation_minutes,
    sleep_hours,
    sleep_quality, 
    physical_activity_hours,
    chronic_stress[0],
    chronic_stress[1]
    ]

if st.button("Predict"):
    prediction = regression_model.predict([data])
    st.write(prediction[0])