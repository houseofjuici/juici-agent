import os
import streamlit as st
from dotenv import load_dotenv
from praisonaiagents import Agent
import sys
import yaml
import json
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Agents Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .agent-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 10px 0;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .agent-message {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

def load_agent_config(agent_name):
    """Load agent configuration and prompt."""
    config_path = Path(f"{agent_name}/agent_config.json")
    prompt_path = Path(f"{agent_name}/prompt.yaml")
    
    with open(config_path) as f:
        config = json.load(f)
    with open(prompt_path) as f:
        prompt = yaml.safe_load(f)['instructions']
    
    return config, prompt

def initialize_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = None

def display_quickstart():
    """Display quickstart guide."""
    st.markdown("""
    ## 🚀 Quick Start Guide
    
    Welcome to the AI Agents Hub! Here's how to get started:
    
    1. **Choose an Agent**
       - Select an agent from the sidebar based on your needs
       - Each agent has specific capabilities listed below
    
    2. **Start Chatting**
       - Type your question or request in the chat box
       - Be specific about what you need help with
    
    3. **Available Agents**:
       - 🏋️ **FitCoachAI**: Personal fitness and nutrition planning
       - ✍️ **BlogSmith**: Professional content creation
       - 📊 **FunnelBot**: Marketing funnel optimization
       - 📝 **ContractCopilot**: Legal document assistance
    
    4. **Tips**:
       - Start with simple, clear requests
       - Provide relevant details when asked
       - Follow the agent's guidance for best results
    """)

def display_agent_info(agent_name, config):
    """Display agent information."""
    st.markdown(f"""
    ### {config['name']} 
    **{config['description']}**
    
    **Capabilities**:
    """)
    for tool in config['tools']:
        st.markdown(f"- {tool.replace('_', ' ').title()}")

def chat_interface(agent_name):
    """Create chat interface for the selected agent."""
    if st.session_state.current_agent != agent_name:
        st.session_state.messages = []
        st.session_state.current_agent = agent_name
        
    config, prompt = load_agent_config(agent_name)
    agent = Agent(instructions=prompt)
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input(f"Ask {config['name']} something..."):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get and display agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = agent.start(prompt)
                st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    # Initialize session state
    initialize_session_state()
    
    # Sidebar for agent selection
    with st.sidebar:
        st.title("🤖 AI Agents Hub")
        selected_agent = st.radio(
            "Choose an Agent:",
            ["QuickStart", "FitCoachAI", "BlogSmith", "FunnelBot", "ContractCopilot"]
        )
    
    # Main content area
    if selected_agent == "QuickStart":
        display_quickstart()
    else:
        config, _ = load_agent_config(selected_agent)
        display_agent_info(selected_agent, config)
        chat_interface(selected_agent)

if __name__ == "__main__":
    main() 