import re
import time
import streamlit as st

from aegis.auth import authenticate_user, create_user
from aegis.database import create_water_reminder


def render_login():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

        with tab1:
            st.markdown("### Welcome Back to Your Health Journey!")
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                login_button = st.form_submit_button("🚀 Login", use_container_width=True)

                if login_button:
                    if username and password:
                        user = authenticate_user(username, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user = user
                            # Create water reminders for the day
                            create_water_reminder(user['id'])
                            st.success("✅ Welcome back! Logging you in...")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Please try again.")
                    else:
                        st.warning("⚠️ Please fill in all fields")

        with tab2:
            st.markdown("### Join Our Healthcare Community!")
            with st.form("signup_form"):
                new_username = st.text_input("Choose Username", placeholder="Your unique username")
                new_email = st.text_input("Email Address", placeholder="your.email@example.com")

                # User type selection with descriptions
                user_type = st.selectbox(
                    "I am a:",
                    options=['patient', 'medical_student', 'healthcare_professional'],
                    format_func=lambda x: {
                        'patient': '👤 Patient - Seeking health guidance',
                        'medical_student': '📚 Medical Student - Learning and practicing',
                        'healthcare_professional': '👩‍⚕️ Healthcare Professional - Clinical practice'
                    }[x]
                )

                # Additional fields based on user type
                medical_id = None
                specialization = None

                if user_type == 'medical_student':
                    medical_id = st.text_input("Student ID", placeholder="Medical school ID number")
                    specialization = st.selectbox(
                        "Year of Study:",
                        ["Pre-clinical Year 1", "Pre-clinical Year 2", "Clinical Year 3", 
                         "Clinical Year 4", "Intern", "Resident"]
                    )
                elif user_type == 'healthcare_professional':
                    medical_id = st.text_input("License/Registration Number", placeholder="Professional license number")
                    specialization = st.selectbox(
                        "Specialty:",
                        ["Family Medicine", "Internal Medicine", "Pediatrics", "Surgery", 
                         "Emergency Medicine", "Cardiology", "Neurology", "Psychiatry", 
                         "Radiology", "Anesthesiology", "Other"]
                    )

                col1, col2 = st.columns(2)
                with col1:
                    new_password = st.text_input("Create Password", type="password", 
                                               placeholder="Minimum 8 characters")
                    age = st.number_input("Age", min_value=0, max_value=120, step=1, value=25)
                    height = st.number_input("Height (cm)", min_value=50, max_value=250, step=1, value=170)

                with col2:
                    confirm_password = st.text_input("Confirm Password", type="password", 
                                                   placeholder="Re-enter your password")
                    weight = st.number_input("Weight (kg)", min_value=10, max_value=300, step=1, value=70)

                    bmi = 0
                    if height > 0 and weight > 0:
                        bmi = round(weight / ((height / 100) ** 2), 2)

                    st.text_input("BMI (Auto-calculated)", value=str(bmi) if bmi > 0 else "", disabled=True)

                terms_agreed = st.checkbox("I agree to the Terms of Service and Privacy Policy")
                signup_button = st.form_submit_button("🎉 Create Account", use_container_width=True)

                if signup_button:
                    if all([new_username, new_email, new_password, confirm_password, age, height, weight]) and terms_agreed:
                        if new_password == confirm_password:
                            if len(new_password) >= 8:
                                if re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                                    # Additional validation for professionals
                                    if user_type in ['medical_student', 'healthcare_professional'] and not medical_id:
                                        st.error("Please provide your medical ID/license number")
                                    else:
                                        if create_user(new_username, new_email, new_password, age, height, 
                                                     weight, bmi, user_type, medical_id, specialization):
                                            st.success("🎉 Account created successfully! Please login to continue.")
                                            st.balloons()
                                        else:
                                            st.error("❌ Username or email already exists")
                                else:
                                    st.error("📧 Please enter a valid email address")
                            else:
                                st.error("🔒 Password must be at least 8 characters long")
                        else:
                            st.error("❌ Passwords don't match")
                    elif not terms_agreed:
                        st.error("📋 Please agree to the Terms of Service")
                    else:
                        st.warning("⚠️ Please fill in all required fields")
