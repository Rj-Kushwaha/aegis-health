def analyze_symptoms(symptoms_text, user_type='patient'):
    """Enhanced symptom analysis with user type consideration"""
    symptoms_lower = symptoms_text.lower()
    
    # Emergency conditions
    emergency_keywords = [
        'chest pain', 'difficulty breathing', 'severe headache', 'stroke', 'heart attack', 
        'unconscious', 'severe bleeding', 'poisoning', 'overdose', 'seizure',
        'anaphylaxis', 'severe allergic reaction', 'choking', 'cardiac arrest'
    ]
    
    # High-risk conditions
    high_risk_keywords = [
        'fever over 103', 'persistent vomiting', 'severe abdominal pain', 
        'difficulty swallowing', 'severe dehydration', 'diabetic emergency',
        'severe burns', 'head trauma', 'loss of consciousness'
    ]
    
    # Medium risk conditions
    medium_risk_keywords = [
        'moderate fever', 'persistent cough', 'shortness of breath', 'severe pain',
        'blood in stool', 'blood in urine', 'severe diarrhea', 'fainting'
    ]
    
    # Common conditions
    cold_keywords = ['runny nose', 'sneezing', 'mild fever', 'cough', 'sore throat']
    digestive_keywords = ['nausea', 'stomach pain', 'diarrhea', 'indigestion', 'heartburn']
    musculoskeletal_keywords = ['back pain', 'joint pain', 'muscle ache', 'stiffness']
    mental_health_keywords = ['anxiety', 'depression', 'stress', 'panic attack', 'insomnia']
    
    diagnosis = "General consultation needed"
    severity = "Low"
    recommendations = []
    professional_note = ""
    
    # Add professional context based on user type
    if user_type == 'medical_student':
        professional_note = "\n📚 Educational Context: Consider differential diagnoses and evidence-based treatment protocols."
    elif user_type == 'healthcare_professional':
        professional_note = "\n👩‍⚕️ Professional Assessment: Review clinical guidelines and consider patient comorbidities."
    
    # Check for emergency conditions
    if any(keyword in symptoms_lower for keyword in emergency_keywords):
        diagnosis = "⚠️ EMERGENCY CONDITION DETECTED"
        severity = "CRITICAL"
        recommendations = [
            "🚨 CALL 911 IMMEDIATELY",
            "Go to the nearest emergency room",
            "Do not drive yourself - call ambulance",
            "Have someone stay with you",
            "Prepare list of current medications",
            "Stay calm and follow emergency operator instructions"
        ]
    
    # Check for high-risk conditions
    elif any(keyword in symptoms_lower for keyword in high_risk_keywords):
        diagnosis = "High-risk condition - Urgent medical attention needed"
        severity = "High"
        recommendations = [
            "Seek immediate medical attention within 2-4 hours",
            "Visit urgent care or emergency room",
            "Contact your primary care physician immediately",
            "Monitor symptoms closely and call 911 if worsening",
            "Avoid eating or drinking until medical evaluation",
            "Have someone available to drive you to medical facility"
        ]
    
    # Check for medium-risk conditions
    elif any(keyword in symptoms_lower for keyword in medium_risk_keywords):
        diagnosis = "Moderate concern - Medical evaluation recommended within 24 hours"
        severity = "Medium"
        recommendations = [
            "Schedule appointment with healthcare provider within 24 hours",
            "Monitor symptoms and seek urgent care if worsening",
            "Take temperature regularly and keep symptom log",
            "Stay hydrated and rest",
            "Avoid strenuous activities"
        ]
    
    # Check for common conditions
    elif any(keyword in symptoms_lower for keyword in cold_keywords):
        diagnosis = "Possible common cold or upper respiratory infection"
        severity = "Low"
        recommendations = [
            "Rest and stay well hydrated with warm fluids",
            "Use over-the-counter medications as directed",
            "Gargle with warm salt water for sore throat",
            "Use humidifier to ease congestion",
            "See a doctor if symptoms worsen or persist beyond 7-10 days",
            "Isolate to prevent spreading to others"
        ]
    
    elif any(keyword in symptoms_lower for keyword in digestive_keywords):
        diagnosis = "Possible digestive issue or gastroenteritis"
        severity = "Low"
        recommendations = [
            "Stay hydrated with clear fluids and electrolyte solutions",
            "Follow BRAT diet (bananas, rice, applesauce, toast)",
            "Avoid dairy, caffeine, alcohol, and fatty foods",
            "Rest and allow digestive system to recover",
            "See a doctor if symptoms persist beyond 48 hours",
            "Seek immediate care if signs of severe dehydration appear"
        ]
    
    elif any(keyword in symptoms_lower for keyword in musculoskeletal_keywords):
        diagnosis = "Possible musculoskeletal condition or injury"
        severity = "Low"
        recommendations = [
            "Apply RICE protocol: Rest, Ice, Compression, Elevation",
            "Use over-the-counter anti-inflammatory medications as directed",
            "Gentle stretching and movement as tolerated",
            "Heat therapy after initial 48 hours if helpful",
            "See a doctor if pain is severe or persists beyond a week",
            "Physical therapy may be beneficial for chronic issues"
        ]
    
    elif any(keyword in symptoms_lower for keyword in mental_health_keywords):
        diagnosis = "Possible mental health concern"
        severity = "Medium"
        recommendations = [
            "Consider speaking with a mental health professional",
            "Practice stress reduction techniques (meditation, deep breathing)",
            "Maintain regular sleep schedule and healthy diet",
            "Stay connected with supportive friends and family",
            "Contact crisis helpline if having thoughts of self-harm: 988",
            "Regular exercise can help improve mood and reduce anxiety"
        ]
    
    return diagnosis, severity, recommendations, professional_note


def medical_chatbot_response(question, user_type='patient'):
    """Enhanced medical chatbot with user type consideration"""
    question_lower = question.lower()
    
    response_prefix = ""
    if user_type == 'medical_student':
        response_prefix = "📚 **Educational Response:** "
    elif user_type == 'healthcare_professional':
        response_prefix = "👩‍⚕️ **Professional Insight:** "
    
    if any(word in question_lower for word in ['fever', 'temperature']):
        return f"""{response_prefix}🌡️ **About Fever:**
        
A fever is generally considered a temperature above 100.4°F (38°C). Here's comprehensive information:

**Pathophysiology:** Fever is the body's natural immune response to infection or inflammation, mediated by pyrogens affecting the hypothalamic thermostat.

**Assessment Guidelines:**
- Low-grade: 100.4-102°F (38-38.9°C)
- Moderate: 102-104°F (38.9-40°C)  
- High-grade: >104°F (>40°C)

**When to seek immediate care:**
- Temperature above 103°F (39.4°C)
- Fever lasting more than 3 days
- Accompanied by severe symptoms (difficulty breathing, chest pain, severe headache)
- Febrile seizures (especially in children)

**Evidence-based management:**
- Maintain hydration (increase fluid intake by 15-20%)
- Antipyretics: Acetaminophen 650-1000mg q6h or Ibuprofen 400-600mg q6h
- Cool compresses to forehead and wrists
- Rest in cool environment

**Red flags requiring immediate evaluation:**
- Petechial rash, nuchal rigidity, altered mental status, severe dehydration"""
    
    elif any(word in question_lower for word in ['headache', 'head pain']):
        return f"""{response_prefix}🤕 **About Headaches:**
        
**Classification (IHS Criteria):**
- Primary: Tension-type (90%), Migraine, Cluster
- Secondary: Due to underlying pathology

**Differential Diagnosis:**
- Tension headaches: Bilateral, pressing/tightening quality
- Migraines: Unilateral, pulsating, with nausea/photophobia
- Cluster: Severe unilateral periorbital pain
- Secondary: SAH, meningitis, temporal arteritis

**Red flag symptoms (require immediate evaluation):**
- Sudden onset "thunderclap" headache
- Headache with fever, neck stiffness, altered consciousness
- New headache in patient >50 years
- Progressive worsening pattern
- Headache following head trauma

**Management approach:**
- Acute: NSAIDs, triptans (for migraines), avoid medication overuse
- Prophylaxis: Consider for >4 headache days/month
- Non-pharmacological: Sleep hygiene, stress management, trigger avoidance"""
    
    elif any(word in question_lower for word in ['chest pain', 'cardiac', 'heart']):
        return f"""{response_prefix}❤️ **About Chest Pain:**
        
**⚠️ CRITICAL: Chest pain requires immediate professional evaluation**

**High-risk features (ACS indicators):**
- Crushing, pressure-like substernal pain
- Radiation to left arm, jaw, or back
- Associated with diaphoresis, nausea, dyspnea
- Worse with exertion, better with rest

**Differential diagnosis:**
- Cardiac: ACS, pericarditis, aortic dissection
- Pulmonary: PE, pneumothorax, pneumonia
- GI: GERD, esophageal spasm
- Musculoskeletal: Costochondritis, muscle strain

**Immediate actions:**
1. Call 911 if suspected cardiac etiology
2. Administer aspirin 325mg (if no contraindications)
3. Position patient comfortably
4. Monitor vital signs
5. Prepare for potential CPR

**Never ignore chest pain - early intervention saves lives**"""
    
    elif any(word in question_lower for word in ['mental health', 'depression', 'anxiety']):
        return f"""{response_prefix}🧠 **About Mental Health:**
        
**Screening tools:**
- PHQ-9 for depression screening
- GAD-7 for anxiety assessment
- Suicide risk assessment (PHQ-9 item 9)

**Evidence-based treatments:**
- Depression: CBT, IPT, SSRIs, SNRIs
- Anxiety: CBT, exposure therapy, SSRIs, benzodiazepines (short-term)
- Combined approach often most effective

**Crisis resources:**
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741
- Emergency services: 911

**Professional referral indicators:**
- Persistent symptoms >2 weeks
- Functional impairment
- Suicidal ideation
- Substance abuse comorbidity

**Lifestyle interventions:**
- Regular exercise (30 min, 5x/week)
- Sleep hygiene (7-9 hours)
- Mindfulness/meditation practices
- Social connection and support"""
    
    else:
        return f"""{response_prefix}🩺 **Comprehensive Health Information:**
        
I provide evidence-based medical information tailored to your professional level:

**For Medical Students:** Focus on pathophysiology, differential diagnosis, and learning objectives
**For Healthcare Professionals:** Clinical pearls, recent guidelines, and practice management
**For Patients:** Clear, actionable health guidance and when to seek care

**Available topics:**
- Symptom assessment and triage
- Medication information and interactions  
- Diagnostic criteria and clinical guidelines
- Emergency recognition and management
- Preventive health measures
- Mental health screening and support

**Quality assurance:**
- Information based on current medical literature
- Guidelines from major medical organizations
- Regular updates with latest evidence

Please ask about specific symptoms, conditions, or health topics for detailed, personalized responses."""
