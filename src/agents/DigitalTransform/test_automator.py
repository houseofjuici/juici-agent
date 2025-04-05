import pytest
import os
from dotenv import load_dotenv
from run_automator import create_automation, load_config, load_prompt

@pytest.fixture(autouse=True)
def setup_env():
    """Setup environment variables for tests."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set. Skipping tests.")

def test_config_loading():
    """Test that the agent configuration can be loaded correctly."""
    config = load_config('Automator')
    assert config is not None
    assert config['name'] == 'Automator'
    assert config['model'] == 'gpt-4-turbo-preview'
    assert isinstance(config['temperature'], float)
    assert isinstance(config['max_tokens'], int)
    assert isinstance(config['tools'], list)

def test_prompt_loading():
    """Test that the agent prompt can be loaded correctly."""
    prompt = load_prompt('Automator')
    assert prompt is not None
    assert isinstance(prompt, str)
    assert "You are Automator" in prompt
    assert "Output format:" in prompt

def test_automation_creation():
    """Test the automation creation functionality."""
    test_design = """
    Design System:
    - Modern component library
    - RESTful API integration
    - Real-time updates
    - User authentication flow
    
    Interface Designs:
    - Dashboard layout
    - Data visualization components
    - Form automation
    - Workflow management
    """
    
    test_requirements = {
        'processes': ['data_entry', 'report_generation', 'approval_workflow'],
        'integrations': ['CRM', 'ERP', 'Email'],
        'data_sources': ['PostgreSQL', 'REST APIs', 'File System'],
        'performance_reqs': 'Response time < 500ms, 99.9% uptime',
        'security_reqs': 'OAuth2, encryption at rest, audit logging'
    }
    
    automation = create_automation(test_design, test_requirements)
    assert automation is not None
    assert len(automation) > 0
    
    # Check for required sections in output
    assert any(term in automation.lower() for term in [
        'automation workflows',
        'system integrations',
        'testing framework',
        'documentation'
    ])

def test_error_handling():
    """Test error handling for invalid input."""
    invalid_requirements = {
        'processes': [],  # Empty processes
        'integrations': ['invalid'],  # Invalid integration
        'data_sources': None,  # Missing data sources
        'performance_reqs': '',
        'security_reqs': ''
    }
    
    automation = create_automation("Test design", invalid_requirements)
    assert "Error" in automation

def test_comprehensive_automation():
    """Test comprehensive automation creation with detailed input."""
    detailed_design = """
    Design System:
    - Enterprise component library
    - GraphQL API integration
    - WebSocket real-time updates
    - SSO authentication
    - Role-based access control
    
    Interface Designs:
    - Executive dashboard
    - Analytics visualization
    - Automated workflow builder
    - Integration management console
    - Monitoring dashboard
    """
    
    detailed_requirements = {
        'processes': [
            'customer_onboarding',
            'data_synchronization',
            'report_scheduling',
            'alert_management',
            'audit_logging'
        ],
        'integrations': [
            'Salesforce',
            'SAP',
            'Microsoft365',
            'Slack',
            'Jira'
        ],
        'data_sources': [
            'PostgreSQL',
            'MongoDB',
            'Redis',
            'S3',
            'External APIs'
        ],
        'performance_reqs': 'Response time < 200ms, 99.99% uptime, auto-scaling',
        'security_reqs': 'SSO, MFA, encryption, audit trails, compliance monitoring'
    }
    
    automation = create_automation(detailed_design, detailed_requirements)
    assert automation is not None
    assert len(automation) > 0
    
    # Check for detailed automation elements
    assert any(term in automation.lower() for term in [
        'workflow',
        'integration',
        'api',
        'monitoring',
        'security'
    ]) 