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
    print("FunnelBot - Sales Funnel Copy Generator")
    print("1. Generate Landing Page Copy")
    print("2. Create Email Sequence")
    print("3. Design Sales Page")
    choice = input("Select task (1-3): ")
    
    if choice == "1":
        product = input("Enter product/service name: ")
        target_audience = input("Enter target audience: ")
        response = agent.start(f"Create landing page copy for {product} targeting {target_audience}")
    elif choice == "2":
        product = input("Enter product/service name: ")
        sequence_length = input("Enter number of emails (3-7): ")
        response = agent.start(f"Create a {sequence_length}-email sequence for {product}")
    elif choice == "3":
        product = input("Enter product/service name: ")
        price = input("Enter price point: ")
        response = agent.start(f"Create sales page copy for {product} priced at {price}")
    else:
        print("Invalid choice")
        return
    
    # Print response
    print("\nGenerated Marketing Copy:")
    print("=" * 50)
    print(response)
    print("=" * 50)

if __name__ == "__main__":
    main() 