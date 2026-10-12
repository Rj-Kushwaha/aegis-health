import streamlit as st

from aegis.database import init_database
from aegis.layout import render_sidebar
from aegis.pages.chatbot import render_chatbot
from aegis.pages.dashboard import render_dashboard
from aegis.pages.diagnosis import render_diagnosis
from aegis.pages.hospitals_page import render_hospitals
from aegis.pages.login import render_login
from aegis.pages.notifications import check_notifications, render_notification_toasts, render_notifications
from aegis.pages.reminders import render_reminders
from aegis.pages.reports_page import render_reports
from aegis.styles import apply_styles


def run_app():
    st.set_page_config(
        page_title="AEGIS HEALTH",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_database()
    apply_styles()

    st.markdown("""
        <div class="main-header">
            <h1 style="font-size: 3rem; margin-bottom: 1rem;">🩺 AEGIS HEALTH</h1>
            <p style="font-size: 1.2rem; opacity: 0.9;">Your Intelligent Medical Companion</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-quote">
            <h2 style="margin-bottom: 1rem; font-size: 1.8rem;">💫 "Health is not valued until sickness comes" 💫</h2>
            <p style="font-size: 1.1rem; opacity: 0.95; line-height: 1.6;">
                Empowering medical students, healthcare professionals, and patients with AI-driven insights for better health outcomes. 
                Your journey to wellness starts with informed decisions.
            </p>
        </div>
        """, unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    if 'voice_enabled' not in st.session_state:
        st.session_state.voice_enabled = False

    if not st.session_state.logged_in:
        render_login()
    else:
        render_sidebar()
        check_notifications()
        render_notification_toasts()
        page_renderers = {
            'dashboard': render_dashboard,
            'diagnosis': render_diagnosis,
            'chatbot': render_chatbot,
            'hospitals': render_hospitals,
            'reminders': render_reminders,
            'reports': render_reports,
            'notifications': render_notifications,
        }
        renderer = page_renderers.get(st.session_state.page)
        if renderer:
            renderer()

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem; color: #636e72;">
            <strong>AEGIS HEALTH</strong> · Your Intelligent Medical Companion
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 1rem; margin-top: 1rem;">
            <strong>Medical Disclaimer:</strong> This demo is for informational and educational purposes only,
            and is not a substitute for professional medical advice, diagnosis, or treatment.
            For a medical emergency, contact local emergency services immediately.
        </div>
        """,
        unsafe_allow_html=True,
    )
