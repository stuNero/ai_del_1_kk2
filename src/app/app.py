import streamlit as st
import requests

from src.config.constants import API_URL

def run_app():
    st.set_page_config(
        page_title="Burnout Predictor 🔥",
        page_icon="🔥"
        )
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://media.licdn.com/dms/image/v2/D4E22AQH7p1CnOwEabg/feedshare-shrink_800/B4EZsKnzSsHcAg-/0/1765411773608?e=2147483647&v=beta&t=K0gdWtPo8xM6-neDxU2rBGx187LEoGCeTWvKpj29glU");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    with st.container():
        st.markdown(
            """
            <style>
            div[data-testid="stVerticalBlock"]:has(div.marker) {
                background-color: rgba(0, 0, 0, 0.6);
                padding: 20px;
                border-radius: 10px;
            }
            </style>
            <div class="marker"></div>
            """,
            unsafe_allow_html=True
        )
        st.title("Burnout Predictor 🔥")
        st.markdown("This app predicts your burnout status based on your mental health status, stress level, and chronic stress.")
        st.markdown("Please fill out the form below to get started.")

        mental_health = st.selectbox("Mental Health Status", ["Critical", "Needs Attention", "Healthy"])
        mental_health = {"Critical": 0, "Needs Attention": 1, "Healthy": 2}[mental_health]

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

    raw_input = {
        "mental_health_status": mental_health,
        "stress_level": stress_level,
        "work_hours_per_week": work_hours_per_week,
        "screen_time_hours": screen_time_hours,
        "meditation_minutes": meditation_minutes,
        "sleep_hours": sleep_hours,
        "sleep_quality": sleep_quality,
        "physical_activity_hours": physical_activity_hours,
        "chronic_stress_no": chronic_stress[0],
        "chronic_stress_yes": chronic_stress[1],
    }


    if st.button("Predict"):
        with st.spinner("Loading page..."):
            response = requests.post(f"{API_URL}/prediction", json=raw_input)

        if response.ok:
            st.write(f"Predicted burnout score: {response.json()}")
        else:
            st.error(f"Prediction failed ({response.status_code}): {response.text}")

if __name__ == "__main__":
    run_app()