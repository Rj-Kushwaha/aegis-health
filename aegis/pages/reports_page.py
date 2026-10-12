import json
import pandas as pd
import streamlit as st
from datetime import datetime

from aegis.database import get_user_consultations, get_user_reminders
from aegis.reports import generate_pdf_report


def render_reports():
    st.markdown("## 📊 Health Reports & Analytics")
    st.markdown("Comprehensive view of your health data and consultation history.")

    consultations = get_user_consultations(st.session_state.user['id'])

    if consultations:
        # Enhanced analytics dashboard
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📋 Total Consultations", len(consultations))

        with col2:
            critical_count = len([c for c in consultations if c[5] == 'CRITICAL'])
            st.metric("⚠️ Critical Cases", critical_count)

        with col3:
            recent_count = len([c for c in consultations if 
                              (datetime.now() - datetime.strptime(c[6], '%Y-%m-%d %H:%M:%S')).days <= 30])
            st.metric("📅 Last 30 Days", recent_count)

        with col4:
            avg_gap = "N/A"
            if len(consultations) > 1:
                dates = [datetime.strptime(c[6], '%Y-%m-%d %H:%M:%S') for c in consultations]
                dates.sort()
                gaps = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
                avg_gap = f"{sum(gaps) // len(gaps)} days"
            st.metric("📊 Avg. Gap", avg_gap)

        # Filters and analytics
        tab1, tab2, tab3 = st.tabs(["📋 Consultation History", "📈 Health Analytics", "💾 Export Data"])

        with tab1:
            # Enhanced filtering
            col1, col2, col3 = st.columns(3)

            with col1:
                severity_filter = st.selectbox(
                    "Filter by Severity:",
                    options=['All', 'CRITICAL', 'High', 'Medium', 'Low']
                )

            with col2:
                date_range = st.selectbox(
                    "Date Range:",
                    options=['All Time', 'Last 7 Days', 'Last 30 Days', 'Last 90 Days', 'Last Year']
                )

            with col3:
                sort_option = st.selectbox(
                    "Sort by:",
                    options=['Newest First', 'Oldest First', 'Severity (High to Low)', 'Severity (Low to High)']
                )

            # Apply filters
            filtered_consultations = consultations.copy()

            if severity_filter != 'All':
                filtered_consultations = [c for c in filtered_consultations if c[5] == severity_filter]

            if date_range != 'All Time':
                days_map = {
                    'Last 7 Days': 7, 'Last 30 Days': 30, 
                    'Last 90 Days': 90, 'Last Year': 365
                }
                days = days_map[date_range]
                filtered_consultations = [
                    c for c in filtered_consultations 
                    if (datetime.now() - datetime.strptime(c[6], '%Y-%m-%d %H:%M:%S')).days <= days
                ]

            # Apply sorting
            if sort_option == 'Oldest First':
                filtered_consultations.reverse()
            elif 'Severity' in sort_option:
                severity_order = {'CRITICAL': 4, 'High': 3, 'Medium': 2, 'Low': 1}
                reverse_sort = 'High to Low' in sort_option
                filtered_consultations.sort(key=lambda x: severity_order.get(x[5], 0), reverse=reverse_sort)

            st.markdown(f"### 📋 Showing {len(filtered_consultations)} consultations")

            # Display consultations with enhanced cards
            for i, consultation in enumerate(filtered_consultations):
                severity_colors = {
                    'CRITICAL': '#e74c3c',
                    'High': '#f39c12', 
                    'Medium': '#f1c40f',
                    'Low': '#27ae60'
                }

                severity_icons = {
                    'CRITICAL': '🚨',
                    'High': '⚠️',
                    'Medium': '🟡',
                    'Low': '✅'
                }

                color = severity_colors.get(consultation[5], '#95a5a6')
                icon = severity_icons.get(consultation[5], '📋')

                with st.expander(f"{icon} {consultation[6][:16]} - {consultation[5]} Severity"):
                    st.markdown(f"""
                    <div style="border-left: 4px solid {color}; padding-left: 1rem; margin-bottom: 1rem;">
                        <h4 style="color: {color}; margin-bottom: 0.5rem;">
                            {icon} {consultation[5]} Priority Case
                        </h4>
                        <p style="margin-bottom: 0.5rem;"><strong>Date:</strong> {consultation[6]}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.markdown("**🩺 Reported Symptoms:**")
                        st.write(consultation[2])

                        st.markdown("**🔍 AI Assessment:**")
                        st.write(consultation[3])

                        st.markdown("**💡 Recommendations:**")
                        recommendations = consultation[4].split(', ')
                        for rec in recommendations:
                            st.write(f"• {rec}")

                    with col2:
                        st.markdown(f"**⚠️ Severity:** {consultation[5]}")
                        st.markdown(f"**📅 Date:** {consultation[6][:10]}")
                        st.markdown(f"**⏰ Time:** {consultation[6][11:16]}")

                        # Individual report download
                        consultation_data = {
                            'date': consultation[6],
                            'symptoms': consultation[2],
                            'diagnosis': consultation[3],
                            'severity': consultation[5],
                            'recommendations': consultation[4].split(', ')
                        }

                        pdf_buffer = generate_pdf_report(consultation_data, st.session_state.user)

                        st.download_button(
                            label="📄 PDF",
                            data=pdf_buffer.getvalue(),
                            file_name=f"report_{consultation[6][:10]}_{i}.pdf",
                            mime="application/pdf",
                            key=f"pdf_download_{i}",
                            use_container_width=True
                        )

        with tab2:
            st.markdown("### 📈 Health Analytics & Insights")

            if len(consultations) >= 2:
                # Health trends analysis
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### 📊 Severity Distribution")
                    severity_counts = {}
                    for consultation in consultations:
                        severity = consultation[5]
                        severity_counts[severity] = severity_counts.get(severity, 0) + 1

                    severity_df = pd.DataFrame(
                        list(severity_counts.items()), 
                        columns=['Severity', 'Count']
                    )
                    st.bar_chart(severity_df.set_index('Severity'))

                with col2:
                    st.markdown("#### 📅 Monthly Activity")
                    monthly_counts = {}
                    for consultation in consultations:
                        month = consultation[6][:7]  # YYYY-MM
                        monthly_counts[month] = monthly_counts.get(month, 0) + 1

                    if len(monthly_counts) > 1:
                        monthly_df = pd.DataFrame(
                            list(monthly_counts.items()), 
                            columns=['Month', 'Consultations']
                        )
                        st.line_chart(monthly_df.set_index('Month'))
                    else:
                        st.info("Need more data points for trend analysis")

                # Health insights
                st.markdown("#### 🔍 AI Health Insights")

                # Calculate patterns
                recent_severity = [c[5] for c in consultations[:5]]  # Last 5 consultations
                critical_trend = recent_severity.count('CRITICAL')
                high_trend = recent_severity.count('High')

                if critical_trend > 0:
                    st.error(f"⚠️ You have {critical_trend} critical case(s) in your recent history. Consider following up with healthcare providers.")
                elif high_trend >= 2:
                    st.warning(f"🟡 You have {high_trend} high-priority cases recently. Monitor symptoms and seek medical advice.")
                else:
                    st.success("✅ Your recent health consultations show manageable concerns.")

                # Symptom analysis
                all_symptoms = ' '.join([c[2] for c in consultations]).lower()
                common_keywords = ['headache', 'fever', 'pain', 'nausea', 'fatigue', 'cough']
                symptom_frequency = {keyword: all_symptoms.count(keyword) for keyword in common_keywords if all_symptoms.count(keyword) > 0}

                if symptom_frequency:
                    st.markdown("#### 🎯 Most Reported Symptoms")
                    for symptom, count in sorted(symptom_frequency.items(), key=lambda x: x[1], reverse=True)[:5]:
                        st.write(f"• **{symptom.title()}:** {count} times")

            else:
                st.info("📊 More consultation data needed for detailed analytics. Continue using the symptom checker to build your health profile.")

        with tab3:
            st.markdown("### 💾 Export & Backup Your Health Data")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📄 Individual Reports")

                export_format = st.selectbox(
                    "Choose format:",
                    ["PDF Report", "JSON Data", "CSV Summary"]
                )

                selected_consultations = st.multiselect(
                    "Select consultations to export:",
                    options=[(i, f"{c[6][:16]} - {c[5]}") for i, c in enumerate(consultations)],
                    format_func=lambda x: x[1],
                    default=[(i, f"{c[6][:16]} - {c[5]}") for i, c in enumerate(consultations[:3])]
                )

                if st.button("📥 Export Selected", use_container_width=True) and selected_consultations:
                    if export_format == "PDF Report":
                        st.info("Individual PDF exports available in the consultation cards above")
                    elif export_format == "JSON Data":
                        selected_data = []
                        for idx, _ in selected_consultations:
                            consultation = consultations[idx]
                            selected_data.append({
                                'date': consultation[6],
                                'symptoms': consultation[2],
                                'diagnosis': consultation[3],
                                'severity': consultation[5],
                                'recommendations': consultation[4].split(', ')
                            })

                        export_json = json.dumps({
                            'user': st.session_state.user['username'],
                            'export_date': datetime.now().isoformat(),
                            'consultations': selected_data
                        }, indent=2)

                        st.download_button(
                            label="📥 Download JSON Export",
                            data=export_json,
                            file_name=f"health_data_export_{datetime.now().strftime('%Y%m%d')}.json",
                            mime="application/json",
                            use_container_width=True
                        )

            with col2:
                st.markdown("#### 📊 Complete Health Summary")

                if st.button("📋 Generate Comprehensive Report", use_container_width=True):
                    # Create comprehensive health summary
                    summary_data = {
                        'user_profile': {
                            'username': st.session_state.user['username'],
                            'user_type': st.session_state.user.get('user_type', 'patient'),
                            'total_consultations': len(consultations),
                            'date_range': f"{consultations[-1][6][:10]} to {consultations[0][6][:10]}" if consultations else "N/A"
                        },
                        'health_statistics': {
                            'critical_cases': len([c for c in consultations if c[5] == 'CRITICAL']),
                            'high_priority': len([c for c in consultations if c[5] == 'High']),
                            'medium_priority': len([c for c in consultations if c[5] == 'Medium']),
                            'low_priority': len([c for c in consultations if c[5] == 'Low'])
                        },
                        'recent_activity': [
                            {
                                'date': c[6],
                                'severity': c[5],
                                'symptoms_summary': c[2][:100] + '...' if len(c[2]) > 100 else c[2]
                            } for c in consultations[:10]
                        ]
                    }

                    summary_json = json.dumps(summary_data, indent=2)

                    st.download_button(
                        label="📥 Download Complete Summary",
                        data=summary_json,
                        file_name=f"complete_health_summary_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json",
                        use_container_width=True
                    )

                st.markdown("#### 🔄 Data Backup")
                st.info("💡 **Tip:** Regularly backup your health data for your records and to share with healthcare providers.")

                if st.button("☁️ Backup All Data", use_container_width=True):
                    # Complete data backup
                    backup_data = {
                        'backup_info': {
                            'created_date': datetime.now().isoformat(),
                            'user_id': st.session_state.user['id'],
                            'username': st.session_state.user['username'],
                            'backup_version': '1.0'
                        },
                        'consultations': [
                            {
                                'id': c[0],
                                'symptoms': c[2],
                                'diagnosis': c[3],
                                'recommendations': c[4],
                                'severity': c[5],
                                'date': c[6]
                            } for c in consultations
                        ],
                        'reminders': [
                            {
                                'medicine_name': r[2],
                                'dosage': r[3],
                                'frequency': r[4],
                                'time_slots': json.loads(r[5]) if r[5] else [],
                                'start_date': r[6],
                                'end_date': r[7],
                                'active': r[8]
                            } for r in get_user_reminders(st.session_state.user['id'])
                        ]
                    }

                    backup_json = json.dumps(backup_data, indent=2)

                    st.download_button(
                        label="📥 Download Complete Backup",
                        data=backup_json,
                        file_name=f"aegis_health_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )

    else:
        st.info("📋 No consultation records found. Start by using our Symptom Diagnosis tool to build your health profile!")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🩺 Start First Diagnosis", use_container_width=True, type="primary"):
                st.session_state.page = 'diagnosis'
                st.rerun()

        with col2:
            if st.button("💬 Ask Health Questions", use_container_width=True):
                st.session_state.page = 'chatbot'
                st.rerun()

        with col3:
            if st.button("🏥 Find Nearby Care", use_container_width=True):
                st.session_state.page = 'hospitals'
                st.rerun()
