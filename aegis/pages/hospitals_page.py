import folium
import streamlit as st
from streamlit_folium import st_folium

from aegis.hospitals import find_nearby_hospitals


def render_hospitals():
    st.markdown("## 🏥 Hospital & Healthcare Facility Finder")
    st.markdown("Locate nearby hospitals, urgent care centers, and specialized medical facilities.")

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        city = st.text_input("🏙️ City", value=st.session_state.get('hospital_city', 'New York'), key='hospital_city')

    with col2:
        state = st.text_input("🗺️ State", value=st.session_state.get('hospital_state', 'NY'), key='hospital_state')

    with col3:
        emergency_only = st.checkbox("🚨 Emergency Only", value=False)

    # Search filters
    with st.expander("🔍 Advanced Search Filters"):
        col1, col2 = st.columns(2)

        with col1:
            specialty_filter = st.multiselect(
                "Specialties:",
                ["Emergency Medicine", "Cardiology", "Neurology", "Pediatrics", 
                 "Surgery", "Orthopedics", "Oncology", "Mental Health"]
            )

            min_rating = st.slider("Minimum Rating:", 1.0, 5.0, 3.0, 0.1)

        with col2:
            max_distance = st.selectbox("Maximum Distance:", 
                                      ["5 miles", "10 miles", "25 miles", "50 miles", "Any"])

            sort_by = st.selectbox("Sort by:", 
                                 ["Distance", "Rating", "Emergency Services", "Specialties"])

    # --- Only create/update the map when the button is pressed ---
    if st.button("🔍 Find Healthcare Facilities", use_container_width=True, type="primary"):
        with st.spinner("🔍 Searching for healthcare facilities..."):
            hospitals = find_nearby_hospitals(city, state)
            # Apply filters
            if emergency_only:
                hospitals = [h for h in hospitals if h['emergency']]
            if specialty_filter:
                hospitals = [h for h in hospitals if any(spec in h.get('specialties', []) for spec in specialty_filter)]
            # Filter by rating
            hospitals = [h for h in hospitals if h['rating'] >= min_rating]
            # Sort results
            if sort_by == "Rating":
                hospitals.sort(key=lambda x: x['rating'], reverse=True)
            elif sort_by == "Emergency Services":
                hospitals.sort(key=lambda x: x['emergency'], reverse=True)
            # Use a stable city center for the map to prevent blinking
            city_centers = {
                'Chennai': [13.0827, 80.2707],
                'Coimbatore': [11.0168, 76.9558],
                'Madurai': [9.9252, 78.1198],
                'Tiruchirappalli': [10.7905, 78.7047],
                'Salem': [11.6643, 78.1460],
                # Add more Tamil Nadu cities as needed
            }
            city_key = city.strip().title()
            default_center = city_centers.get(city_key, [13.0827, 80.2707])  # Default: Chennai center
            if hospitals:
                avg_lat = sum(h['lat'] for h in hospitals) / len(hospitals)
                avg_lng = sum(h['lng'] for h in hospitals) / len(hospitals)
                map_center = [avg_lat, avg_lng]
            else:
                map_center = default_center
            import folium
            m = folium.Map(location=map_center, zoom_start=14, tiles=None)
            folium.TileLayer(
                tiles='https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}',
                attr='Google',
                name='Google Maps',
                overlay=False,
                                       control=True
            ).add_to(m)
            for hospital in hospitals:
                popup_text = f"""
                <div style='width: 200px;'>
                <b>{hospital['name']}</b><br>
                <i class='fa fa-map-marker'></i> {hospital['address']}<br>
                <i class='fa fa-phone'></i> {hospital['phone']}<br>
                <i class='fa fa-star'></i> Rating: {hospital['rating']}/5<br>
                <i class='fa fa-ambulance'></i> Emergency: {'Yes' if hospital['emergency'] else 'No'}<br>
                <a href='https://www.google.com/maps/search/?api=1&query={hospital['lat']},{hospital['lng']}' target='_blank'>Open in Google Maps</a>
                </div>
                """
                folium.Marker(
                    [hospital['lat'], hospital['lng']],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=hospital['name'],
                    icon=folium.Icon(
                        color='red' if hospital['emergency'] else 'blue',
                        icon='plus',
                        prefix='fa'
                    )
                ).add_to(m)
            st.session_state.hospital_map = m
            st.session_state.hospital_results = hospitals
            if not hospitals:
                st.warning("No facilities found matching your criteria. Try adjusting your filters.")

    # --- Always display the map and results from session state (never recreate here) ---
    if hasattr(st.session_state, 'hospital_map'):
        st.markdown('<div class="map-container">', unsafe_allow_html=True)
        st_folium(st.session_state.hospital_map, width=700, height=400)
        st.markdown('</div>', unsafe_allow_html=True)
        if hasattr(st.session_state, 'hospital_results') and st.session_state.hospital_results:
            st.markdown(f"### 🏥 Found {len(st.session_state.hospital_results)} Healthcare Facilities")
            st.markdown("---")
            for hospital in st.session_state.hospital_results:
                emergency_badge = "🚨 Emergency" if hospital['emergency'] else "🏥 General"
                rating_stars = "⭐" * int(hospital['rating']) + "☆" * (5 - int(hospital['rating']))
                with st.expander(f"{emergency_badge} | {hospital['name']} | {rating_stars} ({hospital['rating']})"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**📍 Address:** {hospital['address']}")
                        st.markdown(f"**📞 Phone:** {hospital['phone']}")
                        st.markdown(f"**🏥 Bed Capacity:** {hospital.get('beds', 'N/A')}")
                        st.markdown(f"**🚨 Emergency Services:** {'Available 24/7' if hospital['emergency'] else 'Not Available'}")
                        if hospital.get('specialties'):
                            st.markdown(f"**🔬 Specialties:** {', '.join(hospital['specialties'])}")
                    with col2:
                        st.markdown(f"**⭐ Rating:** {hospital['rating']}/5.0")
                        if st.button(f"📞 Call {hospital['name']}", key=f"call_{hospital['name']}"):
                            st.success(f"Calling {hospital['phone']}... (simulated)")
                        if st.button(f"🗺️ Get Directions", key=f"directions_{hospital['name']}"):
                            st.info(f"Opening directions to {hospital['address']}... (would integrate with maps)")
                        if hospital['emergency']:
                            if st.button(f"🚨 Emergency Contact", key=f"emergency_{hospital['name']}", type="primary"):
                                st.error(f"🚨 Contacting {hospital['name']} emergency department...")
