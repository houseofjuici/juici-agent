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
    agent = Agent(
        instructions=instructions,
        model=config['model'],
        temperature=config['temperature'],
        max_tokens=config['max_tokens']
    )
    
    assert agent is not None
    assert agent.instructions == instructions
    assert agent.model == config['model']

@pytest.mark.asyncio
async def test_agent_response():
    """Test that the agent can generate a response."""
    # Load test configuration
    with open('agent_config.json', 'r') as f:
        config = json.load(f)
    
    with open('prompt.yaml', 'r') as f:
        instructions = yaml.safe_load(f)['instructions']
    
    # Initialize agent
    agent = Agent(
        instructions=instructions,
        model=config['model'],
        temperature=config['temperature'],
        max_tokens=config['max_tokens']
    )
    
    # Test with a simple topic
    response = await agent.start("Write a short blog post about AI")
    
    assert response is not None
    assert len(response) > 0
    assert "Title" in response or "Introduction" in response 