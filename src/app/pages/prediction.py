import streamlit as st
import requests
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.config.constants import API_URL
from styles import PREDICTION_CSS
from questions import QUESTIONS

st.set_page_config(page_title="Burnout Predictor 🔥", page_icon="🔥", layout="wide")

st.markdown(PREDICTION_CSS, unsafe_allow_html=True)

if "current_question" not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.form_data = {
        "mental_health_status": None,
        "stress_level": None,
        "chronic_stress_no": 1,
        "chronic_stress_yes": 0,
        "sleep_quality": None,
        "sleep_hours": 7.0,
        "work_hours_per_week": 40.0,
        "screen_time_hours": 0.0,
        "meditation_minutes": 0.0,
        "physical_activity_hours": 0.0,
    }
    st.session_state.completed = False


if not st.session_state.completed:
    # Hämta nuvarande fråga
    q = QUESTIONS[st.session_state.current_question]

    answer = None

    # Home-knapp
    if st.button("← Home", key="home_button"):
        st.switch_page("app.py")

    with st.container(border=True, key="question_card"):
        st.markdown(
            f'<div class="progress-label">Question {st.session_state.current_question + 1} of {len(QUESTIONS)}</div>',
            unsafe_allow_html=True,
        )

        # Progress bar
        st.progress(
            (st.session_state.current_question + 1) / len(QUESTIONS),
        )

        st.markdown(
            f'<div class="question-title">{q["title"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="question-description">{q["description"]}</div>',
            unsafe_allow_html=True,
        )

        if q["type"] == "select":
            answer = st.selectbox(
                "Select an answer:",
                q["options"],
                key=f"answer_{st.session_state.current_question}",
                label_visibility="collapsed",
            )

        elif q["type"] == "radio":
            answer = st.radio(
                "Select an answer:",
                q["options"],
                key=f"answer_{st.session_state.current_question}",
                label_visibility="collapsed",
            )

        elif q["type"] == "slider":
            answer = st.slider(
                "Select a value:",
                min_value=q["min"],
                max_value=q["max"],
                step=q["step"],
                value=st.session_state.form_data[q["key"]],
                key=f"answer_{st.session_state.current_question}",
                label_visibility="collapsed",
            )

        st.markdown("")

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button(
                "Back",
                use_container_width=True,
                disabled=(st.session_state.current_question == 0),
            ):
                # Spara svaret innan vi går tillbaka
                if answer is not None:
                    if "mapping" in q:
                        st.session_state.form_data[q["key"]] = q["mapping"][answer]
                    elif q["type"] == "radio" and q["key"] == "chronic_stress":
                        st.session_state.form_data["chronic_stress_no"] = (
                            1 if answer == "No" else 0
                        )
                        st.session_state.form_data["chronic_stress_yes"] = (
                            0 if answer == "No" else 1
                        )
                    else:
                        st.session_state.form_data[q["key"]] = answer

                st.session_state.current_question -= 1
                st.rerun()

        with col3:
            if st.button("Next  →", use_container_width=True, type="primary"):
                # Spara svaret
                if answer is not None:
                    if "mapping" in q:
                        st.session_state.form_data[q["key"]] = q["mapping"][answer]
                    elif q["type"] == "radio" and q["key"] == "chronic_stress":
                        st.session_state.form_data["chronic_stress_no"] = (
                            1 if answer == "No" else 0
                        )
                        st.session_state.form_data["chronic_stress_yes"] = (
                            0 if answer == "No" else 1
                        )
                    else:
                        st.session_state.form_data[q["key"]] = answer

                # Gå till nästa fråga eller markera som klar
                if st.session_state.current_question < len(QUESTIONS) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    # Sista frågan - markera som klar
                    st.session_state.completed = True
                    st.rerun()

# Om completed, visa resultat
else:
    st.toast("All questions answered! Processing your data...")

    with st.spinner("Analyzing your burnout risk..."):
        try:
            # Konvertera form_data till rätt format
            payload = {
                "mental_health_status": int(
                    st.session_state.form_data["mental_health_status"]
                ),
                "stress_level": int(st.session_state.form_data["stress_level"]),
                "chronic_stress_no": int(
                    st.session_state.form_data["chronic_stress_no"]
                ),
                "chronic_stress_yes": int(
                    st.session_state.form_data["chronic_stress_yes"]
                ),
                "sleep_quality": int(st.session_state.form_data["sleep_quality"]),
                "sleep_hours": float(st.session_state.form_data["sleep_hours"]),
                "work_hours_per_week": int(
                    st.session_state.form_data["work_hours_per_week"]
                ),
                "screen_time_hours": int(
                    st.session_state.form_data["screen_time_hours"]
                ),
                "meditation_minutes": int(
                    st.session_state.form_data["meditation_minutes"]
                ),
                "physical_activity_hours": float(
                    st.session_state.form_data["physical_activity_hours"]
                ),
            }

            response = requests.post(f"{API_URL}/prediction", json=payload, timeout=10)

            if response.ok:
                raw_score = response.json()

                # Normalisera score till 0-100
                if raw_score > 10:
                    score = min(10, (raw_score / 100) * 10)
                else:
                    score = raw_score

                # Score display
                with st.container(border=True, key="result_card"):
                    # Risknivå + färger
                    if score <= 3:
                        risk_level = "Low Risk"
                        risk_color = "#4ade80"
                        risk_bg = "rgba(74, 222, 128, 0.1)"
                        risk_border = "rgba(74, 222, 128, 0.35)"
                        risk_message = "Your responses indicate a low risk of burnout. Keep taking care of your mental and physical well-being."
                    elif score <= 6:
                        risk_level = "Moderate Risk"
                        risk_color = "#fbbf24"
                        risk_bg = "rgba(251, 191, 36, 0.1)"
                        risk_border = "rgba(251, 191, 36, 0.35)"
                        risk_message = "Your responses indicate a moderate risk of burnout. Consider making some lifestyle changes."
                    else:
                        risk_level = "High Risk"
                        risk_color = "#f87171"
                        risk_bg = "rgba(248, 113, 113, 0.1)"
                        risk_border = "rgba(248, 113, 113, 0.35)"
                        risk_message = "Your responses indicate a high risk of burnout. Please consider talking to a mental health professional."

                    risk_pct = int((score / 10) * 100)
                    score_display = risk_pct

                    st.markdown(
                        f"""
                        <div class="score-container">
                            <div class="score-eyebrow">Burnout Score</div>
                            <div class="score-value">
                                <span style="color:{risk_color};">{score_display}</span>
                                <span class="score-value-unit"> / 100</span>
                            </div>
                        </div>

                        <div class="risk-summary-row">
                            <span class="risk-summary-label">Burnout Risk Level: {risk_pct}%</span>
                            <span class="risk-summary-value" style="color:{risk_color};">{risk_level}</span>
                        </div>
                        <div class="risk-track">
                            <div class="risk-fill" style="width:{risk_pct}%; background:{risk_color};"></div>
                        </div>

                        <div class="risk-box" style="background:{risk_bg}; border:1px solid {risk_border};">
                            <div class="risk-box-title" style="color:{risk_color};">{risk_level}</div>
                            <div class="risk-box-message">{risk_message}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Rekommendationer
                    st.markdown(
                        '<div class="recommendations-title">Recommendations</div>',
                        unsafe_allow_html=True,
                    )

                    sleep_hours = st.session_state.form_data["sleep_hours"]
                    work_hours = st.session_state.form_data["work_hours_per_week"]
                    activity_hours = st.session_state.form_data[
                        "physical_activity_hours"
                    ]
                    meditation_min = st.session_state.form_data["meditation_minutes"]
                    screen_hours = st.session_state.form_data["screen_time_hours"]

                    recommendations = []

                    if sleep_hours < 7:
                        recommendations.append(
                            {
                                "title": "Improve your sleep",
                                "description": "Aim for 7–9 hours of quality sleep each night.",
                                "severity": (7 - sleep_hours) / 7,
                            }
                        )
                    if work_hours > 50:
                        recommendations.append(
                            {
                                "title": "Reduce work hours",
                                "description": "Try to cut back or take more breaks during the week.",
                                "severity": (work_hours - 50) / 50,
                            }
                        )
                    if activity_hours < 2:
                        recommendations.append(
                            {
                                "title": "Get moving more",
                                "description": "Aim for 150+ minutes of physical activity per week.",
                                "severity": (2 - activity_hours) / 2,
                            }
                        )
                    if meditation_min == 0:
                        recommendations.append(
                            {
                                "title": "Try meditation",
                                "description": "Start with just 5–10 minutes of daily meditation.",
                                "severity": 0.4,
                            }
                        )
                    if screen_hours > 8:
                        recommendations.append(
                            {
                                "title": "Cut down screen time",
                                "description": "Especially in the hour before bed.",
                                "severity": (screen_hours - 8) / 8,
                            }
                        )

                    recommendations = sorted(
                        recommendations, key=lambda r: r["severity"], reverse=True
                    )[:3]

                    if not recommendations:
                        recommendations.append(
                            {
                                "title": "Keep up the good work",
                                "description": "You're already doing all the right things.",
                            }
                        )

                    for rec in recommendations:
                        st.markdown(
                            f'<div class="recommendation-item" style="border-left-color:{risk_color};">'
                            f'<div class="recommendation-title">{rec["title"]}</div>'
                            f'<div class="recommendation-description">{rec["description"]}</div>'
                            f"</div>",
                            unsafe_allow_html=True,
                        )

                    st.markdown("")

                    # Back to home button
                    col1, col2, col3 = st.columns([1, 1.2, 1])
                    with col2:
                        if st.button(
                            "Back to Home", use_container_width=True, type="secondary"
                        ):
                            st.session_state.current_question = 0
                            st.session_state.form_data = {
                                "mental_health_status": None,
                                "stress_level": None,
                                "chronic_stress_no": 1,
                                "chronic_stress_yes": 0,
                                "sleep_quality": None,
                                "sleep_hours": 7.0,
                                "work_hours_per_week": 40.0,
                                "screen_time_hours": 0.0,
                                "meditation_minutes": 0.0,
                                "physical_activity_hours": 0.0,
                            }
                            st.session_state.completed = False
                            st.switch_page("app.py")

            else:
                st.error(f"Prediction failed: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to API. Make sure the backend is running on port 8000!"
            )
        except Exception as e:
            st.error(f"Error: {str(e)}")
