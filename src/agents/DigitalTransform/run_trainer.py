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

def create_training(automation_specs, training_requirements):
    """
    Create training materials and documentation based on automation specifications.
    
    Args:
        automation_specs (str): Automation specifications from the Automator agent
        training_requirements (dict): Dictionary containing training requirements
            - user_roles: List of user roles to train
            - skill_levels: Required skill levels
            - learning_objectives: Key learning objectives
            - delivery_methods: Preferred training delivery methods
            - assessment_needs: Assessment requirements
    
    Returns:
        str: Detailed training program and documentation
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Check for API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Load configuration
        config = load_config('Trainer')
        instructions = load_prompt('Trainer')
        
        # Initialize agent
        agent = Agent(
            instructions=instructions,
            model=config['model'],
            temperature=config['temperature'],
            max_tokens=config['max_tokens']
        )
        
        # Prepare training prompt
        training_prompt = f"""
        Create training materials and documentation based on the following specifications and requirements:
        
        Automation Specifications:
        {automation_specs}
        
        Training Requirements:
        User Roles: {', '.join(training_requirements['user_roles'])}
        Skill Levels: {', '.join(training_requirements['skill_levels'])}
        Learning Objectives: {', '.join(training_requirements['learning_objectives'])}
        Delivery Methods: {', '.join(training_requirements['delivery_methods'])}
        Assessment Needs: {training_requirements['assessment_needs']}
        
        Provide detailed training program and documentation following the output format in your instructions.
        """
        
        # Get training program
        response = agent.start(training_prompt)
        return response
        
    except Exception as e:
        return f"Error creating training materials: {str(e)}"

def main():
    """Main function to run the Trainer agent interactively."""
    print("Digital Transform - Training Developer")
    print("=" * 50)
    
    # Get automation specifications
    print("\nPaste the automation specifications from the Automator agent:")
    automation_specs = input().strip()
    
    # Gather training requirements
    print("\nEnter training requirements:")
    training_requirements = {
        'user_roles': input("User roles to train (comma-separated): ").split(','),
        'skill_levels': input("Required skill levels (comma-separated): ").split(','),
        'learning_objectives': input("Key learning objectives (comma-separated): ").split(','),
        'delivery_methods': input("Preferred delivery methods (comma-separated): ").split(','),
        'assessment_needs': input("Assessment requirements: ")
    }
    
    # Create training program
    print("\nCreating training program...")
    training = create_training(automation_specs, training_requirements)
    
    # Print results
    print("\nTraining Program:")
    print("=" * 50)
    print(training)

if __name__ == "__main__":
    main() 