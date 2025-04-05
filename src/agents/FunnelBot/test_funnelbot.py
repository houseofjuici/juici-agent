import os
import pytest
from dotenv import load_dotenv
from praisonaiagents import Agent

@pytest.fixture(autouse=True)
def setup_env():
    """Load environment variables and check for API key."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        pytest.skip("OPENAI_API_KEY not set or invalid")

@pytest.fixture
def agent():
    """Create a test agent instance."""
    return Agent(instructions="You are a marketing copywriter.")

def test_landing_page_copy(agent):
    """Test landing page copy generation."""
    response = agent.start("Create landing page copy for a fitness app targeting busy professionals")
    assert response is not None
    assert len(response) > 0
    assert "headline" in response.lower()
    assert "features" in response.lower()

def test_email_sequence(agent):
    """Test email sequence generation."""
    response = agent.start("Create a 3-email sequence for a fitness app")
    assert response is not None
    assert len(response) > 0
    assert "email 1" in response.lower()
    assert "email 2" in response.lower()
    assert "email 3" in response.lower()

def test_sales_page(agent):
    """Test sales page copy generation."""
    response = agent.start("Create sales page copy for a fitness app priced at $29.99/month")
    assert response is not None
    assert len(response) > 0
    assert "$29.99" in response.lower()
    assert "offer" in response.lower()

def test_persuasive_elements(agent):
    """Test inclusion of persuasive elements."""
    response = agent.start("Create landing page copy for a fitness app")
    assert response is not None
    assert any(element in response.lower() for element in [
        "features",
        "testimonials",
        "call to action",
        "offer"
    ])

def test_brand_voice(agent):
    """Test brand voice consistency."""
    response = agent.start("Create landing page copy for a fitness app with a professional tone")
    assert response is not None
    assert len(response) > 0
    # Check for professional language
    assert any(word in response.lower() for word in [
        "professional",
        "effective",
        "efficient",
        "results"
    ]) 