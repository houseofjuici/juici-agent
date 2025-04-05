import pytest
import os
from dotenv import load_dotenv
from run_designer import create_design, load_config, load_prompt

@pytest.fixture(autouse=True)
def setup_env():
    """Setup environment variables for tests."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set. Skipping tests.")

def test_config_loading():
    """Test that the agent configuration can be loaded correctly."""
    config = load_config('Designer')
    assert config is not None
    assert config['name'] == 'Designer'
    assert config['model'] == 'gpt-4-turbo-preview'
    assert isinstance(config['temperature'], float)
    assert isinstance(config['max_tokens'], int)
    assert isinstance(config['tools'], list)

def test_prompt_loading():
    """Test that the agent prompt can be loaded correctly."""
    prompt = load_prompt('Designer')
    assert prompt is not None
    assert isinstance(prompt, str)
    assert "You are Designer" in prompt
    assert "Output format:" in prompt

def test_design_creation():
    """Test the design creation functionality."""
    test_solution = """
    Solution Architecture:
    - Microservices architecture
    - React frontend
    - REST APIs
    - Cloud hosting
    
    Technology Stack:
    - React/Next.js
    - Node.js microservices
    - PostgreSQL database
    - AWS infrastructure
    """
    
    test_requirements = {
        'platform': 'Web, Mobile responsive',
        'user_type': 'Business professionals',
        'brand_guidelines': 'Modern, professional, blue/gray palette',
        'accessibility': 'WCAG 2.1 AA',
        'key_features': 'Dashboard, Analytics, User Management'
    }
    
    design = create_design(test_solution, test_requirements)
    assert design is not None
    assert len(design) > 0
    
    # Check for required sections in output
    assert any(term in design.lower() for term in [
        'design system',
        'user flows',
        'interface designs',
        'accessibility plan'
    ])

def test_error_handling():
    """Test error handling for invalid input."""
    invalid_requirements = {
        'platform': '',  # Empty platform
        'user_type': 'invalid',  # Invalid user type
        'brand_guidelines': None,  # Missing guidelines
        'accessibility': '',
        'key_features': ''
    }
    
    design = create_design("Test solution", invalid_requirements)
    assert "Error" in design

def test_comprehensive_design():
    """Test comprehensive design creation with detailed input."""
    detailed_solution = """
    Solution Architecture:
    - Microservices-based SaaS platform
    - React/Next.js frontend
    - GraphQL API gateway
    - Event-driven architecture
    - Multi-tenant database
    
    Technology Stack:
    - React 18 with TypeScript
    - Node.js/Express microservices
    - Apollo GraphQL
    - PostgreSQL with multi-tenancy
    - Redis caching
    - AWS cloud infrastructure
    """
    
    detailed_requirements = {
        'platform': 'Web (desktop-first), iOS and Android apps',
        'user_type': 'Enterprise users, IT administrators',
        'brand_guidelines': 'Enterprise-grade, Material Design 3, dark mode support',
        'accessibility': 'WCAG 2.1 AAA compliance required',
        'key_features': 'SSO, Role-based access, Analytics dashboard, Real-time collaboration'
    }
    
    design = create_design(detailed_solution, detailed_requirements)
    assert design is not None
    assert len(design) > 0
    
    # Check for detailed design elements
    assert any(term in design.lower() for term in [
        'material design',
        'responsive',
        'component library',
        'design tokens',
        'accessibility'
    ]) 