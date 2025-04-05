import os
import json
import yaml
import warnings
import re
from datetime import datetime, timedelta
from typing import Dict, Optional
from dotenv import load_dotenv
from praisonaiagents import Agent
from pathlib import Path

# Filter out specific warnings
warnings.filterwarnings('ignore', category=UserWarning, module='main')

# Rate limiting configuration
RATE_LIMIT_WINDOW = timedelta(minutes=1)
MAX_REQUESTS_PER_WINDOW = 5

class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, user_id: str) -> bool:
        now = datetime.now()
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Remove old requests
        self.requests[user_id] = [t for t in self.requests[user_id] 
                                if now - t < RATE_LIMIT_WINDOW]
        
        if len(self.requests[user_id]) >= MAX_REQUESTS_PER_WINDOW:
            return False
        
        self.requests[user_id].append(now)
        return True

def validate_input(text: str) -> bool:
    """Validate input to prevent injection attacks."""
    if not text or len(text.strip()) == 0:
        return False
    
    if len(text) > 1000:
        return False
        
    # Check for harmful patterns
    harmful_pattern = r'[<>{}()\[\]\\/;:\'"`]|script|alert|eval|exec|system|cmd|shell'
    if re.search(harmful_pattern, text, flags=re.IGNORECASE):
        return False
        
    # Additional check for common XSS patterns
    xss_pattern = r'<[^>]*>|javascript:|data:|vbscript:'
    if re.search(xss_pattern, text, flags=re.IGNORECASE):
        return False
    
    return True

def load_config() -> dict:
    """Load agent configuration from JSON file."""
    try:
        with open('agent_config.json', 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise RuntimeError("Failed to load configuration") from e

def load_prompt() -> str:
    """Load agent instructions from YAML file."""
    try:
        with open('prompt.yaml', 'r') as f:
            return yaml.safe_load(f)['instructions']
    except (yaml.YAMLError, FileNotFoundError) as e:
        raise RuntimeError("Failed to load prompt") from e

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
    
    # Initialize rate limiter
    rate_limiter = RateLimiter()
    
    try:
        # Load configuration
        config = load_config()
        instructions = load_prompt()
        
        # Initialize agent
        agent = Agent(instructions=instructions)
        
        # Start agent
        print("FitCoachAI - Personalized Fitness Assistant")
        print("1. Create Workout Plan")
        print("2. Get Nutrition Advice")
        print("3. Learn Exercise Form")
        print("4. Track Progress")
        
        choice = input("Select task (1-4): ")
        
        # Validate choice
        if not choice.isdigit() or int(choice) not in range(1, 5):
            print("Invalid choice. Please select a number between 1 and 4.")
            return
        
        # Check rate limit
        user_id = "default_user"  # In a real app, this would be a unique user identifier
        if not rate_limiter.is_allowed(user_id):
            print("Rate limit exceeded. Please try again later.")
            return
        
        # Process user input based on choice
        if choice == "1":
            fitness_level = input("Enter your fitness level (beginner/intermediate/advanced): ")
            goals = input("Enter your fitness goals: ")
            equipment = input("What equipment do you have available? ")
            
            # Validate inputs
            if not all(validate_input(x) for x in [fitness_level, goals, equipment]):
                print("Invalid input. Please try again with valid characters.")
                return
                
            response = agent.start(f"Create a workout plan for a {fitness_level} with goals: {goals}. Available equipment: {equipment}")
            
        elif choice == "2":
            dietary_restrictions = input("Any dietary restrictions? ")
            goals = input("Enter your nutrition goals: ")
            
            # Validate inputs
            if not all(validate_input(x) for x in [dietary_restrictions, goals]):
                print("Invalid input. Please try again with valid characters.")
                return
                
            response = agent.start(f"Provide nutrition advice for someone with {dietary_restrictions} and goals: {goals}")
            
        elif choice == "3":
            exercise = input("Which exercise would you like to learn? ")
            experience = input("What's your experience level with this exercise? ")
            
            # Validate inputs
            if not all(validate_input(x) for x in [exercise, experience]):
                print("Invalid input. Please try again with valid characters.")
                return
                
            response = agent.start(f"Guide proper form for {exercise} for someone with {experience} experience")
            
        elif choice == "4":
            current_progress = input("Describe your current progress: ")
            goals = input("What are your current goals? ")
            
            # Validate inputs
            if not all(validate_input(x) for x in [current_progress, goals]):
                print("Invalid input. Please try again with valid characters.")
                return
                
            response = agent.start(f"Track progress for someone with current progress: {current_progress}. Goals: {goals}")
        
        # Print response
        print("\nFitness Guidance:")
        print("=" * 50)
        print(response)
        print("=" * 50)
        
    except Exception as e:
        print("An error occurred. Please try again later.")
        # Log the error (in a real app, this would be proper logging)
        print(f"Error details: {str(e)}")

if __name__ == "__main__":
    main() 