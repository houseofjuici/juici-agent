import os
import json
import yaml
import warnings
from dotenv import load_dotenv
from praisonaiagents import Agent
from pathlib import Path

# Filter out specific warnings
warnings.filterwarnings('ignore', category=UserWarning, module='main')

def load_config(agent_name):
    """Load agent configuration from JSON file."""
    with open('agent_config.json', 'r') as f:
        config = json.load(f)
        return config['agents'][agent_name]

def load_prompt(agent_name):
    """Load agent instructions from YAML file."""
    prompt_path = Path('prompts') / f"{agent_name.lower()}.yaml"
    with open(prompt_path, 'r') as f:
        return yaml.safe_load(f)['instructions']

def analyze_performance(training_data, measurement_requirements):
    """
    Analyze performance metrics and ROI based on training outcomes.
    
    Args:
        training_data (str): Training program outcomes from the Trainer agent
        measurement_requirements (dict): Dictionary containing measurement requirements
            - baseline_metrics: Initial performance metrics
            - target_kpis: Target key performance indicators
            - measurement_period: Time period for analysis
            - stakeholders: Key stakeholders for reporting
            - success_criteria: Defined success criteria
    
    Returns:
        str: Detailed performance analysis and recommendations
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Check for API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Load configuration
        config = load_config('Measurer')
        instructions = load_prompt('Measurer')
        
        # Initialize agent
        agent = Agent(
            instructions=instructions,
            model=config['model'],
            temperature=config['temperature'],
            max_tokens=config['max_tokens']
        )
        
        # Prepare analysis prompt
        analysis_prompt = f"""
        Analyze performance metrics and ROI based on the following data and requirements:
        
        Training Outcomes:
        {training_data}
        
        Measurement Requirements:
        Baseline Metrics: {measurement_requirements['baseline_metrics']}
        Target KPIs: {', '.join(measurement_requirements['target_kpis'])}
        Measurement Period: {measurement_requirements['measurement_period']}
        Key Stakeholders: {', '.join(measurement_requirements['stakeholders'])}
        Success Criteria: {measurement_requirements['success_criteria']}
        
        Provide detailed performance analysis following the output format in your instructions.
        """
        
        # Get performance analysis
        response = agent.start(analysis_prompt)
        return response
        
    except Exception as e:
        return f"Error analyzing performance: {str(e)}"

def main():
    """Main function to run the Measurer agent interactively."""
    print("Digital Transform - Performance Measurer")
    print("=" * 50)
    
    # Get training outcomes
    print("\nPaste the training program outcomes from the Trainer agent:")
    training_data = input().strip()
    
    # Gather measurement requirements
    print("\nEnter measurement requirements:")
    measurement_requirements = {
        'baseline_metrics': input("Baseline performance metrics: "),
        'target_kpis': input("Target KPIs (comma-separated): ").split(','),
        'measurement_period': input("Measurement period: "),
        'stakeholders': input("Key stakeholders (comma-separated): ").split(','),
        'success_criteria': input("Success criteria: ")
    }
    
    # Analyze performance
    print("\nAnalyzing performance metrics...")
    analysis = analyze_performance(training_data, measurement_requirements)
    
    # Print results
    print("\nPerformance Analysis:")
    print("=" * 50)
    print(analysis)

if __name__ == "__main__":
    main() 