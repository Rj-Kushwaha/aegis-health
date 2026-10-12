import streamlit as st


def render_sidebar():
    with st.sidebar:
        _render_sidebar_content()


def _render_sidebar_content():
    user_type_colors = {
        'patient': 'patient-badge',
        'medical_student': 'student-badge', 
        'healthcare_professional': 'professional-badge'
    }

    user_type_icons = {
        'patient': '👤',
        'medical_student': '📚',
        'healthcare_professional': '👩‍⚕️'
    }

    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 1rem;">
        <h3 style="color: white; margin: 0;">Welcome back!</h3>
        <h2 style="color: white; margin: 0.5rem 0;">{st.session_state.user['username']}</h2>
        <span class="{user_type_colors.get(st.session_state.user.get('user_type', 'patient'), 'patient-badge')}">
            {user_type_icons.get(st.session_state.user.get('user_type', 'patient'), '👤')} 
            {st.session_state.user.get('user_type', 'patient').replace('_', ' ').title()}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Navigation buttons
    st.markdown("### 🧭 Navigation")

    nav_buttons = [
        ("🏠 Dashboard", "dashboard", "🏠"),
        ("🩺 Symptom Diagnosis", "diagnosis", "🩺"),
        ("💬 Medical Chatbot", "chatbot", "💬"),
        ("🏥 Find Hospitals", "hospitals", "🏥"),
        ("💊 Medicine Reminders", "reminders", "💊"),
        ("📊 My Reports", "reports", "📊"),
        ("🔔 Notifications", "notifications", "🔔")
    ]

    for button_text, page_key, icon in nav_buttons:
        if st.button(button_text, use_container_width=True, key=f"nav_{page_key}"):
            st.session_state.page = page_key
            st.rerun()

    # Quick health tips based on user type
    st.markdown("---")
    if st.session_state.user.get('user_type') == 'medical_student':
        st.markdown("""
        ### 📚 Study Tips
        - Review cases daily
        - Practice differential diagnosis
        - Join study groups
        - Use evidence-based resources
        """)
    elif st.session_state.user.get('user_type') == 'healthcare_professional':
        st.markdown("""
        ### 👩‍⚕️ Professional Resources
        - Latest clinical guidelines
        - Continuing education credits
        - Peer consultation network
        - Research updates
        """)
    else:
        st.markdown("""
        ### 💡 Health Tips
        - Stay hydrated (8 glasses/day)
        - Regular exercise (150 min/week)
        - 7-9 hours sleep
        - Balanced nutrition
        """)

    st.markdown("---")

    # Emergency contacts
    st.markdown("""
    ### 🚨 Tamil Nadu Emergency Contacts
    **Medical Helpline:** 104  
    **Ambulance:** 108  
    **Police:** 100  
    """)

    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = 'login'
        st.session_state.notifications = []
        st.rerun()
