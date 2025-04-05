import os
import json
import yaml
import warnings
import asyncio
from typing import Dict, List
from dotenv import load_dotenv
from praisonaiagents import Agent, PraisonAIAgents
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

class AnalystAgent:
    def __init__(self):
        self.config = load_config('Analyst')
        self.instructions = load_prompt('Analyst')
        self.memory = {}
        self.initialize_agents()

    def initialize_agents(self):
        """Initialize specialized sub-agents for different analysis tasks."""
        self.process_analyzer = Agent(
            instructions=f"{self.instructions}\nFocus on process analysis and workflow optimization.",
            model=self.config['model'],
            temperature=0.3
        )
        
        self.gap_assessor = Agent(
            instructions=f"{self.instructions}\nFocus on identifying gaps and maturity assessment.",
            model=self.config['model'],
            temperature=0.3
        )
        
        self.opportunity_finder = Agent(
            instructions=f"{self.instructions}\nFocus on identifying opportunities and innovation potential.",
            model=self.config['model'],
            temperature=0.7
        )
        
        self.recommendation_maker = Agent(
            instructions=f"{self.instructions}\nFocus on making actionable recommendations.",
            model=self.config['model'],
            temperature=0.4
        )

    async def analyze_processes(self, business_info: Dict) -> str:
        """Analyze business processes in parallel."""
        tasks = [
            self.process_analyzer.start(f"Analyze current processes:\n{business_info['current_processes']}"),
            self.gap_assessor.start(f"Assess gaps and maturity:\n{business_info['current_processes']}"),
            self.opportunity_finder.start(f"Identify opportunities:\n{business_info['current_processes']}")
        ]
        results = await asyncio.gather(*tasks)
        return "\n\n".join(results)

    def self_reflect(self, analysis: str, business_info: Dict) -> str:
        """Perform self-reflection on the analysis."""
        reflection_prompt = f"""
        Review and reflect on the following analysis:
        
        Analysis:
        {analysis}
        
        Business Context:
        {business_info}
        
        Consider:
        1. Are the assumptions valid?
        2. Is the analysis comprehensive?
        3. Are there alternative perspectives?
        4. What potential biases exist?
        5. How reliable are the recommendations?
        
        Provide reflection notes and any necessary adjustments.
        """
        
        reflection_agent = Agent(
            instructions="You are a critical thinking expert focused on validation and reflection.",
            model=self.config['model'],
            temperature=0.4
        )
        
        return reflection_agent.start(reflection_prompt)

    def store_in_memory(self, business_info: Dict, analysis: str):
        """Store analysis results in memory for future reference."""
        key = f"{business_info['name']}_{business_info['industry']}"
        self.memory[key] = {
            'analysis': analysis,
            'timestamp': asyncio.get_event_loop().time(),
            'context': business_info
        }

    async def analyze_business(self, business_info: Dict) -> str:
        """
        Analyze business processes with enhanced capabilities.
        
        Args:
            business_info (dict): Dictionary containing business information
                - name: Business name
                - industry: Industry sector
                - size: Company size
                - current_processes: Description of current processes
                - pain_points: Known issues or challenges
                - goals: Digital transformation goals
        
        Returns:
            str: Detailed analysis and recommendations
        """
        try:
            # Perform parallel analysis
            initial_analysis = await self.analyze_processes(business_info)
            
            # Self-reflection
            reflection = self.self_reflect(initial_analysis, business_info)
            
            # Generate final recommendations
            final_analysis = self.recommendation_maker.start(f"""
            Create final recommendations based on:
            
            Initial Analysis:
            {initial_analysis}
            
            Self-Reflection:
            {reflection}
            
            Business Context:
            {business_info}
            """)
            
            # Store in memory
            self.store_in_memory(business_info, final_analysis)
            
            return final_analysis
            
        except Exception as e:
            return f"Error performing analysis: {str(e)}"

async def main():
    """Main function to run the Analyst agent interactively."""
    print("Digital Transform - Business Process Analyst")
    print("=" * 50)
    
    # Initialize agent
    analyst = AnalystAgent()
    
    # Gather business information
    business_info = {
        'name': input("Business Name: "),
        'industry': input("Industry: "),
        'size': input("Company Size (employees): "),
        'current_processes': input("Describe current processes: "),
        'pain_points': input("What are the main pain points? "),
        'goals': input("What are your digital transformation goals? ")
    }
    
    # Run analysis
    print("\nAnalyzing business processes...")
    analysis = await analyst.analyze_business(business_info)
    
    # Print results
    print("\nAnalysis Results:")
    print("=" * 50)
    print(analysis)

if __name__ == "__main__":
    asyncio.run(main()) 