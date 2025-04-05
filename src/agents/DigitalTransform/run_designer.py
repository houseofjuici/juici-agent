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

def create_design(solution_design, design_requirements):
    """
    Create UI/UX design based on technical solution and requirements.
    
    Args:
        solution_design (str): Technical solution from the Architect agent
        design_requirements (dict): Dictionary containing design requirements
            - platform: Target platform(s)
            - user_type: Primary user type/persona
            - brand_guidelines: Brand requirements
            - accessibility: Accessibility requirements
            - key_features: Main features to focus on
    
    Returns:
        str: Detailed design specifications and implementation guide
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Check for API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Load configuration
        config = load_config('Designer')
        instructions = load_prompt('Designer')
        
        # Initialize agent
        agent = Agent(
            instructions=instructions,
            model=config['model'],
            temperature=config['temperature'],
            max_tokens=config['max_tokens']
        )
        
        # Prepare design prompt
        design_prompt = f"""
        Create a user interface and experience design based on the following solution and requirements:
        
        Technical Solution:
        {solution_design}
        
        Design Requirements:
        Platform: {design_requirements['platform']}
        User Type: {design_requirements['user_type']}
        Brand Guidelines: {design_requirements['brand_guidelines']}
        Accessibility: {design_requirements['accessibility']}
        Key Features: {design_requirements['key_features']}
        
        Provide detailed design specifications following the output format in your instructions.
        """
        
        # Get design specifications
        response = agent.start(design_prompt)
        return response
        
    except Exception as e:
        return f"Error creating design: {str(e)}"

def main():
    """Main function to run the Designer agent interactively."""
    print("Digital Transform - UX/UI Designer")
    print("=" * 50)
    
    # Get solution design
    print("\nPaste the solution design from the Architect agent:")
    solution_design = input().strip()
    
    # Gather design requirements
    design_requirements = {
        'platform': input("\nTarget platform(s) (web, mobile, desktop): "),
        'user_type': input("Primary user type/persona: "),
        'brand_guidelines': input("Brand guidelines/requirements: "),
        'accessibility': input("Accessibility requirements (WCAG level): "),
        'key_features': input("Key features to focus on (comma-separated): ")
    }
    
    # Create design
    print("\nCreating UI/UX design...")
    design = create_design(solution_design, design_requirements)
    
    # Print results
    print("\nDesign Specifications:")
    print("=" * 50)
    print(design)

if __name__ == "__main__":
    main() 