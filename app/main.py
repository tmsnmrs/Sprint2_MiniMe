import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="MiniMe - Marketing Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("🎯 MiniMe - Your Marketing Assistant")
    st.markdown("""
    Welcome to MiniMe! I'm here to help you with your marketing tasks while teaching you 
    the fundamentals of marketing along the way.
    """)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Brand Analysis", "Value Proposition", "Target Audience", "Creative Concepts"]
    )
    
    # Main content area
    if page == "Home":
        st.header("How can I help you today?")
        st.markdown("""
        Select a task from the sidebar to get started:
        
        - **Brand Analysis**: Understand your brand's unique position in the market
        - **Value Proposition**: Craft compelling value propositions for your products
        - **Target Audience**: Identify and understand your ideal customers
        - **Creative Concepts**: Generate creative ideas for your marketing campaigns
        """)
    
    elif page == "Brand Analysis":
        st.header("Brand Analysis")
        st.write("This feature is coming soon!")
    
    elif page == "Value Proposition":
        st.header("Value Proposition")
        st.write("This feature is coming soon!")
    
    elif page == "Target Audience":
        st.header("Target Audience")
        st.write("This feature is coming soon!")
    
    elif page == "Creative Concepts":
        st.header("Creative Concepts")
        st.write("This feature is coming soon!")

if __name__ == "__main__":
    main() 