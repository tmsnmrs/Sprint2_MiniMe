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
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern dark theme
st.markdown("""
    <style>
        /* Global Styles */
        [data-testid="stAppViewContainer"] {
            background-color: #111111;
            padding: 1rem !important;
        }

        [data-testid="stHeader"] {
            display: none;
        }
        
        .main {
            padding: 0 !important;
        }

        section[data-testid="stSidebar"] {
            display: none;
        }
        
        .stMarkdown {
            color: #E6E6E6;
        }
        
        h1, h2, h3 {
            color: white !important;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }
        
        /* Section Styles */
        .content-section {
            background-color: #1A1A1A;
            padding: 2rem;
            border-radius: 8px;
            margin: 0 0 1rem 0;
        }
        
        .section-title {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: white;
        }
        
        .section-description {
            color: #B3B3B3;
            font-size: 1rem;
            line-height: 1.5;
            margin-bottom: 1rem;
        }
        
        /* Marketing Tasks Grid */
        .tasks-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-top: 1.5rem;
        }
        
        .task-item {
            background-color: #222222;
            padding: 1.5rem;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .task-item:hover {
            background-color: #2A2A2A;
        }
        
        .task-item h3 {
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        
        .task-item p {
            color: #B3B3B3;
            margin: 0;
            font-size: 0.9rem;
            line-height: 1.4;
        }
        
        /* Chat Section */
        .chat-area {
            background-color: #222222;
            border-radius: 6px;
            padding: 1rem;
            margin-top: 1rem;
        }
        
        .chat-message {
            padding: 0.8rem;
            margin: 0.5rem 0;
            border-radius: 4px;
        }
        
        .user-message {
            background-color: #2A2A2A;
        }
        
        .assistant-message {
            background-color: #1A1A1A;
        }

        /* Input field styling */
        .stTextInput input {
            background-color: #222222;
            border: 1px solid #333333;
            color: white;
            border-radius: 6px;
        }

        .stTextInput input:focus {
            border-color: #444444;
            box-shadow: none;
        }

        .stTextInput input::placeholder {
            color: #888888;
        }

        /* Copyright styling */
        .copyright {
            text-align: center;
            color: #666666;
            font-size: 0.8rem;
            padding: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    # Introduction Section
    st.markdown("""
    <div class="content-section">
        <h1>MiniMe</h1>
        <p class="section-description">
        Turn your knowledge into digital product businesses that sell themselves. 
        Let me help you build your brand, understand your audience, and create compelling content.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Marketing Tasks Section
    st.markdown("""
    <div class="content-section">
        <h2 class="section-title">Marketing Tasks</h2>
        <p class="section-description">
        Select a marketing task below to get started. Each task includes step-by-step guidance 
        and educational insights to help you learn as you go.
        </p>
        <div class="tasks-container">
            <div class="task-item">
                <h3>Analyze my product</h3>
                <p>Understand your product's unique features and market position.</p>
            </div>
            <div class="task-item">
                <h3>Identify target audiences</h3>
                <p>Define and understand your ideal customer segments.</p>
            </div>
            <div class="task-item">
                <h3>Identify product benefits</h3>
                <p>Discover key advantages your product offers to customers.</p>
            </div>
            <div class="task-item">
                <h3>Phrase value propositions</h3>
                <p>Create compelling statements that showcase your value.</p>
            </div>
            <div class="task-item">
                <h3>Position the product</h3>
                <p>Define your product's place in the market landscape.</p>
            </div>
            <div class="task-item">
                <h3>Pick a product message</h3>
                <p>Choose the core message that resonates with your audience.</p>
            </div>
            <div class="task-item">
                <h3>Select an archetype</h3>
                <p>Choose a brand personality that connects with customers.</p>
            </div>
            <div class="task-item">
                <h3>Craft creative equations</h3>
                <p>Generate unique marketing ideas and content strategies.</p>
            </div>
            <div class="task-item">
                <h3>Copywrite content for me</h3>
                <p>Create engaging copy for your marketing materials.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat Section
    st.markdown("""
    <div class="content-section">
        <h2 class="section-title">Chat with MiniMe</h2>
        <p class="section-description">
        Ask questions, get marketing advice, or start working on specific tasks. 
        I'll guide you through the process and explain marketing concepts along the way.
        </p>
        <div class="chat-area">
            <div class="chat-message assistant-message">
                Hi! I'm MiniMe, your marketing assistant. How can I help you today?
            </div>
    """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Chat message", placeholder="Type your message here...", label_visibility="collapsed")
    if user_input:
        st.markdown(f"""
            <div class="chat-message user-message">
                {user_input}
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Copyright
    st.markdown("""
    <div class="copyright">
        Turing College | AI Engineering | Sprint 2 | Tomas Nemura ©
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 