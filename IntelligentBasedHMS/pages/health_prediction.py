import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
 
from components import show_header, show_footer, navigate_to_page,back_to_dashboard_button


import pickle
import numpy as np
import streamlit as st

 
load_model = pickle.load(open("xgb_model.pkl", "rb"))

def predict(features):
    X = np.array([features])
    return load_model.predict(X)[0]
 
st.set_page_config(page_title="Risk Predictor", page_icon="⚕️", layout="centered")
st.title("⚕️ Health Risk Predictor")
st.markdown("Enter your details below to predict your risk level.")
 
st.header("Personal Information")
age = st.number_input("Age", min_value=0, step=1, value=30)
weight = st.number_input("Weight (kg)", min_value=0, step=1, value=70)
height = st.number_input("Height (cm)", min_value=0, step=1, value=170)
 
with st.expander("Health & Lifestyle Details"):
    exercise = st.number_input("Exercise (hours/day)", min_value=0, step=1, value=1)
    sleep = st.number_input("Sleep (hours/day)", min_value=0, step=1, value=7)
    sugar_intake = st.number_input("Sugar intake (times/day)", min_value=0, step=1, value=1)
    bmi_recalc = st.number_input("BMI", min_value=0.0, step=0.1, value=22.5)
    smoking_yes = st.selectbox("Smoking?", [0, 1], index=0)
    alcohol_yes = st.selectbox("Alcohol?", [0, 1], index=0)
 
st.header("Profession")
profession_options = [
    "Doctor", "Driver", "Engineer", "Farmer", 
    "Office Worker", "Student", "Teacher"
]
profession = st.selectbox("Select your profession", profession_options)
 
if st.button("Predict Risk"):
  
    profession_one_hot = [1 if p == profession else 0 for p in profession_options]

   
    features = [
        int(age), int(weight), int(height), int(exercise), int(sleep),
        int(sugar_intake), float(bmi_recalc), int(smoking_yes), int(alcohol_yes)
    ] + profession_one_hot

   
    pred = predict(features)

   
    if pred == 1:
        st.error("🚨 High Risk")
    else:
        st.success("✅ Low Risk / Safe")

 
st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit")


if st.button("Consult Doctor / Chatbot"):
    navigate_to_page("pages/medical_bot.py")

back_to_dashboard_button()
show_footer()