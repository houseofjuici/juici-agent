import pytest
import os
from dotenv import load_dotenv
from run_measurer import analyze_performance, load_config, load_prompt

@pytest.fixture(autouse=True)
def setup_env():
    """Setup environment variables for tests."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set. Skipping tests.")

def test_config_loading():
    """Test that the agent configuration can be loaded correctly."""
    config = load_config('Measurer')
    assert config is not None
    assert config['name'] == 'Measurer'
    assert config['model'] == 'gpt-4-turbo-preview'
    assert isinstance(config['temperature'], float)
    assert isinstance(config['max_tokens'], int)
    assert isinstance(config['tools'], list)

def test_prompt_loading():
    """Test that the agent prompt can be loaded correctly."""
    prompt = load_prompt('Measurer')
    assert prompt is not None
    assert isinstance(prompt, str)
    assert "You are Measurer" in prompt
    assert "Output format:" in prompt

def test_performance_analysis():
    """Test the performance analysis functionality."""
    test_training = """
    Training Program Results:
    - 95% completion rate
    - Average skill improvement: 40%
    - User satisfaction: 4.5/5
    
    Adoption Metrics:
    - Daily active users: 500
    - Feature utilization: 75%
    - Support tickets: reduced by 30%
    
    Business Impact:
    - Process time reduced by 45%
    - Error rate decreased by 60%
    - Cost savings: $100,000
    """
    
    test_requirements = {
        'baseline_metrics': 'Process time: 2 hours, Error rate: 10%, Cost per transaction: $50',
        'target_kpis': ['process_efficiency', 'error_reduction', 'cost_savings'],
        'measurement_period': 'Q3 2024',
        'stakeholders': ['executive_team', 'department_heads', 'end_users'],
        'success_criteria': 'ROI > 200%, User adoption > 80%, Error reduction > 50%'
    }
    
    analysis = analyze_performance(test_training, test_requirements)
    assert analysis is not None
    assert len(analysis) > 0
    
    # Check for required sections in output
    assert any(term in analysis.lower() for term in [
        'performance metrics',
        'roi analysis',
        'impact assessment',
        'recommendations'
    ])

def test_error_handling():
    """Test error handling for invalid input."""
    invalid_requirements = {
        'baseline_metrics': '',  # Empty metrics
        'target_kpis': ['invalid'],  # Invalid KPI
        'measurement_period': None,  # Missing period
        'stakeholders': [],
        'success_criteria': ''
    }
    
    analysis = analyze_performance("Test training", invalid_requirements)
    assert "Error" in analysis

def test_comprehensive_analysis():
    """Test comprehensive performance analysis with detailed input."""
    detailed_training = """
    Training Program Results:
    - Course completion: 98%
    - Certification rate: 85%
    - Average assessment score: 92%
    - User satisfaction: 4.8/5
    
    System Adoption Metrics:
    - Daily active users: 1,200
    - Feature utilization: 85%
    - Mobile app usage: 60%
    - API calls: 50,000/day
    
    Process Improvements:
    - Workflow automation: 75%
    - Document processing time: -65%
    - Data accuracy: +40%
    - Integration success rate: 99.9%
    
    Business Impact:
    - Annual cost savings: $500,000
    - Employee productivity: +35%
    - Customer satisfaction: +25%
    - Market response time: -50%
    """
    
    detailed_requirements = {
        'baseline_metrics': '''
        Process time: 4 hours/transaction
        Error rate: 15%
        Cost per transaction: $75
        Customer satisfaction: 3.5/5
        Employee productivity index: 100
        ''',
        'target_kpis': [
            'process_efficiency',
            'error_reduction',
            'cost_optimization',
            'user_adoption',
            'system_performance',
            'business_impact'
        ],
        'measurement_period': 'Full Year 2024',
        'stakeholders': [
            'ceo',
            'cto',
            'department_heads',
            'project_managers',
            'end_users',
            'customers'
        ],
        'success_criteria': '''
        ROI > 300%
        User adoption > 85%
        Error reduction > 60%
        Cost savings > $400,000
        System uptime > 99.9%
        Customer satisfaction > 4.5/5
        '''
    }
    
    analysis = analyze_performance(detailed_training, detailed_requirements)
    assert analysis is not None
    assert len(analysis) > 0
    
    # Check for detailed analysis elements
    assert any(term in analysis.lower() for term in [
        'metrics',
        'roi',
        'impact',
        'adoption',
        'recommendations'
    ]) 