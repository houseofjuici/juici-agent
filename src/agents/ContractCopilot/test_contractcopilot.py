import pytest
from praisonaiagents import Agent
import json
import yaml
import os
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def setup_env():
    """Setup environment variables for tests."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        pytest.skip("OPENAI_API_KEY not set. Skipping tests.")

def test_agent_initialization():
    """Test that the agent can be initialized with correct configuration."""
    # Load test configuration
    with open('agent_config.json', 'r') as f:
        config = json.load(f)
    
    with open('prompt.yaml', 'r') as f:
        instructions = yaml.safe_load(f)['instructions']
    
    # Initialize agent
    agent = Agent(instructions=instructions)
    
    assert agent is not None
    assert agent.instructions == instructions

def test_agent_response():
    """Test that the agent can generate a response."""
    # Load test configuration
    with open('agent_config.json', 'r') as f:
        config = json.load(f)
    
    with open('prompt.yaml', 'r') as f:
        instructions = yaml.safe_load(f)['instructions']
    
    # Initialize agent
    agent = Agent(instructions=instructions)
    
    # Test with a simple contract clause
    response = agent.start("Generate a non-disclosure agreement clause")
    
    assert response is not None
    assert len(response) > 0
    assert "clause" in response.lower() or "agreement" in response.lower() 