import streamlit as st

# Page configuration - MUST be first command
st.set_page_config(
    page_title="Smart HealthCare System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'role' not in st.session_state:
    st.session_state.role = None

# --- PROFESSIONAL CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 3rem;
        margin: 2rem auto;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        max-width: 900px;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .sub-header {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .role-prompt {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.8);
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .centered-buttons {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        margin: 3rem 0;
        flex-wrap: wrap;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 20px 40px;
        border-radius: 16px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        margin: 10px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 250px;
        height: 70px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 3rem 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.5;
    }
    
    .medical-icon {
        text-align: center;
        font-size: 4rem;
        margin: 2rem 0;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    @media (max-width: 768px) {
        .glass-container {
            margin: 1rem;
            padding: 2rem;
        }
        .main-header {
            font-size: 2.5rem;
        }
        .centered-buttons {
            flex-direction: column;
            gap: 1.5rem;
        }
        .stButton > button {
            width: 100%;
            max-width: 300px;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- MAIN CONTENT ---
def main():
    # Header Section
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🏥 Smart HealthCare System</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Revolutionizing Healthcare with Intelligent Monitoring</h2>', unsafe_allow_html=True)
    st.markdown('<p class="role-prompt">Please select your role to continue your healthcare journey</p>', unsafe_allow_html=True)
    
    # Centered Medical Icon
    st.markdown('<div class="medical-icon">💻🏥</div>', unsafe_allow_html=True)
    
    # Perfectly Centered Role Selection Buttons
    st.markdown('<div class="centered-buttons">', unsafe_allow_html=True)
    
    # Create two columns for side-by-side buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👤 Patient Portal", key="patient_btn", 
                    help="Access your personal health dashboard and monitoring tools",
                    use_container_width=True):
            st.session_state.role = "patient"
            st.rerun()
    
    with col2:
        if st.button("👨‍⚕️ Doctor Dashboard", key="doctor_btn", 
                    help="Access professional tools for patient management and care",
                    use_container_width=True):
            st.session_state.role = "doctor"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature Highlights
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Real-time Monitoring</div>
            <div class="feature-desc">Track vital signs and health metrics with AI-powered insights</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Diagnostics</div>
            <div class="feature-desc">Advanced machine learning for early detection and prevention</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">Instant Communication</div>
            <div class="feature-desc">Seamless doctor-patient interaction and consultation</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure & Private</div>
            <div class="feature-desc">Enterprise-grade security for your sensitive health data</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 Smart HealthCare Inc. | HIPAA Compliant | Built with ❤️ for better patient outcomes</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.6;">
            Trusted by 1,000+ healthcare professionals worldwide
        </p>
    </div>
    """, unsafe_allow_html=True)

# Check role redirects AFTER defining the main function
if st.session_state.role == "patient":
    st.switch_page("pages/login.py")
elif st.session_state.role == "doctor":
    st.switch_page("pages/doctor_dashboard.py")
else:
    # Only show the main content if no role is selected
    main()