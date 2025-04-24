import streamlit as st
from app.backend import ChatManager
from datetime import datetime

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_task" not in st.session_state:
    st.session_state.current_task = None
if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager()

def handle_task_click(task_id: str, task_title: str):
    """Handle task selection and update session state"""
    # Update the current task in both session state and chat manager
    st.session_state.current_task = task_id
    st.session_state.chat_manager.set_current_task(task_id)
    
    # Get response from chat manager
    response = st.session_state.chat_manager.get_response("", task_id)
    
    # Update session state with the response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.content,
        "message_id": response.message_id,
        "timestamp": response.timestamp,
        "task_id": response.task_id
    })

# Page config
st.set_page_config(
    page_title="MiniMe",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #0E1117;
            padding-left: 25px;  /* Add consistent left padding */
        }
        .intro-section {
            padding: 1rem 0 2rem 0;
            margin: 0.5rem 2rem 3rem 0;  /* Adjusted margins */
        }
        .main-content {
            padding-top: 25px;  /* Space from intro section */
        }
        .section-title {
            font-size: 2.5rem;
            color: #FAFAFA;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        .main-description {
            color: #C6CCD7;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        .section-description {
            color: #C6CCD7;
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }
        /* Button styling to look like a card */
        div[data-testid="stButton"] {
            margin: 0.5rem 0;
            height: 180px !important;  /* Fixed height for container */
        }
        div[data-testid="stButton"] > button {
            width: 100% !important;
            height: 180px !important;  /* Fixed height for button */
            background-color: #1A1C23 !important;
            border: 2px solid transparent !important;
            border-radius: 0.5rem !important;
            padding: 1.5rem !important;
            transition: all 0.3s ease !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: flex-start !important;
            text-align: left !important;
            white-space: normal !important;
            line-height: 1.5 !important;
            box-sizing: border-box !important;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #262730 !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        div[data-testid="stButton"] > button.selected {
            border-color: #00CC66 !important;
            background-color: #1E2128 !important;
            box-shadow: 0 0 0 2px #00CC66, 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        }
        /* Text styling within buttons */
        div[data-testid="stButton"] button strong {
            display: block !important;
            color: #FAFAFA !important;
            font-size: 1.1rem !important;
            margin-bottom: 0.75rem !important;
            font-weight: 500 !important;
            width: 100% !important;
        }
        div[data-testid="stButton"] button p {
            color: #C6CCD7 !important;
            font-size: 0.9rem !important;
            margin: 0 !important;
            line-height: 1.4 !important;
            flex-grow: 1 !important;
        }
        /* Column layout adjustments */
        [data-testid="column"] {
            width: calc(33.33% - 1rem) !important;
            padding: 0 0.5rem !important;
        }
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        /* Remove default padding */
        .block-container {
            padding: 0 !important;
        }
        [data-testid="stAppViewContainer"] {
            padding: 0 !important;
        }
        [data-testid="stVerticalBlock"] {
            padding: 0 !important;
            gap: 0 !important;
        }
        [data-testid="stHorizontalBlock"] {
            padding: 0 !important;
            gap: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Welcome Section
st.markdown('<div class="intro-section">', unsafe_allow_html=True)
st.markdown('<h1 class="section-title">MiniMe</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="main-description">Turn your knowledge into digital product businesses that sell themselves. '
    'Let me help you build your brand, understand your audience, and create compelling content.</p>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Create two main columns for the split layout
tasks_col, divider_col, chat_col = st.columns([1, 0.05, 1])

# Left column - Marketing Tasks
with tasks_col:
    # Debug information
    st.markdown(f"<div style='color: #666; font-size: 0.8rem;'>Debug: Current task = {st.session_state.current_task}</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">Marketing Tasks</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-description">Select a marketing task below to get started. Each task includes step-by-step guidance '
        'and educational insights to help you learn as you go.</p>',
        unsafe_allow_html=True
    )

    # Create three columns for tasks
    col1, col2, col3 = st.columns(3)

    # Task definitions
    tasks = [
        ("analyze-product", "Analyze my product", "Understand your product's unique features and market position.", col1),
        ("identify-audience", "Identify target audiences", "Define and understand your ideal customer segments.", col2),
        ("identify-benefits", "Identify product benefits", "Discover key advantages your product offers to customers.", col3),
        ("value-propositions", "Phrase value propositions", "Create compelling statements that showcase your value.", col1),
        ("position-product", "Position the product", "Define your product's place in the market landscape.", col2),
        ("product-message", "Pick a product message", "Choose the core message that resonates with your audience.", col3),
        ("select-archetype", "Select an archetype", "Choose a brand personality that connects with customers.", col1),
        ("creative-equations", "Craft creative equations", "Generate unique marketing ideas and content strategies.", col2),
        ("copywrite-content", "Copywrite content for me", "Create engaging copy for your marketing materials.", col3)
    ]

    # Render task cards
    for task_id, title, description, col in tasks:
        with col:
            if st.button(
                f"**{title}**\n\n{description}",
                key=f"task_{task_id}",
                use_container_width=True,
                help=f"Click to start working on: {title}"
            ):
                handle_task_click(task_id, title)
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Vertical Divider
with divider_col:
    st.markdown('<div class="divider-container"><div class="vertical-divider"></div></div>', unsafe_allow_html=True)

# Right column - Chat
with chat_col:
    st.markdown('<h1 class="section-title">Chat with MiniMe</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-description">Ask questions, get marketing advice, or start working on specific tasks. '
        "I'll guide you through the process and explain marketing concepts along the way.</p>",
        unsafe_allow_html=True
    )

    # Chat container with scroll
    chat_container = st.container()
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                # Display message metadata in small text if in debug mode
                if st.session_state.get("debug_mode", False):
                    st.markdown(
                        f"<div style='color: #666; font-size: 0.7rem;'>"
                        f"ID: {message.get('message_id', 'N/A')} | "
                        f"Task: {message.get('task_id', 'N/A')} | "
                        f"Time: {message.get('timestamp', 'N/A')}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

        # Add initial message if no messages exist
        if not st.session_state.messages:
            with st.chat_message("assistant"):
                welcome_message = "Hi! I'm MiniMe, your marketing assistant. How can I help you today?"
                st.markdown(welcome_message)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": welcome_message,
                    "message_id": f"msg_{int(datetime.now().timestamp())}",
                    "timestamp": datetime.now(),
                    "task_id": None
                })

        # Chat input
        prompt = st.chat_input(
            "Message MiniMe",
            key="chat_input",
        )

        if prompt:
            # Add user message to chat history
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "message_id": f"msg_{int(datetime.now().timestamp())}",
                "timestamp": datetime.now(),
                "task_id": st.session_state.current_task
            })
            
            # Get response from chat manager
            response = st.session_state.chat_manager.get_response(prompt)
            
            # Add assistant's response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.content,
                "message_id": response.message_id,
                "timestamp": response.timestamp,
                "task_id": response.task_id
            })
            st.rerun()

# Footer
st.markdown(
    '<div style="text-align: center; color: #C6CCD7; padding: 2rem 0;">Turing College | AI Engineering | Sprint 2 | Tomas Nemura ©</div>',
    unsafe_allow_html=True) 