# app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.ai import (
    init_granite_model,
    answer_patient_query,
    predict_disease,
    generate_treatment_plan,
    recommend_doctor,
    display_health_analytics
)

# Simulated users (for login)
USERS = {
    "irfan": "1234",
    "soniya": "abcd"
}

# Login system
def login():
    st.title("🔐 HealthAI Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid credentials.")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    login()
    st.stop()

# Initialize the model
model = init_granite_model()

# Sidebar – Patient Profile
with st.sidebar:
    st.header("Patient Profile")
    if "profile" not in st.session_state:
        st.session_state.profile = {}

    st.session_state.profile['name'] = st.text_input("Name", st.session_state.profile.get('name', ''))
    st.session_state.profile['age'] = st.number_input("Age", min_value=0, max_value=120, value=30)
    st.session_state.profile['gender'] = st.selectbox("Gender", ["Male", "Female", "Other"])
    st.session_state.profile['history'] = st.text_area("Medical History", st.session_state.profile.get('history', ''))
    st.session_state.profile['medications'] = st.text_area("Medications", st.session_state.profile.get('medications', ''))
    st.session_state.profile['allergies'] = st.text_area("Allergies", st.session_state.profile.get('allergies', ''))

# Main App Navigation
tab = st.radio("Select Module", ["Patient Chat", "Disease Prediction", "Treatment Plan", "Doctor Recommendation", "Health Analytics"])

# Patient Chat
if tab == "Patient Chat":
    st.subheader("Patient Chat Assistant")
    query = st.text_input("Ask your health question:")
    if st.button("Send"):
        if query:
            response = answer_patient_query(query, model)
            user = st.session_state.get("username", "guest")
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = {}
            if user not in st.session_state.chat_history:
                st.session_state.chat_history[user] = []
            st.session_state.chat_history[user].append({"query": query, "response": response})

    if "chat_history" in st.session_state:
        user = st.session_state.get("username", "guest")
        chats = st.session_state.chat_history.get(user, [])
        if chats:
            st.markdown("### Chat History")
            for chat in reversed(chats):
                st.markdown(f"**You:** {chat['query']}")
                st.markdown(f"**Assistant:** {chat['response']}")
                st.markdown("---")
    st.markdown("\n⚠️ *Disclaimer: This response is AI-generated and not a substitute for professional medical advice.*")

# Disease Prediction
elif tab == "Disease Prediction":
    st.subheader("Disease Prediction System")
    with st.form("disease_form"):
        symptoms = st.text_input("Enter Symptoms (comma-separated)")
        age = st.number_input("Age", min_value=0, max_value=120, value=st.session_state.profile.get('age', 30))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0)
        history = st.text_area("Medical History", st.session_state.profile.get('history', ''))
        vitals = st.text_area("Vitals (e.g., BP 120/80, HR 70, Temp 98.6°F)")
        submitted = st.form_submit_button("Generate Prediction")
        if submitted:
            result = predict_disease(symptoms, age, gender, history, vitals, model)
            st.markdown("### Possible Conditions:")
            st.markdown(result)
            st.markdown("⚠️ *Disclaimer: This is AI-generated. Please consult a licensed physician for diagnosis.*")

# Treatment Plan
elif tab == "Treatment Plan":
    st.subheader("Treatment Plan Generator")
    condition = st.text_input("Enter Condition")
    age = st.number_input("Age", min_value=0, max_value=120, value=st.session_state.profile.get('age', 30))
    history = st.text_area("Medical History", st.session_state.profile.get('history', ''))
    if st.button("Generate Treatment Plan"):
        if condition:
            plan = generate_treatment_plan(condition, age, history, model)
            st.markdown("### Suggested Treatment Plan")
            st.markdown(plan)
            st.markdown("⚠️ *Disclaimer: AI-generated content. Please consult a healthcare provider.*")

# Doctor Recommendation
elif tab == "Doctor Recommendation":
    st.subheader("Doctor Recommendation")
    symptoms = st.text_input("List your symptoms (comma-separated):")
    if st.button("Recommend Doctor"):
        if symptoms:
            suggestion = recommend_doctor(symptoms, model)
            st.markdown(f"**Recommended Specialist:** {suggestion}")

# Health Analytics
elif tab == "Health Analytics":
    st.subheader("Health Analytics Dashboard")
    dates = pd.date_range(end=pd.Timestamp.today(), periods=90)
    df = pd.DataFrame({
        'date': dates,
        'heart_rate': np.random.normal(72, 5, size=90),
        'blood_pressure': np.random.normal(120, 10, size=90),
        'glucose': np.random.normal(90, 12, size=90),
        'symptom': np.random.choice(['headache', 'fatigue', 'none', 'dizziness'], size=90)
    })
    display_health_analytics(df)
