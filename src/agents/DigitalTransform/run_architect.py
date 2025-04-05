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

def design_solution(analysis_results, requirements):
    """
    Design technical solution based on analysis results and requirements.
    
    Args:
        analysis_results (str): Results from the Analyst agent
        requirements (dict): Dictionary containing solution requirements
            - scale: Expected scale/growth
            - budget: Budget constraints
            - timeline: Implementation timeline
            - tech_preferences: Preferred technologies
            - security_requirements: Security needs
    
    Returns:
        str: Detailed solution design and implementation plan
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Check for API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Load configuration
        config = load_config('Architect')
        instructions = load_prompt('Architect')
        
        # Initialize agent
        agent = Agent(
            instructions=instructions,
            model=config['model'],
            temperature=config['temperature'],
            max_tokens=config['max_tokens']
        )
        
        # Prepare design prompt
        design_prompt = f"""
        Design a technical solution based on the following analysis and requirements:
        
        Analysis Results:
        {analysis_results}
        
        Requirements:
        Scale: {requirements['scale']}
        Budget: {requirements['budget']}
        Timeline: {requirements['timeline']}
        Tech Preferences: {requirements['tech_preferences']}
        Security Requirements: {requirements['security_requirements']}
        
        Provide a detailed solution design following the output format in your instructions.
        """
        
        # Get solution design
        response = agent.start(design_prompt)
        return response
        
    except Exception as e:
        return f"Error designing solution: {str(e)}"

def main():
    """Main function to run the Architect agent interactively."""
    print("Digital Transform - Solution Architect")
    print("=" * 50)
    
    # Get analysis results
    print("\nPaste the analysis results from the Analyst agent:")
    analysis_results = input().strip()
    
    # Gather requirements
    requirements = {
        'scale': input("\nExpected scale/growth: "),
        'budget': input("Budget constraints: "),
        'timeline': input("Implementation timeline: "),
        'tech_preferences': input("Preferred technologies (comma-separated): "),
        'security_requirements': input("Security requirements: ")
    }
    
    # Design solution
    print("\nDesigning technical solution...")
    solution = design_solution(analysis_results, requirements)
    
    # Print results
    print("\nSolution Design:")
    print("=" * 50)
    print(solution)

if __name__ == "__main__":
    main() 