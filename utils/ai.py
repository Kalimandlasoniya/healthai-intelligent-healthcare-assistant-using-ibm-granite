# utils/ai.py

from transformers import pipeline
import plotly.express as px
import streamlit as st

# Load text2text generation model
def init_granite_model():
    return pipeline("text2text-generation", model="google/flan-t5-large")

# Patient Chat

def answer_patient_query(query, model):
    prompt = f"""
You are a kind and knowledgeable medical assistant.

Patient's Question:
{query}

Instructions:
- Provide a compassionate and clear explanation.
- Suggest evidence-based home care tips or common treatments.
- Emphasize this is not a diagnosis.
- Encourage doctor consultation.

Format in simple points.
End with a disclaimer.
"""
    return model(prompt)[0]['generated_text'].strip()

# Disease Prediction

def predict_disease(symptoms, age, gender, history, vitals, model):
    prompt = f"""
You are a smart medical assistant.

Given the patient details below, list the top 3 most likely medical conditions they may have.

Symptoms: {symptoms}
Age: {age}
Gender: {gender}
Medical History: {history}
Vitals: {vitals}

Instructions:
- Mention 3 likely conditions.
- Estimate likelihood for each (as a percentage).
- Suggest next steps or actions.
- Avoid giving a diagnosis.
- Format as a numbered list.
"""
    return model(prompt)[0]['generated_text'].strip()

# Treatment Plan Generator

def generate_treatment_plan(condition, age, history, model):
    prompt = f"""
You are a reliable medical assistant.

Create a treatment plan for:
- Condition: {condition}
- Age: {age}
- History: {history}

Include:
1. Medications (if any)
2. Lifestyle changes
3. Tests or monitoring advice

End with a disclaimer and encourage doctor consultation.
"""
    return model(prompt)[0]['generated_text'].strip()

# Doctor Recommendation

def recommend_doctor(symptoms, model):
    prompt = f"""
You are a medical assistant.
Based on the symptoms: {symptoms}, suggest what kind of doctor (e.g., Neurologist, Cardiologist) the patient should see.
Only suggest the type of doctor. Do not guess a diagnosis.
"""
    return model(prompt)[0]['generated_text'].strip()

# Health Analytics Dashboard

def display_health_analytics(df):
    st.subheader("📈 Health Trends (Last 90 Days)")

    fig1 = px.line(df, x='date', y='heart_rate', title='Heart Rate Trend')
    st.plotly_chart(fig1)

    fig2 = px.line(df, x='date', y='blood_pressure', title='Blood Pressure Trend')
    st.plotly_chart(fig2)

    fig3 = px.line(df, x='date', y='glucose', title='Glucose Trend')
    st.plotly_chart(fig3)

    symptom_counts = df['symptom'].value_counts().reset_index()
    symptom_counts.columns = ['symptom', 'count']
    fig4 = px.pie(symptom_counts, names='symptom', values='count', title='Symptom Frequency')
    st.plotly_chart(fig4)

    st.metric("Avg Heart Rate", f"{df['heart_rate'].mean():.1f} bpm")
    st.metric("Avg BP", f"{df['blood_pressure'].mean():.1f} mmHg")
    st.metric("Avg Glucose", f"{df['glucose'].mean():.1f} mg/dL")