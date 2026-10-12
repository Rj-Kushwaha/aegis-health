import json
import streamlit as st
from datetime import datetime, timedelta

from aegis.database import add_medicine_reminder, create_water_reminder, get_user_reminders


def render_reminders():
    st.markdown("## 💊 Medicine Reminders & Health Notifications")

    tab1, tab2, tab3 = st.tabs(["💊 My Medications", "➕ Add New", "🔔 Notifications"])

    with tab1:
        reminders = get_user_reminders(st.session_state.user['id'])

        if reminders:
            st.markdown("### 📋 Your Current Medications")

            for reminder in reminders:
                time_slots = json.loads(reminder[5]) if reminder[5] else []

                with st.expander(f"💊 {reminder[2]} - {reminder[3]}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**Dosage:** {reminder[3]}")
                        st.write(f"**Frequency:** {reminder[4]}")
                        st.write(f"**Duration:** {reminder[6]} to {reminder[7]}")

                    with col2:
                        st.write(f"**Times:** {', '.join(time_slots)}")
                        st.write(f"**Status:** {'🟢 Active' if reminder[8] else '🔴 Inactive'}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✅ Mark as Taken", key=f"taken_{reminder[0]}"):
                            st.success("✅ Medication marked as taken!")
                    with col2:
                        if st.button(f"❌ Deactivate", key=f"deactivate_{reminder[0]}"):
                            # Deactivate reminder logic here
                            st.info("Reminder deactivated")
        else:
            st.info("📭 No active medication reminders. Add your first medication below!")

    with tab2:
        st.markdown("### ➕ Add New Medication Reminder")

        with st.form("add_reminder"):
            col1, col2 = st.columns(2)

            with col1:
                medicine_name = st.text_input("💊 Medicine Name", placeholder="e.g., Aspirin, Metformin")
                dosage = st.text_input("📏 Dosage", placeholder="e.g., 100mg, 1 tablet")
                frequency = st.selectbox("🔄 Frequency", 
                                        ["Once daily", "Twice daily", "Three times daily", 
                                         "Every 6 hours", "Every 8 hours", "As needed"])

            with col2:
                start_date = st.date_input("📅 Start Date", value=datetime.now().date())
                end_date = st.date_input("📅 End Date", value=datetime.now().date() + timedelta(days=30))

                # Time selection based on frequency
                st.markdown("⏰ **Select Times:**")
                time_slots = []

                if "Once" in frequency:
                    time_slots.append(st.time_input("Time", value=datetime.strptime("09:00", "%H:%M").time()).strftime("%H:%M"))
                elif "Twice" in frequency:
                    col_t1, col_t2 = st.columns(2)
                    with col_t1:
                        time_slots.append(st.time_input("Morning", value=datetime.strptime("09:00", "%H:%M").time()).strftime("%H:%M"))
                    with col_t2:
                        time_slots.append(st.time_input("Evening", value=datetime.strptime("21:00", "%H:%M").time()).strftime("%H:%M"))
                elif "Three" in frequency:
                    col_t1, col_t2, col_t3 = st.columns(3)
                    with col_t1:
                        time_slots.append(st.time_input("Morning", value=datetime.strptime("09:00", "%H:%M").time()).strftime("%H:%M"))
                    with col_t2:
                        time_slots.append(st.time_input("Afternoon", value=datetime.strptime("15:00", "%H:%M").time()).strftime("%H:%M"))
                    with col_t3:
                        time_slots.append(st.time_input("Evening", value=datetime.strptime("21:00", "%H:%M").time()).strftime("%H:%M"))

            special_instructions = st.text_area("📝 Special Instructions", 
                                              placeholder="e.g., Take with food, avoid alcohol")

            submit_reminder = st.form_submit_button("💾 Save Medication Reminder", use_container_width=True)

            if submit_reminder and medicine_name and dosage and time_slots:
                add_medicine_reminder(
                    st.session_state.user['id'],
                    medicine_name,
                    dosage,
                    frequency,
                    time_slots,
                    start_date.strftime('%Y-%m-%d'),
                    end_date.strftime('%Y-%m-%d')
                )
                st.success("✅ Medication reminder created successfully!")
                st.balloons()
                st.rerun()

    with tab3:
        st.markdown("### 🔔 Health Notifications & Reminders")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            #### 💧 Water Intake Reminders
            Stay hydrated throughout the day with personalized reminders.
            """)

            water_frequency = st.selectbox("Reminder frequency:", 
                                         ["Every 2 hours", "Every 3 hours", "Every 4 hours"])

            if st.button("💧 Enable Water Reminders", use_container_width=True):
                hours = int(water_frequency.split()[1])
                create_water_reminder(st.session_state.user['id'], hours)
                st.success(f"💧 Water reminders set for every {hours} hours!")

        with col2:
            st.markdown("""
            #### 🏃‍♂️ Exercise Reminders  
            Get motivated to stay active with regular exercise prompts.
            """)

            exercise_time = st.time_input("Preferred exercise time:", value=datetime.strptime("07:00", "%H:%M").time())

            if st.button("🏃‍♂️ Enable Exercise Reminders", use_container_width=True):
                st.success("🏃‍♂️ Exercise reminders activated!")

        # Recent notifications
        if st.session_state.notifications:
            st.markdown("---")
            st.markdown("### 📬 Recent Notifications")

            for notification in st.session_state.notifications[-10:]:
                notification_type = "💧" if notification['type'] == 'water' else "💊" if notification['type'] == 'medicine' else "🔔"

                st.markdown(f"""
                <div class="notification-card">
                    <span style="font-size: 1.2rem;">{notification_type}</span>
                    <strong>{notification['message']}</strong>
                    <br><small style="opacity: 0.7;">⏰ {notification['time']}</small>
                </div>
                """, unsafe_allow_html=True)
