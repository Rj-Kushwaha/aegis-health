import streamlit as st
from datetime import datetime

from aegis.database import get_and_mark_due_notifications


def render_notifications():
    st.markdown("## 🔔 Notification Center")

    tab1, tab2 = st.tabs(["📬 All Notifications", "⚙️ Settings"])

    with tab1:
        if st.session_state.notifications:
            st.markdown(f"### 📬 Your Notifications ({len(st.session_state.notifications)})")

            # Group notifications by type
            notification_types = {}
            for notif in st.session_state.notifications:
                notif_type = notif['type']
                if notif_type not in notification_types:
                    notification_types[notif_type] = []
                notification_types[notif_type].append(notif)

            for notif_type, notifications in notification_types.items():
                type_icon = "💧" if notif_type == 'water' else "💊" if notif_type == 'medicine' else "🔔"
                type_name = notif_type.replace('_', ' ').title()

                with st.expander(f"{type_icon} {type_name} ({len(notifications)})"):
                    for notif in notifications[-10:]:  # Show last 10 of each type
                        st.markdown(f"""
                        <div style="background: white; padding: 0.75rem; border-radius: 8px; 
                                   margin: 0.25rem 0; border-left: 3px solid #667eea;">
                            <strong>{notif['message']}</strong>
                            <br><small style="color: #636e72;">⏰ {notif['time']}</small>
                        </div>
                        """, unsafe_allow_html=True)

            if st.button("🗑️ Clear All Notifications", type="secondary"):
                st.session_state.notifications = []
                st.success("All notifications cleared!")
                st.rerun()

        else:
            st.info("📭 No notifications yet. Your reminders and alerts will appear here.")

    with tab2:
        st.markdown("### ⚙️ Notification Preferences")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 💊 Medicine Reminders")
            medicine_notifications = st.radio(
                "Medicine reminder notifications:",
                ["All reminders", "Critical only", "Disabled"],
                index=0
            )

            snooze_duration = st.selectbox(
                "Snooze duration:",
                ["5 minutes", "10 minutes", "15 minutes", "30 minutes"]
            )

            st.markdown("#### 💧 Health Reminders")
            water_reminders = st.checkbox("Water intake reminders", value=True)
            exercise_reminders = st.checkbox("Exercise reminders", value=True)
            sleep_reminders = st.checkbox("Sleep schedule reminders", value=False)

        with col2:
            st.markdown("#### 🔊 Alert Settings")
            sound_alerts = st.checkbox("Sound alerts", value=True)
            push_notifications = st.checkbox("Push notifications", value=True)
            email_notifications = st.checkbox("Email notifications", value=False)

            st.markdown("#### ⏰ Quiet Hours")
            quiet_start = st.time_input("Quiet hours start:", value=datetime.strptime("22:00", "%H:%M").time())
            quiet_end = st.time_input("Quiet hours end:", value=datetime.strptime("07:00", "%H:%M").time())

        if st.button("💾 Save Notification Settings", use_container_width=True, type="primary"):
            st.success("✅ Notification preferences saved successfully!")



def check_notifications():
    user = st.session_state.user
    if user:
        due_notifications = get_and_mark_due_notifications(user['id'], datetime.now())
        for notification in due_notifications:
            st.session_state.notifications.append({
                'id': notification[0],
                'type': notification[2],
                'message': notification[3],
                'time': notification[4],
            })


def render_notification_toasts():
    if st.session_state.notifications:
        for notification in st.session_state.notifications[-3:]:
            st.markdown(f"""
                <div class="notification-card">
                    <strong>{notification['message']}</strong>
                    <br><small>⏰ {notification['time']}</small>
                </div>
                """, unsafe_allow_html=True)
