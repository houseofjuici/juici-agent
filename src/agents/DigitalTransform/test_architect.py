import pytest
import os
from dotenv import load_dotenv
from run_architect import design_solution, load_config, load_prompt

@pytest.fixture(autouse=True)
def setup_env():
    """Setup environment variables for tests."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set. Skipping tests.")

def test_config_loading():
    """Test that the agent configuration can be loaded correctly."""
    config = load_config('Architect')
    assert config is not None
    assert config['name'] == 'Architect'
    assert config['model'] == 'gpt-4-turbo-preview'
    assert isinstance(config['temperature'], float)
    assert isinstance(config['max_tokens'], int)
    assert isinstance(config['tools'], list)

def test_prompt_loading():
    """Test that the agent prompt can be loaded correctly."""
    prompt = load_prompt('Architect')
    assert prompt is not None
    assert isinstance(prompt, str)
    assert "You are Architect" in prompt
    assert "Output format:" in prompt

def test_solution_design():
    """Test the solution design functionality."""
    test_analysis = """
    Current State Analysis:
    - Manual processes
    - Legacy systems
    - Data silos
    
    Gap Assessment:
    - Need for automation
    - Integration required
    - Security updates needed
    """
    
    test_requirements = {
        'scale': 'Growth from 100 to 500 users in 12 months',
        'budget': '$500,000',
        'timeline': '6 months',
        'tech_preferences': 'Cloud-native, microservices',
        'security_requirements': 'SOC2 compliance required'
    }
    
    solution = design_solution(test_analysis, test_requirements)
    assert solution is not None
    assert len(solution) > 0
    
    # Check for required sections in output
    assert any(term in solution.lower() for term in [
        'solution architecture',
        'technology stack',
        'implementation roadmap',
        'risk assessment'
    ])

def test_error_handling():
    """Test error handling for invalid input."""
    invalid_requirements = {
        'scale': '',  # Empty scale
        'budget': 'invalid',  # Invalid budget
        'timeline': None,  # Missing timeline
        'tech_preferences': '',
        'security_requirements': ''
    }
    
    solution = design_solution("Test analysis", invalid_requirements)
    assert "Error" in solution

def test_comprehensive_design():
    """Test comprehensive solution design with detailed input."""
    detailed_analysis = """
    Current State Analysis:
    - Monolithic legacy application
    - Manual deployment process
    - On-premise infrastructure
    - Basic authentication
    
    Gap Assessment:
    - Need cloud migration
    - CI/CD pipeline required
    - Enhanced security needed
    - Scalability issues
    """
    
    detailed_requirements = {
        'scale': 'Expected 10x growth in 24 months',
        'budget': '$1.5M',
        'timeline': '12 months',
        'tech_preferences': 'AWS, Kubernetes, Docker, Microservices',
        'security_requirements': 'SOC2, GDPR, encryption at rest and in transit'
    }
    
    solution = design_solution(detailed_analysis, detailed_requirements)
    assert solution is not None
    assert len(solution) > 0
    
    # Check for detailed technical elements
    assert any(term in solution.lower() for term in [
        'cloud',
        'container',
        'microservice',
        'security',
        'scalability'
    ]) 