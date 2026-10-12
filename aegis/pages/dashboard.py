import streamlit as st
from datetime import datetime

from aegis.database import get_user_consultations, get_user_reminders


def render_dashboard():
    st.markdown("# 📊 Personal Health Dashboard")

    # Quick stats
    consultations = get_user_consultations(st.session_state.user['id'])
    reminders = get_user_reminders(st.session_state.user['id'])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #667eea; margin-bottom: 0.5rem;">📋 Total Consultations</h3>
            <h2 style="color: #2d3436; margin: 0; font-size: 2.5rem;">{len(consultations)}</h2>
            <p style="color: #636e72; margin: 0.5rem 0 0 0; font-size: 0.9rem;">All time record</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        recent_consultations = len([c for c in consultations if 
                                  (datetime.now() - datetime.strptime(c[6], '%Y-%m-%d %H:%M:%S')).days <= 7])
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00b894; margin-bottom: 0.5rem;">🗓️ This Week</h3>
            <h2 style="color: #2d3436; margin: 0; font-size: 2.5rem;">{recent_consultations}</h2>
            <p style="color: #636e72; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Recent activity</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #fdcb6e; margin-bottom: 0.5rem;">💊 Active Reminders</h3>
            <h2 style="color: #2d3436; margin: 0; font-size: 2.5rem;">{len(reminders)}</h2>
            <p style="color: #636e72; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Medicine schedule</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        health_score = min(100, 60 + (len(consultations) * 5) + (len(reminders) * 10))
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #e17055; margin-bottom: 0.5rem;">❤️ Health Score</h3>
            <h2 style="color: #2d3436; margin: 0; font-size: 2.5rem;">{health_score}%</h2>
            <p style="color: #636e72; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Wellness index</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # User-specific dashboard content
    if st.session_state.user.get('user_type') == 'medical_student':
        st.markdown("## 📚 Medical Student Hub")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 🎯 Learning Objectives Today
            - [ ] Review cardiovascular pathophysiology
            - [ ] Practice physical examination techniques
            - [ ] Study pharmacokinetics principles
            - [ ] Complete case study analysis
            """)

            if st.button("📖 Access Study Materials", use_container_width=True):
                st.info("Study materials would be integrated here in a full implementation")

        with col2:
            st.markdown("""
            ### 📊 Study Progress
            - **Cases Reviewed:** 15/50
            - **Quiz Average:** 87%
            - **Study Hours This Week:** 25
            - **Next Exam:** Cardiology (5 days)
            """)

            if st.button("📈 View Detailed Analytics", use_container_width=True):
                st.info("Detailed study analytics would be shown here")

    elif st.session_state.user.get('user_type') == 'healthcare_professional':
        st.markdown("## 👩‍⚕️ Professional Dashboard")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 🏥 Today's Schedule
            - **09:00 AM** - Patient Consultation
            - **11:00 AM** - Surgical Procedure
            - **02:00 PM** - Department Meeting  
            - **04:00 PM** - Research Review
            """)

            if st.button("📅 Manage Schedule", use_container_width=True):
                st.info("Calendar integration would be available here")

        with col2:
            st.markdown("""
            ### 📋 Clinical Updates
            - **New Guidelines:** Hypertension Management 2024
            - **Drug Alerts:** 2 new safety warnings
            - **Research:** 5 relevant studies published
            - **CME Credits:** 12/25 completed
            """)

            if st.button("🔬 View Clinical Resources", use_container_width=True):
                st.info("Clinical resources and guidelines would be displayed")

    else:  # Patient dashboard
        st.markdown("## 👤 Your Health Journey")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 🎯 Health Goals
            - [ ] Drink 8 glasses of water daily
            - [ ] Exercise 30 minutes, 5x per week
            - [ ] Take medications as prescribed
            - [ ] Get 7-8 hours of sleep
            """)

            if st.button("⚡ Quick Health Check", use_container_width=True):
                st.session_state.page = 'diagnosis'
                st.rerun()

        with col2:
            st.markdown("""
            ### 📈 Health Trends
            - **Water Intake:** 6/8 glasses today
            - **Sleep Quality:** Good (7.5 hrs)
            - **Exercise:** 3/5 sessions this week
            - **Medication Adherence:** 95%
            """)

            if st.button("💊 Manage Medications", use_container_width=True):
                st.session_state.page = 'reminders'
                st.rerun()

    # Quick actions section
    st.markdown("---")
    st.markdown("## 🚀 Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🩺 New Diagnosis", use_container_width=True):
            st.session_state.page = 'diagnosis'
            st.rerun()

    with col2:
        if st.button("💬 Ask AI Doctor", use_container_width=True):
            st.session_state.page = 'chatbot'
            st.rerun()

    with col3:
        if st.button("🏥 Find Care", use_container_width=True):
            st.session_state.page = 'hospitals'
            st.rerun()

    with col4:
        if st.button("📊 View Reports", use_container_width=True):
            st.session_state.page = 'reports'
            st.rerun()

    # Recent activity
    if consultations:
        st.markdown("---")
        st.markdown("## 📋 Recent Health Activity")

        for consultation in consultations[:2]:
            severity_color = "#e74c3c" if consultation[5] == "CRITICAL" else "#f39c12" if consultation[5] == "High" else "#27ae60"

            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {severity_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h4 style="margin: 0; color: #2d3436;">📅 {consultation[6][:16]}</h4>
                <p style="margin: 0.5rem 0; color: #636e72;"><strong>Symptoms:</strong> {consultation[2][:100]}{'...' if len(consultation[2]) > 100 else ''}</p>
                <p style="margin: 0; color: {severity_color};"><strong>Severity:</strong> {consultation[5]}</p>
            </div>
            """, unsafe_allow_html=True)
