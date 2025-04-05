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

def create_automation(design_specs, automation_requirements):
    """
    Create automation and integration solutions based on design specifications.
    
    Args:
        design_specs (str): UI/UX design specifications from the Designer agent
        automation_requirements (dict): Dictionary containing automation requirements
            - processes: List of processes to automate
            - integrations: Required system integrations
            - data_sources: Data sources to connect
            - performance_reqs: Performance requirements
            - security_reqs: Security requirements
    
    Returns:
        str: Detailed automation specifications and implementation guide
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Check for API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Load configuration
        config = load_config('Automator')
        instructions = load_prompt('Automator')
        
        # Initialize agent
        agent = Agent(
            instructions=instructions,
            model=config['model'],
            temperature=config['temperature'],
            max_tokens=config['max_tokens']
        )
        
        # Prepare automation prompt
        automation_prompt = f"""
        Create automation and integration solutions based on the following specifications and requirements:
        
        Design Specifications:
        {design_specs}
        
        Automation Requirements:
        Processes to Automate: {', '.join(automation_requirements['processes'])}
        Required Integrations: {', '.join(automation_requirements['integrations'])}
        Data Sources: {', '.join(automation_requirements['data_sources'])}
        Performance Requirements: {automation_requirements['performance_reqs']}
        Security Requirements: {automation_requirements['security_reqs']}
        
        Provide detailed automation specifications following the output format in your instructions.
        """
        
        # Get automation specifications
        response = agent.start(automation_prompt)
        return response
        
    except Exception as e:
        return f"Error creating automation: {str(e)}"

def main():
    """Main function to run the Automator agent interactively."""
    print("Digital Transform - Process Automator")
    print("=" * 50)
    
    # Get design specifications
    print("\nPaste the design specifications from the Designer agent:")
    design_specs = input().strip()
    
    # Gather automation requirements
    print("\nEnter automation requirements:")
    automation_requirements = {
        'processes': input("Processes to automate (comma-separated): ").split(','),
        'integrations': input("Required system integrations (comma-separated): ").split(','),
        'data_sources': input("Data sources to connect (comma-separated): ").split(','),
        'performance_reqs': input("Performance requirements: "),
        'security_reqs': input("Security requirements: ")
    }
    
    # Create automation solution
    print("\nCreating automation solution...")
    automation = create_automation(design_specs, automation_requirements)
    
    # Print results
    print("\nAutomation Specifications:")
    print("=" * 50)
    print(automation)

if __name__ == "__main__":
    main() 