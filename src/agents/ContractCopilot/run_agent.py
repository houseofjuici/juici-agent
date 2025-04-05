import os
import json
import yaml
import warnings
from dotenv import load_dotenv
from praisonaiagents import Agent
from pathlib import Path

# Filter out specific warnings
warnings.filterwarnings('ignore', category=UserWarning, module='main')

def load_config():
    """Load agent configuration from JSON file."""
    with open('agent_config.json', 'r') as f:
        return json.load(f)

def load_prompt():
    """Load agent instructions from YAML file."""
    with open('prompt.yaml', 'r') as f:
        return yaml.safe_load(f)['instructions']

def main():
    # Load environment variables from the root directory
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path, override=True)
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("Error: OPENAI_API_KEY not found or not set.")
        print("Please set your OpenAI API key in the .env file.")
        return
    
    # Load configuration
    config = load_config()
    instructions = load_prompt()
    
    # Initialize agent
    agent = Agent(instructions=instructions)
    
    # Start agent
    print("ContractCopilot - Legal Assistant")
    print("1. Analyze Contract")
    print("2. Generate Clause")
    print("3. Review Language")
    choice = input("Select task (1-3): ")
    
    if choice == "1":
        contract = input("Paste the contract text to analyze: ")
        response = agent.start(f"Analyze this contract:\n{contract}")
    elif choice == "2":
        clause_type = input("Enter the type of clause to generate: ")
        response = agent.start(f"Generate a {clause_type} clause")
    elif choice == "3":
        language = input("Paste the contract language to review: ")
        response = agent.start(f"Review this contract language:\n{language}")
    else:
        print("Invalid choice")
        return
    
    # Print response
    print("\nLegal Analysis:")
    print("=" * 50)
    print(response)
    print("=" * 50)

if __name__ == "__main__":
    main() 