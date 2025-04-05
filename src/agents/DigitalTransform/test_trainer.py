import pytest
import os
from dotenv import load_dotenv
from run_trainer import create_training, load_config, load_prompt

@pytest.fixture(autouse=True)
def setup_env():
    """Setup environment variables for tests."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set. Skipping tests.")

def test_config_loading():
    """Test that the agent configuration can be loaded correctly."""
    config = load_config('Trainer')
    assert config is not None
    assert config['name'] == 'Trainer'
    assert config['model'] == 'gpt-4-turbo-preview'
    assert isinstance(config['temperature'], float)
    assert isinstance(config['max_tokens'], int)
    assert isinstance(config['tools'], list)

def test_prompt_loading():
    """Test that the agent prompt can be loaded correctly."""
    prompt = load_prompt('Trainer')
    assert prompt is not None
    assert isinstance(prompt, str)
    assert "You are Trainer" in prompt
    assert "Output format:" in prompt

def test_training_creation():
    """Test the training material creation functionality."""
    test_automation = """
    Automation Workflows:
    - Customer onboarding process
    - Data synchronization
    - Report generation
    
    System Integrations:
    - CRM integration
    - Email automation
    - Document management
    
    Testing Framework:
    - Unit test suite
    - Integration tests
    - Performance monitoring
    """
    
    test_requirements = {
        'user_roles': ['end_users', 'administrators', 'support_staff'],
        'skill_levels': ['beginner', 'intermediate', 'advanced'],
        'learning_objectives': ['system_usage', 'troubleshooting', 'best_practices'],
        'delivery_methods': ['video', 'documentation', 'workshops'],
        'assessment_needs': 'Regular skill assessments and certification tracking'
    }
    
    training = create_training(test_automation, test_requirements)
    assert training is not None
    assert len(training) > 0
    
    # Check for required sections in output
    assert any(term in training.lower() for term in [
        'training program',
        'documentation',
        'learning resources',
        'assessment tools'
    ])

def test_error_handling():
    """Test error handling for invalid input."""
    invalid_requirements = {
        'user_roles': [],  # Empty roles
        'skill_levels': ['invalid'],  # Invalid level
        'learning_objectives': None,  # Missing objectives
        'delivery_methods': [],
        'assessment_needs': ''
    }
    
    training = create_training("Test automation", invalid_requirements)
    assert "Error" in training

def test_comprehensive_training():
    """Test comprehensive training creation with detailed input."""
    detailed_automation = """
    Automation Workflows:
    - Multi-step approval process
    - Real-time data synchronization
    - Automated reporting system
    - Alert management
    - Audit logging
    
    System Integrations:
    - Enterprise CRM
    - Cloud storage
    - Communication platform
    - Analytics engine
    - Security systems
    
    Testing Framework:
    - Comprehensive test suite
    - Load testing
    - Security testing
    - User acceptance testing
    - Monitoring dashboard
    """
    
    detailed_requirements = {
        'user_roles': [
            'system_administrators',
            'business_analysts',
            'end_users',
            'support_team',
            'managers'
        ],
        'skill_levels': [
            'beginner',
            'intermediate',
            'advanced',
            'expert'
        ],
        'learning_objectives': [
            'system_administration',
            'workflow_management',
            'data_analysis',
            'troubleshooting',
            'security_best_practices'
        ],
        'delivery_methods': [
            'interactive_workshops',
            'video_tutorials',
            'hands_on_labs',
            'documentation',
            'webinars'
        ],
        'assessment_needs': 'Comprehensive skill assessment, certification program, progress tracking'
    }
    
    training = create_training(detailed_automation, detailed_requirements)
    assert training is not None
    assert len(training) > 0
    
    # Check for detailed training elements
    assert any(term in training.lower() for term in [
        'course',
        'workshop',
        'assessment',
        'certification',
        'documentation'
    ]) 