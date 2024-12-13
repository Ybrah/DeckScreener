import streamlit as st
from pdfminer.high_level import extract_text
from ai import get_pitch_insights, deck_direct_chat

# Set page configuration
st.set_page_config(
    page_title="Pitch Deck Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
    color: #4a4a4a;
}
.stTextInput > div > div > input {
    background-color: #f0f2f6;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
}
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    transition-duration: 0.4s;
    cursor: pointer;
}
.stButton > button:hover {
    background-color: #45a049;
}
</style>
""", unsafe_allow_html=True)

def insights_page():
    st.title("🔍 Startup Pitch Deck Insights Extractor")

    # File uploader
    uploaded_file = st.file_uploader("Upload Pitch Deck (PDF)", type=["pdf"])

    if uploaded_file is not None:
        # Extract text from PDF
        with st.spinner('Extracting insights...'):
            deck_content_txt = extract_text(uploaded_file)
            
            # Generate insights
            insights = get_pitch_insights(deck_content_txt)
            
            # Display insights
            st.subheader("Extracted Pitch Deck Insights")
            st.write(insights)

def deck_chat_page():
    st.title("💬 Pitch Deck Chat")

    # File uploader
    uploaded_file = st.file_uploader("Upload Pitch Deck (PDF)", type=["pdf"])

    if uploaded_file is not None:
        # Extract text from PDF
        deck_content_txt = extract_text(uploaded_file)
        
        # Initialize chat history
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about the deck"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                response = deck_direct_chat(deck_content_txt, prompt)
                st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

# Page selection
page = st.sidebar.radio("Select a Feature", ["Pitch Deck Insights", "Deck Chat"])

# Render the selected page
if page == "Pitch Deck Insights":
    insights_page()
else:
    deck_chat_page()