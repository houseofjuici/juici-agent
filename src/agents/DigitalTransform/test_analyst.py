import pytest
import os
from dotenv import load_dotenv
from run_analyst import analyze_business, load_config, load_prompt

@pytest.fixture(autouse=True)
def setup_env():
    """Setup environment variables for tests."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set. Skipping tests.")

def test_config_loading():
    """Test that the agent configuration can be loaded correctly."""
    config = load_config('Analyst')
    assert config is not None
    assert config['name'] == 'Analyst'
    assert config['model'] == 'gpt-4-turbo-preview'
    assert isinstance(config['temperature'], float)
    assert isinstance(config['max_tokens'], int)
    assert isinstance(config['tools'], list)

def test_prompt_loading():
    """Test that the agent prompt can be loaded correctly."""
    prompt = load_prompt('Analyst')
    assert prompt is not None
    assert isinstance(prompt, str)
    assert "You are Analyst" in prompt
    assert "Output format:" in prompt

def test_business_analysis():
    """Test the business analysis functionality."""
    test_business = {
        'name': 'Test Company',
        'industry': 'Technology',
        'size': '50',
        'current_processes': 'Manual data entry, paper-based workflows',
        'pain_points': 'Inefficient processes, data silos',
        'goals': 'Automate workflows, improve data accessibility'
    }
    
    analysis = analyze_business(test_business)
    assert analysis is not None
    assert len(analysis) > 0
    
    # Check for required sections in output
    assert any(term in analysis.lower() for term in [
        'current state',
        'gap assessment',
        'opportunities',
        'recommendations'
    ])

def test_error_handling():
    """Test error handling for invalid input."""
    invalid_business = {
        'name': '',  # Empty name
        'industry': 'Technology',
        'size': 'invalid',  # Invalid size
        'current_processes': None,  # Missing processes
        'pain_points': '',
        'goals': ''
    }
    
    analysis = analyze_business(invalid_business)
    assert "Error" in analysis

def test_comprehensive_analysis():
    """Test comprehensive analysis with detailed input."""
    detailed_business = {
        'name': 'Tech Solutions Inc',
        'industry': 'Software Development',
        'size': '100',
        'current_processes': '''
        - Manual code deployment
        - Email-based project management
        - Spreadsheet-based resource allocation
        - Paper-based expense tracking
        ''',
        'pain_points': '''
        - Slow deployment process
        - Poor communication between teams
        - Inefficient resource management
        - Delayed expense approvals
        ''',
        'goals': '''
        - Implement CI/CD pipeline
        - Adopt project management software
        - Automate resource allocation
        - Digital expense management
        '''
    }
    
    analysis = analyze_business(detailed_business)
    assert analysis is not None
    assert len(analysis) > 0
    
    # Check for detailed recommendations
    assert any(term in analysis.lower() for term in [
        'ci/cd',
        'automation',
        'digital',
        'workflow',
        'integration'
    ]) 