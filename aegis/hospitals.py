import folium
import streamlit as st


@st.cache_data(show_spinner=False)
def get_hospital_map(hospitals, center):
    # Create map with stable tile layer
    # Calculate the average latitude and longitude for better centering
    if hospitals:
        avg_lat = sum(h['lat'] for h in hospitals) / len(hospitals)
        avg_lng = sum(h['lng'] for h in hospitals) / len(hospitals)
        map_center = [avg_lat, avg_lng]
    else:
        map_center = center
    m = folium.Map(
        location=map_center,
        zoom_start=13,
        tiles='OpenStreetMap',
        prefer_canvas=True
    )
    
    for hospital in hospitals:
        popup_text = f"""
        <div style="width: 200px;">
        <b>{hospital['name']}</b><br>
        <i class="fa fa-map-marker"></i> {hospital['address']}<br>
        <i class="fa fa-phone"></i> {hospital['phone']}<br>
        <i class="fa fa-star"></i> Rating: {hospital['rating']}/5<br>
        <i class="fa fa-ambulance"></i> Emergency: {'Yes' if hospital['emergency'] else 'No'}
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
    
    return m


def find_nearby_hospitals(city, state):
    """Return Tamil Nadu hospital data for demo purposes"""
    tamil_nadu_hospitals = [
        {
            'name': 'Apollo Hospital Chennai',
            'address': '21, Greams Lane, Off Greams Road, Chennai, Tamil Nadu',
            'phone': '044-2829 3333',
            'rating': 4.7,
            'emergency': True,
            'specialties': ['Emergency Medicine', 'Cardiology', 'Neurology', 'Trauma'],
            'beds': 500,
            'lat': 13.0632,
            'lng': 80.2618
        },
        {
            'name': 'Government General Hospital',
            'address': 'Poonamallee High Rd, Park Town, Chennai, Tamil Nadu',
            'phone': '044-2530 5000',
            'rating': 4.2,
            'emergency': True,
            'specialties': ['Emergency Medicine', 'Surgery', 'Pediatrics', 'Orthopedics'],
            'beds': 1200,
            'lat': 13.0827,
            'lng': 80.2707
        },
        {
            'name': 'Kauvery Hospital',
            'address': '199, Luz Church Road, Mylapore, Chennai, Tamil Nadu',
            'phone': '044-4000 6000',
            'rating': 4.5,
            'emergency': True,
            'specialties': ['Cardiology', 'General Medicine', 'Orthopedics'],
            'beds': 300,
            'lat': 13.0337,
            'lng': 80.2549
        },
        {
            'name': 'MIOT International',
            'address': '4/112, Mount Poonamallee Road, Manapakkam, Chennai, Tamil Nadu',
            'phone': '044-4200 2288',
            'rating': 4.6,
            'emergency': True,
            'specialties': ['Emergency Medicine', 'Cardiology', 'Orthopedics'],
            'beds': 1000,
            'lat': 13.0107,
            'lng': 80.1802
        },
        {
            'name': 'Fortis Malar Hospital',
            'address': '52, 1st Main Road, Gandhi Nagar, Adyar, Chennai, Tamil Nadu',
            'phone': '044-4289 2222',
            'rating': 4.3,
            'emergency': True,
            'specialties': ['Emergency Medicine', 'Cardiology', 'Neurology'],
            'beds': 180,
            'lat': 13.0067,
            'lng': 80.2570
        }
    ]
    return tamil_nadu_hospitals
