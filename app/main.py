import streamlit as st

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_task" not in st.session_state:
    st.session_state.current_task = None

def handle_task_click(task_id: str, task_title: str):
    """Handle task selection and update session state"""
    st.session_state.current_task = task_id
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Selected task: {task_title}. How can I help you with this?"
    })
    st.rerun()

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
        }
        .intro-section {
            padding: 1rem 0 2rem 0;  /* Reduced top padding */
            margin: 0.5rem 3rem 2rem 3rem;  /* Adjusted margins */
        }
        .main-content {
            margin-left: 3rem;  /* Match intro section margin */
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
        .task-card {
            background-color: #1A1C23;
            padding: 1.5rem;  /* Increased padding */
            border-radius: 0.5rem;
            height: 180px;  /* Increased height */
            margin: 1rem auto;  /* Increased vertical margin */
            width: 85%;
            transition: background-color 0.2s ease;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .task-card:hover {
            background-color: #262730;
        }
        .task-card h3 {
            color: #FAFAFA;
            font-size: 1.1rem;
            margin-bottom: 0.75rem;  /* Increased margin */
            font-weight: 500;
        }
        .task-card p {
            color: #C6CCD7;
            font-size: 0.9rem;
            margin: 0;
            line-height: 1.4;  /* Improved readability */
        }
        div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
            gap: 0rem;
        }
        .chat-container {
            height: calc(100vh - 400px);
            overflow-y: auto;
            padding-right: 1rem;
        }
        .tasks-container {
            height: calc(100vh - 400px);
            overflow-y: auto;
            padding-right: 1rem;
        }
        .vertical-divider {
            border-left: 1px solid #FFFFFF;
            height: 100%;
            margin: 0 20px;
            position: absolute;
            top: 0;
            bottom: 0;
        }
        .divider-container {
            position: relative;
            height: 100%;
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

# Welcome Section (Full Width)
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
            st.markdown(
                f"""
                <div class="task-card" onclick="window.parent.postMessage({{event: 'task_click', task_id: '{task_id}', task_title: '{title}'}}, '*')">
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # JavaScript to handle task clicks
    st.markdown("""
        <script>
            window.addEventListener('message', function(e) {
                if (e.data.event === 'task_click') {
                    window.parent.document.querySelector('button[data-testid="baseButton-secondary"]').click();
                }
            });
        </script>
    """, unsafe_allow_html=True)
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

        # Add initial message if no messages exist
        if not st.session_state.messages:
            with st.chat_message("assistant"):
                st.markdown("Hi! I'm MiniMe, your marketing assistant. How can I help you today?")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Hi! I'm MiniMe, your marketing assistant. How can I help you today?"
                })

        # Chat input
        prompt = st.chat_input(
            "Message MiniMe",
            key="chat_input",
        )

        if prompt:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # For now, just echo the message back
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"You said: {prompt}"
            })
            st.rerun()

# Footer
st.markdown(
    '<div style="text-align: center; color: #C6CCD7; padding: 2rem 0;">Turing College | AI Engineering | Sprint 2 | Tomas Nemura ©</div>',
    unsafe_allow_html=True) 