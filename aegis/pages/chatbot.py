import json
import streamlit as st
from datetime import datetime

from aegis.analysis import medical_chatbot_response


def render_chatbot():
    st.markdown("## 💬 AI Medical Assistant")
    st.markdown("Ask questions and get personalized medical information based on your profile.")

    # Voice controls section
    col1, col2 = st.columns([3, 1])

    with col2:
        st.markdown("""
        <div class="voice-controls">
            <h4 style="color: white; margin-bottom: 1rem;">🎤 Voice Assistant</h4>
        </div>
        """, unsafe_allow_html=True)

        voice_enabled = st.checkbox("🎤 Enable Voice Input", value=st.session_state.voice_enabled)
        st.session_state.voice_enabled = voice_enabled

        if voice_enabled:
            st.info("🎤 Voice input would be enabled here using Web Speech API in a full deployment")
            if st.button("🎙️ Start Recording", use_container_width=True):
                st.success("Recording... (simulated)")

        text_to_speech = st.checkbox("🔊 Text-to-Speech Response")
        if text_to_speech:
            st.info("🔊 AI responses would be read aloud using browser's speech synthesis")

    with col1:
        # Chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        # Display chat history
        chat_container = st.container()

        with chat_container:
            for i, (question, answer) in enumerate(st.session_state.chat_history):
                # User message
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 1rem; border-radius: 15px 15px 5px 15px; 
                            margin: 0.5rem 0; margin-left: 20%;">
                    <strong>You:</strong> {question}
                </div>
                """, unsafe_allow_html=True)

                # AI response
                st.markdown(f"""
                <div style="background: white; color: #2d3436; padding: 1rem; 
                            border-radius: 15px 15px 15px 5px; margin: 0.5rem 0; 
                            margin-right: 20%; box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
                            border-left: 4px solid #00b894;">
                    <strong>🩺 MediBot:</strong><br>{answer}
                </div>
                """, unsafe_allow_html=True)

        # New question input
        with st.form("chat_form", clear_on_submit=True):
            col_input, col_submit = st.columns([4, 1])

            with col_input:
                question = st.text_input(
                    "Ask your health question:",
                    placeholder="e.g., What are the symptoms of diabetes? How do I manage high blood pressure?",
                    label_visibility="collapsed"
                )

            with col_submit:
                ask_button = st.form_submit_button("💬 Ask", use_container_width=True)

            # Quick question buttons
            st.markdown("**Quick Questions:**")
            quick_questions = [
                "What should I do for a fever?",
                "How do I treat a headache?", 
                "What are signs of dehydration?",
                "When should I see a doctor?"
            ]

            cols = st.columns(len(quick_questions))
            for i, quick_q in enumerate(quick_questions):
                with cols[i]:
                    if st.form_submit_button(quick_q.split('?')[0] + '?', use_container_width=True):
                        question = quick_q
                        ask_button = True

            if ask_button and question:
                with st.spinner("🤔 Thinking..."):
                    answer = medical_chatbot_response(question, st.session_state.user.get('user_type', 'patient'))
                    st.session_state.chat_history.append((question, answer))

                    # Simulate text-to-speech
                    if text_to_speech:
                        st.success("🔊 Response would be read aloud")

                    st.rerun()

        # Chat controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

        with col2:
            if st.session_state.chat_history:
                chat_export = json.dumps({
                    'user': st.session_state.user['username'],
                    'chat_history': st.session_state.chat_history,
                    'timestamp': datetime.now().isoformat()
                }, indent=2)

                st.download_button(
                    label="📥 Export Chat",
                    data=chat_export,
                    file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
