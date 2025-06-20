import streamlit as st

st.set_page_config(page_title="HealthAI", layout="wide")

st.sidebar.title("HealthAI Assistant")
option = st.sidebar.radio("Choose a feature", ["Patient Chat", "Disease Prediction", "Treatment Plans", "Health Analytics"])

if option == "Patient Chat":
    st.header("🗣️ Patient Chat")
    query = st.text_input("Ask a health-related question:")
    if query:
        st.write("Response will appear here...")

elif option == "Disease Prediction":
    st.header("🧬 Disease Prediction")
    symptoms = st.text_area("Enter your symptoms:")
    if st.button("Predict"):
        st.write("Prediction will be displayed here...")

elif option == "Treatment Plans":
    st.header("💊 Treatment Plans")
    condition = st.text_input("Enter diagnosed condition:")
    if st.button("Generate Plan"):
        st.write("Treatment plan will be displayed here...")

elif option == "Health Analytics":
    st.header("📊 Health Analytics")
    st.write("Charts and health metrics will be displayed here.")

