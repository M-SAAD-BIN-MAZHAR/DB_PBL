import sys, os

from pages.DataBaseConnection import create_connection
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from components import show_footer
from datetime import datetime

st.set_page_config(page_title="Patient Registration & Login", layout="centered")

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "registration_complete" not in st.session_state:
    st.session_state.registration_complete = False
if "patient_data" not in st.session_state:
    st.session_state.patient_data = {}

# Database function moved to top level
def insert_patient_data(patient_id, first_name, last_name, email, phone, address, emergency_contact, date_of_birth, gender, blood_type, password):
    try:
        conn = create_connection()
        curr = conn.cursor()
        insert_query = """
            INSERT INTO PATIENT_DATA 
            (Patient_ID, First_Name, Last_Name, Email, Phone, Home_Address, Emergency_Contact, Date_of_Birth, Gender, Blood_Type, Password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        curr.execute(insert_query, (int(patient_id), first_name, last_name, email, phone, address, emergency_contact, date_of_birth, gender, blood_type, password))
        conn.commit()
        curr.close()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        st.error(f"Database error: {e}")
        return False

# --- Global CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .main {
        background: transparent;
    }
    
    /* Glass container for forms */
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 40px;
        margin: 50px auto;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        max-width: 500px;
        width: 100%;
    }
    
    /* Title styling */
    .form-title {
        text-align: center;
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }
    
    .form-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        font-size: 14px;
        margin-bottom: 30px;
    }
    
    /* Input field styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        color: #333 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
        background: white !important;
    }
    
    /* Label styling */
    .stTextInput label, .stSelectbox label, .stDateInput label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        color: white !important;
        padding: 14px 24px !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        margin-top: 10px !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    /* Form container */
    [data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
    }
    
    /* Success message */
    .success-container {
        text-align: center;
        padding: 40px 20px;
    }
    
    .success-icon {
        font-size: 64px;
        margin-bottom: 20px;
    }
    
    .success-title {
        font-size: 24px;
        font-weight: 600;
        color: white;
        margin-bottom: 10px;
    }
    
    .success-subtitle {
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 30px;
    }
    
    /* Toggle between login/register */
    .toggle-text {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 20px;
        font-size: 14px;
    }
    
    .toggle-link {
        color: #667eea;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
    }
    
    .toggle-link:hover {
        color: #764ba2;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# --- Registration Form ---
def show_registration_form():
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">👤 Patient Registration</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-subtitle">Complete your profile for better healthcare experience</div>', unsafe_allow_html=True)
    
    with st.form("registration_form"):
        # Personal Information - Two columns for name
        st.markdown("### Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="Enter your first name", key="first_name")
        with col2:
            last_name = st.text_input("Last Name", placeholder="Enter your last name", key="last_name")
        
        # Contact Information
        st.markdown("### Contact Information")
        email = st.text_input("📧 Email Address", placeholder="your.email@example.com", key="email")
        phone = st.text_input("📞 Phone Number", placeholder="+1 (555) 123-4567", key="phone")
        address = st.text_input("🏠 Home Address", placeholder="Enter your complete address", key="address")
        emergency_contact = st.text_input("🚨 Emergency Contact", placeholder="Emergency contact phone number", key="emergency_contact")
        
        # Medical Information
        st.markdown("### Medical Information")
        col3, col4 = st.columns(2)
        with col3:
            date_of_birth = st.date_input("🎂 Date of Birth", value=None, key="dob")
            gender = st.selectbox("⚧ Gender", ["Select", "Male", "Female", "Other", "Prefer not to say"], key="gender")
        with col4:
            blood_type = st.selectbox("💉 Blood Type", ["Select", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], key="blood_type")
            patient_id = st.text_input("🆔 Patient ID", placeholder="Enter unique Patient ID", key="patient_id")
        
        # Account Security
        st.markdown("### Account Security")
        password = st.text_input("🔒 Create Password", type="password", placeholder="Create a strong password", key="password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter your password", key="confirm_password")
        
        # Terms and Submit
        agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy", key="terms")
        
        submit_registration = st.form_submit_button("Complete Registration 🚀")
    
    st.markdown('</div>', unsafe_allow_html=True)

    if submit_registration:
        if not all([first_name, last_name, email, phone, password, confirm_password, patient_id]):
            st.error("❌ Please fill in all required fields")
        elif password != confirm_password:
            st.error("❌ Passwords do not match")
        elif not agree_terms:
            st.error("❌ Please agree to the Terms of Service")
        elif not patient_id.isdigit():
            st.error("❌ Patient ID must be a number")
        else:
            # Store patient data in session state
            st.session_state.patient_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "address": address,
                "emergency_contact": emergency_contact,
                "date_of_birth": date_of_birth,
                "gender": gender,
                "blood_type": blood_type,
                "patient_id": patient_id
            }
            
            # Insert into database
            if insert_patient_data(patient_id, first_name, last_name, email, phone, address, emergency_contact, date_of_birth, gender, blood_type, password):
                st.session_state.registration_complete = True
                st.success("🎉 Registration completed successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to register. Please try again.")

# --- Login Form ---
def show_login_form():
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">🔐 Patient Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-subtitle">Welcome back! Please login to your account</div>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("📧 Email Address", placeholder="your.email@example.com", key="login_email")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="login_password")
        
        submit_login = st.form_submit_button("Login to Portal 🚀")
    
    # Toggle to registration
    st.markdown("""
    <div class="toggle-text">
        Don't have an account? 
        <span class="toggle-link" onclick="window.location.href='?form=register'">Create Account</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if submit_login:
        # Database authentication
        conn = create_connection()
        curr = conn.cursor()
        try:
            curr.execute("SELECT * FROM PATIENT_DATA WHERE Email = %s AND Password = %s", (email, password))
            user = curr.fetchone()
            if user:
                st.session_state.logged_in = True
                # Store user data in session state
                st.session_state.patient_data = {
                    "patient_id": user[0],
                    "first_name": user[1],
                    "last_name": user[2],
                    "email": user[3],
                    "phone": user[4],
                    "address": user[5],
                    "emergency_contact": user[6],
                    "date_of_birth": user[7],
                    "gender": user[8],
                    "blood_type": user[9]
                }
                st.success("✅ Login Successful!")
                st.rerun()
            else:
                
                st.error("❌ Invalid email or password")
        except Exception as e:
            st.error(f"An error occurred during login: {e}")
        finally:
            curr.close()
            conn.close()

# --- After Login Success ---
def show_dashboard():
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<div class="success-container">', unsafe_allow_html=True)
    st.markdown('<div class="success-icon">🎉</div>', unsafe_allow_html=True)
    st.markdown('<div class="success-title">Welcome to Your Patient Portal!</div>', unsafe_allow_html=True)
    st.markdown('<div class="success-subtitle">You have successfully accessed your healthcare dashboard</div>', unsafe_allow_html=True)
    
    # Display patient information
    if st.session_state.patient_data:
        st.markdown("### Your Profile Information")
        patient_data = st.session_state.patient_data
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Patient ID:** {patient_data.get('patient_id', 'Not specified')}")
            st.info(f"**Name:** {patient_data.get('first_name', '')} {patient_data.get('last_name', '')}")
            st.info(f"**Email:** {patient_data.get('email', '')}")
            st.info(f"**Phone:** {patient_data.get('phone', '')}")
        with col2:
            st.info(f"**Blood Type:** {patient_data.get('blood_type', 'Not specified')}")
            st.info(f"**Gender:** {patient_data.get('gender', 'Not specified')}")
            st.info(f"**Emergency Contact:** {patient_data.get('emergency_contact', 'Not specified')}")
            st.info(f"**Date of Birth:** {patient_data.get('date_of_birth', 'Not specified')}")
    
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.registration_complete = False
        st.session_state.patient_data = {}
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Patient Dashboard", use_container_width=True):
        st.switch_page("pages/patient_dashboard.py")
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main App Logic ---
def main():
    # Check URL parameters for form type using st.query_params
    query_params = st.query_params
    form_type = query_params.get("form", ["login"])[0]
    
    if st.session_state.logged_in:
        show_dashboard()
    elif form_type == "register" or not st.session_state.registration_complete:
        show_registration_form()
    else:
        show_login_form()

if __name__ == "__main__":
    main()
    show_footer()