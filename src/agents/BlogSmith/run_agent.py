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
    topic = input("Enter the blog topic: ")
    response = agent.start(f"Create a blog post about: {topic}")
    
    # Print response
    print("\nGenerated Blog Post:")
    print("=" * 50)
    print(response)
    print("=" * 50)

if __name__ == "__main__":
    main() 