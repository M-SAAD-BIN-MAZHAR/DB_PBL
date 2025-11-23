import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="🧠 Depression Prediction", page_icon="🩺", layout="centered")

st.title("🧠 Depression Prediction")
st.write("Fill the form below to assess depression risk based on your inputs.")

THRESHOLD = 0.24  # keep same threshold as backend

# Input form
with st.form(key="prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", min_value=10, max_value=100, value=25)
        profession = st.selectbox("Profession", ["Working Professional", "Student"])
        sleep = st.slider("Sleep Duration (hours)", 0, 24, 7)
        dietary = st.selectbox("Dietary Habits", ["Healthy", "Moderate", "Unhealthy"])

    with col2:
        suicide = st.selectbox("Have you ever had suicidal thoughts?", ["No", "Yes"])
        work_hours = st.slider("Work/Study Hours (0-12)", 0, 12, 6)
        financial = st.slider("Financial Stress (0-5)", 0, 5, 2)
        family = st.selectbox("Family History of Mental Illness?", ["No", "Yes"])
        pressure = st.slider("Pressure (0-5)", 0, 5, 2)
        satisfaction = st.slider("Satisfaction (0-5)", 0, 5, 3)

    submit = st.form_submit_button("🔮 Predict Depression Risk")

# Prediction logic
if submit:
    input_data = {
        "gender": gender,
        "succide": suicide,
        "age": age,
        "work_hours": work_hours,
        "profession": profession,
        "sleep": sleep,
        "financial": financial,
        "family": family,
        "pressure": pressure,
        "dietary": dietary,
        "satisfaction": satisfaction
    }

    # Show input summary
    st.markdown("### 📊 Your Input Summary")
    st.dataframe(pd.DataFrame([input_data]), use_container_width=True)

    try:
        # Call FastAPI backend
        API_URL = "http://127.0.0.1:8000/predict_depression/"
        response = requests.post(API_URL, json=input_data)
        response.raise_for_status()
        result = response.json()

        st.markdown("### 📈 Prediction Results")

        # Display depending on backend response
        if "depression_probability" in result:
            prob = result["depression_probability"]
            status = result["risk_status"]
        else:
            prob = None
            status = result.get("risk_status", "Unknown")

        if "High" in status:
            st.error(f"⚠️ **{status}**")
        else:
            st.success(f"✅ **{status}**")

        # Optional: show probability if available
        if prob is not None:
            st.info(f"Predicted depression probability: {prob:.2f}")

        st.info("""
        **ℹ️ Disclaimer:** This is a predictive model for assessment purposes only. 
        It is not a substitute for professional medical advice, diagnosis, or treatment. 
        If you're experiencing mental health concerns, please consult a healthcare professional.
        """)

    except Exception as e:
        st.error("❌ Prediction failed. Please make sure the backend is running.")
        st.exception(e)

# Footer
st.markdown("---")
st.caption("Built for mental health awareness and early risk assessment")
