import json
import streamlit as st
from datetime import datetime

from aegis.analysis import analyze_symptoms
from aegis.database import save_consultation
from aegis.reports import generate_pdf_report


def render_diagnosis():
    st.markdown("## 🩺 AI-Powered Symptom Analysis")
    st.markdown("Describe your symptoms for a comprehensive health assessment tailored to your profile.")

    # User type specific instructions
    user_type = st.session_state.user.get('user_type', 'patient')

    if user_type == 'medical_student':
        st.info("📚 **Student Mode**: This analysis will include educational context and differential diagnosis considerations.")
    elif user_type == 'healthcare_professional':
        st.info("👩‍⚕️ **Professional Mode**: Assessment includes clinical guidelines and professional insights.")

    with st.form("diagnosis_form"):
        col1, col2 = st.columns([3, 1])

        with col1:
            symptoms = st.text_area(
                "Describe symptoms in detail:",
                placeholder="e.g., I've been experiencing chest pain for 2 hours, accompanied by shortness of breath and sweating. The pain is crushing and radiates to my left arm...",
                height=150
            )

        with col2:
            st.markdown("### 🎯 Quick Symptom Checker")
            common_symptoms = st.multiselect(
                "Select common symptoms:",
                ["Fever", "Headache", "Nausea", "Fatigue", "Cough", 
                 "Chest Pain", "Abdominal Pain", "Dizziness", "Rash"]
            )

            severity_self_assessment = st.slider("Pain level (1-10):", 1, 10, 5)

        analyze_button = st.form_submit_button("🔍 Analyze Symptoms", use_container_width=True)

    # Initialize session state for results
    if 'diagnosis_result' not in st.session_state:
        st.session_state.diagnosis_result = None
    if 'recommendations_result' not in st.session_state:
        st.session_state.recommendations_result = None
    if 'severity_result' not in st.session_state:
        st.session_state.severity_result = None
    if 'symptoms_result' not in st.session_state:
        st.session_state.symptoms_result = None
    if 'professional_note_result' not in st.session_state:
        st.session_state.professional_note_result = None

    if analyze_button and (symptoms or common_symptoms):
        # Combine text and selected symptoms
        full_symptoms = symptoms
        if common_symptoms:
            full_symptoms += f"\nAdditional symptoms: {', '.join(common_symptoms)}"
        if severity_self_assessment >= 7:
            full_symptoms += f"\nSevere pain level: {severity_self_assessment}/10"

        diagnosis, severity, recommendations, professional_note = analyze_symptoms(full_symptoms, user_type)

        # Store results in session state
        st.session_state.diagnosis_result = diagnosis
        st.session_state.recommendations_result = recommendations
        st.session_state.severity_result = severity
        st.session_state.symptoms_result = full_symptoms
        st.session_state.professional_note_result = professional_note

        # Save consultation
        save_consultation(
            st.session_state.user['id'],
            full_symptoms,
            diagnosis,
            ', '.join(recommendations),
            severity
        )

    # Display results if available
    if st.session_state.diagnosis_result and st.session_state.symptoms_result:
        diagnosis = st.session_state.diagnosis_result
        recommendations = st.session_state.recommendations_result
        severity = st.session_state.severity_result
        symptoms = st.session_state.symptoms_result
        professional_note = st.session_state.professional_note_result

        st.markdown("---")

        # Display diagnosis with appropriate styling
        if severity == "CRITICAL":
            st.markdown(f"""
            <div class="emergency-alert">
                <h2>🚨 {diagnosis}</h2>
                <p style="font-size: 1.1rem; margin-top: 1rem;">
                    This appears to be a medical emergency. Immediate action is required.
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif severity == "High":
            st.error(f"⚠️ **{diagnosis}**")
        elif severity == "Medium":
            st.warning(f"🟡 **{diagnosis}**")
        else:
            st.success(f"ℹ️ **{diagnosis}**")

        # Professional context
        if professional_note:
            st.info(professional_note)

        # Recommendations
        st.markdown("### 📝 Personalized Recommendations")

        for i, rec in enumerate(recommendations, 1):
            if severity == "CRITICAL":
                st.error(f"**{i}.** {rec}")
            elif severity == "High":
                st.warning(f"**{i}.** {rec}")
            else:
                st.info(f"**{i}.** {rec}")

        # Additional resources based on user type
        if user_type == 'medical_student':
            with st.expander("📚 Educational Resources & Learning Points"):
                st.markdown("""
                **Learning Objectives:**
                - Practice systematic symptom assessment
                - Consider differential diagnosis approach
                - Review pathophysiology of identified conditions
                - Study evidence-based treatment protocols

                **Suggested Reading:**
                - Harrison's Principles of Internal Medicine
                - Current Medical Diagnosis & Treatment
                - Clinical examination techniques
                """)

        elif user_type == 'healthcare_professional':
            with st.expander("👩‍⚕️ Clinical Decision Support"):
                st.markdown("""
                **Clinical Considerations:**
                - Review patient history and comorbidities
                - Consider diagnostic workup and imaging
                - Evaluate need for specialist consultation
                - Document findings and follow-up plan

                **Guidelines & Protocols:**
                - Latest clinical practice guidelines
                - Institutional protocols
                - Quality measures and indicators
                """)

        # Download options
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        consultation_data = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'symptoms': symptoms,
            'diagnosis': diagnosis,
            'severity': severity,
            'recommendations': recommendations,
            'user_type': user_type,
            'professional_note': professional_note
        }

        with col1:
            pdf_buffer = generate_pdf_report(consultation_data, st.session_state.user)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer.getvalue(),
                file_name=f"medical_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col2:
            json_data = json.dumps(consultation_data, indent=2)
            st.download_button(
                label="💾 Download JSON Data",
                data=json_data,
                file_name=f"medical_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

        with col3:
            if st.button("🔄 New Analysis", use_container_width=True):
                # Clear results
                st.session_state.diagnosis_result = None
                st.session_state.recommendations_result = None
                st.session_state.severity_result = None
                st.session_state.symptoms_result = None
                st.session_state.professional_note_result = None
                st.rerun()
