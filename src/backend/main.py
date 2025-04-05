from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, AsyncGenerator
import os
import yaml
import json
import asyncio
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from praisonaiagents import Agent
import requests
from PIL import Image
from io import BytesIO
import base64
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from fastapi.middleware.gzip import GZipMiddleware
import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient
import gc
import psutil
import time
import random
from config import CORS_ORIGINS, OLLAMA_GENERATE_ENDPOINT, DEFAULT_TIMEOUT

# Load environment variables from the root directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path, override=True)

# Optional environment variable check - now we don't require it since users can provide their own
default_api_key = os.getenv('OPENAI_API_KEY')
if not default_api_key:
    print("Warning: No default OPENAI_API_KEY found in environment variables. Users must provide their own.")

app = FastAPI(title="Juici Agents API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    agent_name: str
    message: str
    context: Optional[Dict[str, Any]] = None

class AgentConfig(BaseModel):
    name: str
    description: str
    tools: List[str]

class AgentInfo(BaseModel):
    config: AgentConfig
    example_prompts: List[str]

# Digital Transform Team Models
class BusinessInfo(BaseModel):
    name: str
    industry: str
    size: str
    current_processes: str
    pain_points: str
    goals: str

class AnalysisRequest(BaseModel):
    business_info: BusinessInfo

class DesignRequest(BaseModel):
    solution_design: str
    design_requirements: Dict[str, Any]

class AutomationRequest(BaseModel):
    design_specs: str
    automation_requirements: Dict[str, Any]

class TrainingRequest(BaseModel):
    automation_specs: str
    training_requirements: Dict[str, Any]

class MeasurementRequest(BaseModel):
    training_data: str
    measurement_requirements: Dict[str, Any]

# Create thread pool for parallel processing
thread_pool = ThreadPoolExecutor(max_workers=10)

# Create response queue for streaming
response_queue = queue.Queue()

class StreamingAgent(Agent):
    """Enhanced Agent with streaming capabilities"""
    def __init__(self, *args, api_key=None, **kwargs):
        # Pass API key to the parent Agent class
        if api_key:
            kwargs['api_key'] = api_key
        super().__init__(*args, **kwargs)
        self.response_queue = response_queue

    async def stream_start(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream responses as they are generated"""
        try:
            # Start response generation in a separate thread
            future = thread_pool.submit(self.start, prompt)
            
            # Stream partial responses
            while not future.done():
                if not self.response_queue.empty():
                    yield self.response_queue.get()
                await asyncio.sleep(0.1)
            
            # Get final response
            final_response = future.result()
            if final_response:
                yield final_response
                
        except Exception as e:
            yield f"Error: {str(e)}"

# Add utility functions
def load_agent_config(agent_name: str) -> tuple[dict, str]:
    """Load agent configuration and prompt."""
    try:
        base_path = Path(__file__).parent.parent
        
        if agent_name.startswith('digital_transform_'):
            # Load from DigitalTransform directory
            config_path = base_path / 'DigitalTransform/agent_config.json'
            agent_type = agent_name.split('_')[-1].capitalize()
            prompt_path = base_path / 'DigitalTransform/prompts' / f"{agent_type.lower()}.yaml"
            
            if not config_path.exists() or not prompt_path.exists():
                raise FileNotFoundError(f"Configuration files not found for agent {agent_name}")
            
            with open(config_path) as f:
                full_config = json.load(f)
                if agent_type not in full_config['agents']:
                    raise ValueError(f"Agent {agent_type} not found in Digital Transform team")
                config = full_config['agents'][agent_type]
        else:
            # Load from agent-specific directory
            config_path = base_path / agent_name / "agent_config.json"
            prompt_path = base_path / agent_name / "prompt.yaml"
            
            if not config_path.exists() or not prompt_path.exists():
                raise FileNotFoundError(f"Configuration files not found for agent {agent_name}")
            
            with open(config_path) as f:
                config = json.load(f)
        
        with open(prompt_path) as f:
            prompt = yaml.safe_load(f)['instructions']
        
        return config, prompt
    except Exception as e:
        print(f"Error loading agent {agent_name}: {str(e)}")  # Debug log
        raise HTTPException(status_code=404, detail=f"Error loading agent {agent_name}: {str(e)}")

# Add AnalystAgent class
class AnalystAgent:
    def __init__(self):
        self.config = load_agent_config('digital_transform_analyst')[0]
        self.instructions = load_agent_config('digital_transform_analyst')[1]
        self.memory = {}
        self.api_key = None
        self.initialize_components()

    def update_api_key(self, api_key):
        """Update the API key for all components."""
        self.api_key = api_key
        # Update API key for all components
        self.process_analyzer = Agent(
            instructions=f"{self.instructions}\nFocus on process analysis and workflow optimization.",
            api_key=api_key
        )
        
        self.gap_assessor = Agent(
            instructions=f"{self.instructions}\nFocus on identifying gaps and maturity assessment.",
            api_key=api_key
        )
        
        self.opportunity_finder = Agent(
            instructions=f"{self.instructions}\nFocus on identifying opportunities and innovation potential.",
            api_key=api_key
        )
        
        self.recommendation_maker = Agent(
            instructions=f"{self.instructions}\nFocus on making actionable recommendations.",
            api_key=api_key
        )

    def initialize_components(self):
        """Initialize specialized components for different analysis tasks."""
        self.process_analyzer = Agent(
            instructions=f"{self.instructions}\nFocus on process analysis and workflow optimization."
        )
        
        self.gap_assessor = Agent(
            instructions=f"{self.instructions}\nFocus on identifying gaps and maturity assessment."
        )
        
        self.opportunity_finder = Agent(
            instructions=f"{self.instructions}\nFocus on identifying opportunities and innovation potential."
        )
        
        self.recommendation_maker = Agent(
            instructions=f"{self.instructions}\nFocus on making actionable recommendations."
        )

    async def analyze_business(self, business_info: Dict) -> str:
        """Analyze business processes with enhanced capabilities."""
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

    async def analyze_processes(self, business_info: Dict) -> str:
        """Analyze business processes in parallel."""
        try:
            tasks = [
                self.process_analyzer.start(f"Analyze current processes:\n{business_info['current_processes']}"),
                self.gap_assessor.start(f"Assess gaps and maturity:\n{business_info['current_processes']}"),
                self.opportunity_finder.start(f"Identify opportunities:\n{business_info['current_processes']}")
            ]
            results = await asyncio.gather(*tasks)
            return "\n\n".join(results)
        except Exception as e:
            print(f"Error in analyze_processes: {str(e)}")
            return f"Error analyzing processes: {str(e)}"

    def self_reflect(self, analysis: str, business_info: Dict) -> str:
        """Perform self-reflection on the analysis."""
        try:
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
                instructions="You are a critical thinking expert focused on validation and reflection."
            )
            
            return reflection_agent.start(reflection_prompt)
            
        except Exception as e:
            print(f"Error in self_reflect: {str(e)}")
            return f"Error during reflection: {str(e)}"

    def store_in_memory(self, business_info: Dict, analysis: str):
        """Store analysis results in memory for future reference."""
        try:
            key = f"{business_info['name']}_{business_info['industry']}"
            self.memory[key] = {
                'analysis': analysis,
                'timestamp': asyncio.get_event_loop().time(),
                'context': business_info
            }
        except Exception as e:
            print(f"Error storing in memory: {str(e)}")

# Now create the global instance
analyst_agent = AnalystAgent()

class StreamingAgent(Agent):
    """Enhanced Agent with streaming capabilities"""
    def __init__(self, *args, api_key=None, **kwargs):
        # Pass API key to the parent Agent class
        if api_key:
            kwargs['api_key'] = api_key
        super().__init__(*args, **kwargs)
        self.response_queue = response_queue

    async def stream_start(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream responses as they are generated"""
        try:
            # Start response generation in a separate thread
            future = thread_pool.submit(self.start, prompt)
            
            # Stream partial responses
            while not future.done():
                if not self.response_queue.empty():
                    yield self.response_queue.get()
                await asyncio.sleep(0.1)
            
            # Get final response
            final_response = future.result()
            if final_response:
                yield final_response
                
        except Exception as e:
            yield f"Error: {str(e)}"

@app.get("/agents", response_model=List[str])
async def list_agents():
    """List all available agents."""
    try:
        base_path = Path(__file__).parent.parent
        # List of directories to exclude
        exclude_dirs = {'frontend', 'backend', 'PraisonAI', '.git', '.pytest_cache', '__pycache__', 'DigitalTransform'}
        
        # Standard agents
        agent_dirs = [d.name for d in base_path.iterdir() 
                     if d.is_dir() 
                     and not d.name.startswith('.') 
                     and d.name not in exclude_dirs
                     and (d / "agent_config.json").exists()]
        
        # Add Digital Transform agents
        dt_config_path = base_path / 'DigitalTransform/agent_config.json'
        if dt_config_path.exists():
            with open(dt_config_path) as f:
                dt_config = json.load(f)
                agent_dirs.extend([f"digital_transform_{agent.lower()}" 
                                 for agent in dt_config['agents'].keys()])
        
        return sorted(agent_dirs)
    except Exception as e:
        print(f"Error listing agents: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=f"Error listing agents: {str(e)}")

@app.get("/agents/{agent_name}", response_model=AgentInfo)
async def get_agent_info(agent_name: str):
    """Get agent information and example prompts."""
    try:
        # Skip loading config for the DigitalTransform directory itself
        if agent_name == "DigitalTransform":
            raise HTTPException(status_code=404, detail="DigitalTransform is not a direct agent")
            
        config, _ = load_agent_config(agent_name)
        
        # Example prompts for Digital Transform agents
        dt_example_prompts = {
            "digital_transform_analyst": [
                "Analyze our current customer service processes for automation opportunities",
                "Assess our digital maturity and identify key gaps",
                "Evaluate our e-commerce workflow and recommend improvements"
            ],
            "digital_transform_architect": [
                "Design a cloud migration strategy for our legacy systems",
                "Create a technical roadmap for implementing AI-powered analytics",
                "Plan a microservices architecture for our monolithic application"
            ],
            "digital_transform_designer": [
                "Design a user-friendly interface for our new workflow automation system",
                "Create a mobile-first design for our customer portal",
                "Develop an accessible UI for our employee dashboard"
            ],
            "digital_transform_automator": [
                "Automate our invoice processing workflow",
                "Create API integrations between our CRM and ERP systems",
                "Implement automated testing for our deployment pipeline"
            ],
            "digital_transform_trainer": [
                "Create a training program for our new digital workflow",
                "Develop documentation for our automated systems",
                "Design learning paths for different user roles"
            ],
            "digital_transform_measurer": [
                "Set up KPIs for our digital transformation initiative",
                "Track ROI metrics for our automation project",
                "Measure user adoption and satisfaction rates"
            ],
            "digital_transform_datadetective": [
                "Create a trend analysis chart from our sales data",
                "Analyze this performance metrics visualization",
                "Generate a correlation matrix for our customer data",
                "Create an interactive dashboard for our KPIs",
                "Analyze this uploaded chart and identify key patterns"
            ]
        }
        
        # Combine with existing example prompts
        example_prompts = dt_example_prompts.get(agent_name, [])
        
        return {
            "config": config,
            "example_prompts": example_prompts
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error getting agent info for {agent_name}: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))

# Helper function to get API key from header or environment
async def get_api_key(x_openai_api_key: str = Header(None)):
    """
    Get OpenAI API key from header or use default from environment.
    If neither is available, raise an exception.
    """
    if x_openai_api_key:
        return x_openai_api_key
    elif default_api_key:
        return default_api_key
    else:
        raise HTTPException(
            status_code=401, 
            detail="OpenAI API key is required. Please provide it in the X-OpenAI-API-Key header."
        )

@app.post("/chat", response_model=Message)
async def chat_with_agent(request: ChatRequest, api_key: str = Depends(get_api_key)):
    """Chat with a specific agent using streaming responses."""
    try:
        config, prompt = load_agent_config(request.agent_name)
        # Pass API key to Agent
        agent = StreamingAgent(instructions=prompt, api_key=api_key)
        
        return StreamingResponse(
            agent.stream_start(request.message),
            media_type='text/event-stream'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Digital Transform Team Endpoints
@app.post("/digital_transform/analyze", response_model=Message)
async def analyze_business(request: AnalysisRequest, api_key: str = Depends(get_api_key)):
    """Analyze business processes with streaming responses."""
    try:
        # Update analyst_agent with the API key
        analyst_agent.update_api_key(api_key)
        business_info = request.business_info.dict()
        return StreamingResponse(
            analyst_agent.stream_analyze_business(business_info),
            media_type='text/event-stream'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/digital_transform/design", response_model=Message)
async def create_design(request: DesignRequest, api_key: str = Depends(get_api_key)):
    """Create design specifications using the Designer agent."""
    try:
        config, prompt = load_agent_config('digital_transform_designer')
        agent = Agent(instructions=prompt, api_key=api_key)
        
        design_prompt = f"""
        Create design based on:
        
        Solution: {request.solution_design}
        Requirements: {json.dumps(request.design_requirements, indent=2)}
        """
        
        response = agent.start(design_prompt)
        return Message(role="assistant", content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/digital_transform/automate", response_model=Message)
async def create_automation(request: AutomationRequest, api_key: str = Depends(get_api_key)):
    """Create automation solutions using the Automator agent."""
    try:
        config, prompt = load_agent_config('digital_transform_automator')
        agent = Agent(instructions=prompt, api_key=api_key)
        
        automation_prompt = f"""
        Create automation solution based on:
        
        Design: {request.design_specs}
        Requirements: {json.dumps(request.automation_requirements, indent=2)}
        """
        
        response = agent.start(automation_prompt)
        return Message(role="assistant", content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/digital_transform/train", response_model=Message)
async def create_training(request: TrainingRequest, api_key: str = Depends(get_api_key)):
    """Create training materials using the Trainer agent."""
    try:
        config, prompt = load_agent_config('digital_transform_trainer')
        agent = Agent(instructions=prompt, api_key=api_key)
        
        training_prompt = f"""
        Create training program based on:
        
        Automation: {request.automation_specs}
        Requirements: {json.dumps(request.training_requirements, indent=2)}
        """
        
        response = agent.start(training_prompt)
        return Message(role="assistant", content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/digital_transform/measure", response_model=Message)
async def analyze_performance(request: MeasurementRequest, api_key: str = Depends(get_api_key)):
    """Analyze performance metrics using the Measurer agent."""
    try:
        config, prompt = load_agent_config('digital_transform_measurer')
        agent = Agent(instructions=prompt, api_key=api_key)
        
        measurement_prompt = f"""
        Analyze performance based on:
        
        Training Data: {request.training_data}
        Requirements: {json.dumps(request.measurement_requirements, indent=2)}
        """
        
        response = agent.start(measurement_prompt)
        return Message(role="assistant", content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New Models for DataDetective
class ChartRequest(BaseModel):
    data: Dict[str, List[Any]]
    chart_type: str
    title: str
    x_label: str
    y_label: str
    additional_params: Optional[Dict[str, Any]] = None

class ImageAnalysisRequest(BaseModel):
    image_url: str
    analysis_type: str
    context: Optional[Dict[str, Any]] = None

class DataAnalysisRequest(BaseModel):
    data: Dict[str, List[Any]]
    analysis_type: str
    parameters: Optional[Dict[str, Any]] = None

# DataDetective Agent Class
class DataDetectiveAgent:
    def __init__(self):
        self.config = load_agent_config('digital_transform_datadetective')[0]
        self.instructions = load_agent_config('digital_transform_datadetective')[1]
        self.api_key = None
        self.initialize_components()

    def update_api_key(self, api_key):
        """Update the API key for all components."""
        self.api_key = api_key
        # Update API key for all components
        self.data_analyzer = Agent(
            instructions=f"{self.instructions}\nFocus on data analysis and pattern detection.",
            api_key=api_key
        )
        
        self.chart_creator = Agent(
            instructions=f"{self.instructions}\nFocus on data visualization and chart creation.",
            api_key=api_key
        )
        
        self.vision_analyzer = Agent(
            instructions=f"{self.instructions}\nFocus on visual analysis and chart interpretation.",
            api_key=api_key
        )

    def initialize_components(self):
        """Initialize specialized components for different analysis tasks."""
        self.data_analyzer = Agent(
            instructions=f"{self.instructions}\nFocus on data analysis and pattern detection."
        )
        
        self.chart_creator = Agent(
            instructions=f"{self.instructions}\nFocus on data visualization and chart creation."
        )
        
        self.vision_analyzer = Agent(
            instructions=f"{self.instructions}\nFocus on visual analysis and chart interpretation."
        )

    async def create_chart(self, request: ChartRequest) -> Dict[str, Any]:
        """Create a chart based on provided data and parameters."""
        try:
            df = pd.DataFrame(request.data)
            
            if request.chart_type == "line":
                fig = px.line(df, x=request.x_label, y=request.y_label, title=request.title)
            elif request.chart_type == "bar":
                fig = px.bar(df, x=request.x_label, y=request.y_label, title=request.title)
            elif request.chart_type == "scatter":
                fig = px.scatter(df, x=request.x_label, y=request.y_label, title=request.title)
            elif request.chart_type == "pie":
                fig = px.pie(df, values=request.y_label, names=request.x_label, title=request.title)
            elif request.chart_type == "heatmap":
                fig = px.imshow(df, title=request.title)
            
            # Apply additional parameters if provided
            if request.additional_params:
                for param, value in request.additional_params.items():
                    if hasattr(fig, param):
                        setattr(fig, param, value)
            
            # Convert to JSON for frontend
            chart_json = fig.to_json()
            return {"chart_data": chart_json}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating chart: {str(e)}")

    async def analyze_image(self, request: ImageAnalysisRequest) -> str:
        """Analyze chart or data visualization using Ollama locally or a cloud API in production."""
        try:
            # Download image if URL provided
            if request.image_url.startswith('http'):
                response = requests.get(request.image_url)
                img = Image.open(BytesIO(response.content))
                image_data = response.content
            else:
                # Load local image
                try:
                    img = Image.open(request.image_url)
                    with open(request.image_url, 'rb') as f:
                        image_data = f.read()
                except Exception as e:
                    print(f"Error loading image from {request.image_url}: {str(e)}")
                    raise HTTPException(status_code=400, detail=f"Error loading image: {str(e)}")
            
            # Optimize image size for faster processing
            max_size = 1024  # Maximum dimension
            if img.size[0] > max_size or img.size[1] > max_size:
                ratio = min(max_size/img.size[0], max_size/img.size[1])
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Convert back to bytes
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='JPEG', quality=85, optimize=True)
                image_data = img_byte_arr.getvalue()
            
            # Prepare prompt based on analysis type
            vision_prompt = f"""
            Analyze this chart/visualization.
            Analysis type: {request.analysis_type}
            
            Consider:
            1. Type of visualization
            2. Key trends or patterns
            3. Data relationships
            4. Notable insights
            5. Potential issues or concerns
            
            Additional context: {json.dumps(request.context) if request.context else 'None'}
            """
            
            # Check environment
            is_vercel = os.environ.get("VERCEL") == "1"
            
            if is_vercel:
                # In Vercel, fallback to mock response for demo purposes
                print("Running in Vercel environment, returning mock analysis")
                time.sleep(2)  # Simulate processing time
                return f"""
                # Chart Analysis

                This appears to be a {random.choice(['bar chart', 'line graph', 'scatter plot', 'pie chart', 'heat map'])}.
                
                ## Key Observations:
                
                - Clear {random.choice(['upward', 'downward', 'cyclical', 'steady'])} trend visible in the data
                - Data points show {random.choice(['strong', 'moderate', 'weak'])} correlation
                - Notable {random.choice(['outliers', 'clusters', 'patterns'])} present
                
                ## Insights:
                
                1. The visualization effectively shows {random.choice(['comparison between categories', 'changes over time', 'distribution of values', 'part-to-whole relationships'])}
                2. The {random.choice(['color scheme', 'scale', 'labeling'])} could be improved for better clarity
                3. Consider adding {random.choice(['annotations', 'trend lines', 'confidence intervals'])} to enhance understanding
                
                ## Recommendations:
                
                - {random.choice(['Normalize the data', 'Use a logarithmic scale', 'Add a secondary axis'])} to improve interpretability
                - {random.choice(['Highlight key data points', 'Add a reference line', 'Include data labels'])} for emphasis
                - Consider {random.choice(['alternative chart types', 'interactive elements', 'supplementary visualizations'])} to tell a more complete story
                
                *This is a demonstration response in the Vercel environment where Ollama is not available.*
                """
            
            try:
                # Convert image to base64
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                
                # Call Ollama llava model API with optimized parameters
                ollama_response = requests.post(
                    OLLAMA_GENERATE_ENDPOINT,
                    json={
                        "model": "llava",
                        "prompt": vision_prompt,
                        "images": [image_base64],
                        "stream": False,
                        "options": {
                            "num_ctx": 2048,  # Reduced context window
                            "num_thread": 4,  # Use multiple threads
                            "temperature": 0.1,  # Lower temperature for faster, more focused responses
                            "top_k": 20,  # Reduced top_k for faster sampling
                            "top_p": 0.9  # Slightly reduced top_p
                        }
                    },
                    timeout=DEFAULT_TIMEOUT  # Use the timeout from config
                )
                
                if ollama_response.status_code != 200:
                    error_detail = ollama_response.json() if ollama_response.content else "No error details"
                    print(f"Ollama API error: {ollama_response.status_code} - {error_detail}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Vision model analysis failed: {error_detail}"
                    )
                
                response_data = ollama_response.json()
                if 'response' not in response_data:
                    print(f"Unexpected Ollama response format: {response_data}")
                    raise HTTPException(
                        status_code=500,
                        detail="Invalid response from vision model"
                    )
                
                return response_data['response']
                
            except requests.exceptions.ConnectionError:
                print("Failed to connect to Ollama service")
                raise HTTPException(
                    status_code=503,
                    detail="Vision model service is not available. Please ensure Ollama is running."
                )
            except requests.exceptions.Timeout:
                print("Ollama request timed out")
                raise HTTPException(
                    status_code=504,
                    detail="Vision model analysis timed out"
                )
            
        except HTTPException as he:
            raise he
        except Exception as e:
            print(f"Unexpected error in analyze_image: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error analyzing image: {str(e)}"
            )

    async def analyze_data(self, request: DataAnalysisRequest) -> Dict[str, Any]:
        """Perform data analysis based on provided data and parameters."""
        try:
            df = pd.DataFrame(request.data)
            analysis_results = {}
            
            if request.analysis_type == "statistical":
                analysis_results = {
                    "summary": df.describe().to_dict(),
                    "correlations": df.corr().to_dict(),
                    "missing_values": df.isnull().sum().to_dict()
                }
            elif request.analysis_type == "pattern":
                # Add pattern detection logic
                analysis_results = {
                    "trends": self._detect_trends(df),
                    "outliers": self._detect_outliers(df),
                    "seasonality": self._analyze_seasonality(df)
                }
            elif request.analysis_type == "predictive":
                # Add predictive analysis
                analysis_results = {
                    "forecast": self._generate_forecast(df),
                    "confidence_intervals": self._calculate_confidence(df)
                }
            
            return analysis_results
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error analyzing data: {str(e)}")

    def _detect_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect trends in the data."""
        trends = {}
        for column in df.select_dtypes(include=[np.number]).columns:
            # Calculate rolling mean
            trends[column] = {
                "direction": "increasing" if df[column].diff().mean() > 0 else "decreasing",
                "magnitude": abs(df[column].diff().mean()),
                "volatility": df[column].std()
            }
        return trends

    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect outliers using IQR method."""
        outliers = {}
        for column in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            outliers[column] = {
                "lower_bound": Q1 - 1.5 * IQR,
                "upper_bound": Q3 + 1.5 * IQR,
                "outlier_count": len(df[(df[column] < Q1 - 1.5 * IQR) | (df[column] > Q3 + 1.5 * IQR)])
            }
        return outliers

    def _analyze_seasonality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze seasonality in time series data."""
        seasonality = {}
        for column in df.select_dtypes(include=[np.number]).columns:
            if len(df) >= 4:  # Need at least 4 points for seasonal analysis
                # Calculate basic seasonal patterns
                seasonality[column] = {
                    "quarterly_mean": df[column].groupby(df.index % 4).mean().to_dict(),
                    "has_seasonality": len(df[column].unique()) > len(df[column].groupby(df.index % 4).mean())
                }
        return seasonality

    def _generate_forecast(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate simple forecasts using moving averages."""
        forecast = {}
        for column in df.select_dtypes(include=[np.number]).columns:
            # Calculate moving averages
            ma_7 = df[column].rolling(window=7).mean().iloc[-1]
            ma_30 = df[column].rolling(window=30).mean().iloc[-1]
            forecast[column] = {
                "short_term": ma_7,
                "long_term": ma_30,
                "trend": "up" if ma_7 > ma_30 else "down"
            }
        return forecast

    def _calculate_confidence(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate confidence intervals for predictions."""
        confidence = {}
        for column in df.select_dtypes(include=[np.number]).columns:
            mean = df[column].mean()
            std = df[column].std()
            confidence[column] = {
                "mean": mean,
                "lower_95": mean - 1.96 * std,
                "upper_95": mean + 1.96 * std
            }
        return confidence

# Create global instance
data_detective = DataDetectiveAgent()

# DataDetective endpoints
@app.post("/digital_transform/datadetective/create_chart", response_model=Dict[str, Any])
async def create_chart(request: ChartRequest, api_key: str = Depends(get_api_key)):
    """Create a chart using the DataDetective agent."""
    data_detective.update_api_key(api_key)
    return await data_detective.create_chart(request)

@app.post("/digital_transform/datadetective/analyze_image", response_model=Message)
async def analyze_image(request: ImageAnalysisRequest, api_key: str = Depends(get_api_key)):
    """Analyze a chart or visualization using vision capabilities."""
    data_detective.update_api_key(api_key)
    analysis = await data_detective.analyze_image(request)
    return Message(role="assistant", content=analysis)

@app.post("/digital_transform/datadetective/analyze_data", response_model=Dict[str, Any])
async def analyze_data(request: DataAnalysisRequest, api_key: str = Depends(get_api_key)):
    """Analyze data using the DataDetective agent."""
    data_detective.update_api_key(api_key)
    return await data_detective.analyze_data(request)

@app.post("/digital_transform/datadetective/upload_chart", response_model=Message)
async def upload_chart(
    file: UploadFile = File(...),
    analysis_type: str = Form("general"),
    context: str = Form("{}"),
    api_key: str = Depends(get_api_key)
):
    """Upload and analyze a chart image."""
    try:
        # Update the agent with the provided API key
        data_detective.update_api_key(api_key)
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload an image file."
            )

        # Create temporary file with unique name
        temp_path = f"temp_{int(time.time())}_{file.filename}"
        try:
            # Read file contents
            contents = await file.read()
            
            if not contents:
                raise HTTPException(
                    status_code=400,
                    detail="Empty file uploaded"
                )
            
            # Save temporarily
            with open(temp_path, "wb") as f:
                f.write(contents)
            
            # Analyze using Ollama llava model
            try:
                analysis = await data_detective.analyze_image(ImageAnalysisRequest(
                    image_url=temp_path,
                    analysis_type=analysis_type,
                    context=json.loads(context)
                ))
                
                return Message(role="assistant", content=analysis)
                
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid context JSON format"
                )
            except Exception as e:
                print(f"Error analyzing image: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error analyzing image: {str(e)}"
                )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception as e:
                    print(f"Error removing temporary file: {str(e)}")
                
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Unexpected error in upload_chart: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chart: {str(e)}"
        )

# Architect Agent Class
class ArchitectAgent:
    def __init__(self):
        self.config = load_agent_config('digital_transform_architect')[0]
        self.instructions = load_agent_config('digital_transform_architect')[1]
        self.memory = {}
        self.api_key = None
        self.initialize_components()

    def update_api_key(self, api_key):
        """Update the API key for all components."""
        self.api_key = api_key
        # Update API key for all components
        self.solution_designer = Agent(
            instructions=f"{self.instructions}\nFocus on technical solution design.",
            api_key=api_key
        )
        
        self.security_assessor = Agent(
            instructions=f"{self.instructions}\nFocus on security and compliance.",
            api_key=api_key
        )
        
        self.integration_planner = Agent(
            instructions=f"{self.instructions}\nFocus on system integration and APIs.",
            api_key=api_key
        )
        
        self.performance_optimizer = Agent(
            instructions=f"{self.instructions}\nFocus on scalability and optimization.",
            api_key=api_key
        )

    def initialize_components(self):
        """Initialize specialized components for different architecture tasks."""
        self.solution_designer = Agent(
            instructions=f"{self.instructions}\nFocus on technical solution design."
        )
        
        self.security_assessor = Agent(
            instructions=f"{self.instructions}\nFocus on security and compliance."
        )
        
        self.integration_planner = Agent(
            instructions=f"{self.instructions}\nFocus on system integration and APIs."
        )
        
        self.performance_optimizer = Agent(
            instructions=f"{self.instructions}\nFocus on scalability and optimization."
        )

    async def design_solution(self, requirements: Dict) -> str:
        """Design technical solution based on requirements."""
        try:
            # Create solution design
            solution = self.solution_designer.start(f"""
            Design technical solution based on:
            Requirements: {json.dumps(requirements, indent=2)}
            """)
            
            # Assess security
            security = self.security_assessor.start(f"""
            Assess security implications of:
            Solution: {solution}
            """)
            
            # Plan integrations
            integrations = self.integration_planner.start(f"""
            Plan system integrations for:
            Solution: {solution}
            Security: {security}
            """)
            
            # Optimize performance
            performance = self.performance_optimizer.start(f"""
            Optimize performance for:
            Solution: {solution}
            Integrations: {integrations}
            """)
            
            return f"""
            Technical Solution Design:
            {solution}
            
            Security Assessment:
            {security}
            
            Integration Plan:
            {integrations}
            
            Performance Optimization:
            {performance}
            """
            
        except Exception as e:
            return f"Error designing solution: {str(e)}"

# Designer Agent Class
class DesignerAgent:
    def __init__(self):
        self.config = load_agent_config('digital_transform_designer')[0]
        self.instructions = load_agent_config('digital_transform_designer')[1]
        self.memory = {}
        self.api_key = None
        self.initialize_components()

    def update_api_key(self, api_key):
        """Update the API key for all components."""
        self.api_key = api_key
        # Update API key for all components
        self.ui_designer = Agent(
            instructions=f"{self.instructions}\nFocus on interface design.",
            api_key=api_key
        )
        
        self.flow_designer = Agent(
            instructions=f"{self.instructions}\nFocus on user flow mapping.",
            api_key=api_key
        )
        
        self.accessibility_tester = Agent(
            instructions=f"{self.instructions}\nFocus on accessibility compliance.",
            api_key=api_key
        )

    def initialize_components(self):
        """Initialize specialized components for different design tasks."""
        self.ui_designer = Agent(
            instructions=f"{self.instructions}\nFocus on interface design."
        )
        
        self.flow_designer = Agent(
            instructions=f"{self.instructions}\nFocus on user flow mapping."
        )
        
        self.accessibility_tester = Agent(
            instructions=f"{self.instructions}\nFocus on accessibility compliance."
        )

    async def create_design(self, requirements: Dict) -> str:
        """Create UI/UX design based on requirements."""
        try:
            # Design interface
            interface = self.ui_designer.start(f"""
            Design interface based on:
            Requirements: {json.dumps(requirements, indent=2)}
            """)
            
            # Create user flows
            flows = self.flow_designer.start(f"""
            Create user flows for:
            Interface: {interface}
            """)
            
            # Test accessibility
            accessibility = self.accessibility_tester.start(f"""
            Test accessibility for:
            Interface: {interface}
            Flows: {flows}
            """)
            
            return f"""
            Interface Design:
            {interface}
            
            User Flows:
            {flows}
            
            Accessibility Report:
            {accessibility}
            """
            
        except Exception as e:
            return f"Error creating design: {str(e)}"

# Automator Agent Class
class AutomatorAgent:
    def __init__(self):
        self.config = load_agent_config('digital_transform_automator')[0]
        self.instructions = load_agent_config('digital_transform_automator')[1]
        self.memory = {}
        self.api_key = None
        self.initialize_components()

    def update_api_key(self, api_key):
        """Update the API key for all components."""
        self.api_key = api_key
        # Update API key for all components
        self.workflow_designer = Agent(
            instructions=f"{self.instructions}\nFocus on workflow automation.",
            api_key=api_key
        )
        
        self.integration_builder = Agent(
            instructions=f"{self.instructions}\nFocus on system integration.",
            api_key=api_key
        )
        
        self.test_creator = Agent(
            instructions=f"{self.instructions}\nFocus on automated testing.",
            api_key=api_key
        )

    def initialize_components(self):
        """Initialize specialized components for different automation tasks."""
        self.workflow_designer = Agent(
            instructions=f"{self.instructions}\nFocus on workflow automation."
        )
        
        self.integration_builder = Agent(
            instructions=f"{self.instructions}\nFocus on system integration."
        )
        
        self.test_creator = Agent(
            instructions=f"{self.instructions}\nFocus on automated testing."
        )

    async def create_automation(self, requirements: Dict) -> str:
        """Create automation solution based on requirements."""
        try:
            # Design workflows
            workflows = self.workflow_designer.start(f"""
            Design automation workflows based on:
            Requirements: {json.dumps(requirements, indent=2)}
            """)
            
            # Build integrations
            integrations = self.integration_builder.start(f"""
            Create system integrations for:
            Workflows: {workflows}
            """)
            
            # Create tests
            tests = self.test_creator.start(f"""
            Create automated tests for:
            Workflows: {workflows}
            Integrations: {integrations}
            """)
            
            return f"""
            Automation Workflows:
            {workflows}
            
            System Integrations:
            {integrations}
            
            Automated Tests:
            {tests}
            """
            
        except Exception as e:
            return f"Error creating automation: {str(e)}"

# Trainer Agent Class
class TrainerAgent:
    def __init__(self):
        self.config = load_agent_config('digital_transform_trainer')[0]
        self.instructions = load_agent_config('digital_transform_trainer')[1]
        self.memory = {}
        self.api_key = None
        self.initialize_components()

    def update_api_key(self, api_key):
        """Update the API key for all components."""
        self.api_key = api_key
        # Update API key for all components
        self.program_designer = Agent(
            instructions=f"{self.instructions}\nFocus on training program design.",
            api_key=api_key
        )
        
        self.content_creator = Agent(
            instructions=f"{self.instructions}\nFocus on content creation.",
            api_key=api_key
        )
        
        self.assessment_builder = Agent(
            instructions=f"{self.instructions}\nFocus on skill assessment.",
            api_key=api_key
        )

    def initialize_components(self):
        """Initialize specialized components for different training tasks."""
        self.program_designer = Agent(
            instructions=f"{self.instructions}\nFocus on training program design."
        )
        
        self.content_creator = Agent(
            instructions=f"{self.instructions}\nFocus on content creation."
        )
        
        self.assessment_builder = Agent(
            instructions=f"{self.instructions}\nFocus on skill assessment."
        )

    async def create_training(self, requirements: Dict) -> str:
        """Create training program based on requirements."""
        try:
            # Design program
            program = self.program_designer.start(f"""
            Design training program based on:
            Requirements: {json.dumps(requirements, indent=2)}
            """)
            
            # Create content
            content = self.content_creator.start(f"""
            Create training content for:
            Program: {program}
            """)
            
            # Build assessments
            assessments = self.assessment_builder.start(f"""
            Create skill assessments for:
            Program: {program}
            Content: {content}
            """)
            
            return f"""
            Training Program:
            {program}
            
            Training Content:
            {content}
            
            Skill Assessments:
            {assessments}
            """
            
        except Exception as e:
            return f"Error creating training: {str(e)}"

# Measurer Agent Class
class MeasurerAgent:
    def __init__(self):
        self.config = load_agent_config('digital_transform_measurer')[0]
        self.instructions = load_agent_config('digital_transform_measurer')[1]
        self.memory = {}
        self.api_key = None
        self.initialize_components()

    def update_api_key(self, api_key):
        """Update the API key for all components."""
        self.api_key = api_key
        # Update API key for all components
        self.kpi_analyzer = Agent(
            instructions=f"{self.instructions}\nFocus on KPI analysis.",
            api_key=api_key
        )
        
        self.roi_calculator = Agent(
            instructions=f"{self.instructions}\nFocus on ROI calculation.",
            api_key=api_key
        )
        
        self.impact_assessor = Agent(
            instructions=f"{self.instructions}\nFocus on impact assessment.",
            api_key=api_key
        )

    def initialize_components(self):
        """Initialize specialized components for different measurement tasks."""
        self.kpi_analyzer = Agent(
            instructions=f"{self.instructions}\nFocus on KPI analysis."
        )
        
        self.roi_calculator = Agent(
            instructions=f"{self.instructions}\nFocus on ROI calculation."
        )
        
        self.impact_assessor = Agent(
            instructions=f"{self.instructions}\nFocus on impact assessment."
        )

    async def analyze_metrics(self, data: Dict) -> str:
        """Analyze metrics and calculate ROI."""
        try:
            # Analyze KPIs
            kpis = self.kpi_analyzer.start(f"""
            Analyze KPIs based on:
            Data: {json.dumps(data, indent=2)}
            """)
            
            # Calculate ROI
            roi = self.roi_calculator.start(f"""
            Calculate ROI based on:
            KPIs: {kpis}
            """)
            
            # Assess impact
            impact = self.impact_assessor.start(f"""
            Assess impact based on:
            KPIs: {kpis}
            ROI: {roi}
            """)
            
            return f"""
            KPI Analysis:
            {kpis}
            
            ROI Calculation:
            {roi}
            
            Impact Assessment:
            {impact}
            """
            
        except Exception as e:
            return f"Error analyzing metrics: {str(e)}"

# Create global instances
architect_agent = ArchitectAgent()
designer_agent = DesignerAgent()
automator_agent = AutomatorAgent()
trainer_agent = TrainerAgent()
measurer_agent = MeasurerAgent()

# Add new request models
class ArchitectRequest(BaseModel):
    solution_requirements: Dict[str, Any]

class DesignerRequest(BaseModel):
    design_requirements: Dict[str, Any]

class AutomatorRequest(BaseModel):
    automation_requirements: Dict[str, Any]

class TrainerRequest(BaseModel):
    training_requirements: Dict[str, Any]

class MeasurerRequest(BaseModel):
    metric_data: Dict[str, Any]

# Add new endpoints
@app.post("/digital_transform/architect/design", response_model=Message)
async def design_solution(request: ArchitectRequest, api_key: str = Depends(get_api_key)):
    """Design technical solution using the Architect agent."""
    architect_agent.update_api_key(api_key)
    solution = await architect_agent.design_solution(request.solution_requirements)
    return Message(role="assistant", content=solution)

@app.post("/digital_transform/designer/create", response_model=Message)
async def create_design(request: DesignerRequest, api_key: str = Depends(get_api_key)):
    """Create UI/UX design using the Designer agent."""
    designer_agent.update_api_key(api_key)
    design = await designer_agent.create_design(request.design_requirements)
    return Message(role="assistant", content=design)

@app.post("/digital_transform/automator/create", response_model=Message)
async def create_automation(request: AutomatorRequest, api_key: str = Depends(get_api_key)):
    """Create automation solution using the Automator agent."""
    automator_agent.update_api_key(api_key)
    automation = await automator_agent.create_automation(request.automation_requirements)
    return Message(role="assistant", content=automation)

@app.post("/digital_transform/trainer/create", response_model=Message)
async def create_training(request: TrainerRequest, api_key: str = Depends(get_api_key)):
    """Create training program using the Trainer agent."""
    trainer_agent.update_api_key(api_key)
    training = await trainer_agent.create_training(request.training_requirements)
    return Message(role="assistant", content=training)

@app.post("/digital_transform/measurer/analyze", response_model=Message)
async def analyze_metrics(request: MeasurerRequest, api_key: str = Depends(get_api_key)):
    """Analyze metrics using the Measurer agent."""
    measurer_agent.update_api_key(api_key)
    analysis = await measurer_agent.analyze_metrics(request.metric_data)
    return Message(role="assistant", content=analysis)

# Add response compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add MongoDB configuration
MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'juici_agents')

# Initialize MongoDB client
try:
    mongodb_client = AsyncIOMotorClient(MONGODB_URL)
    mongodb_db = mongodb_client[MONGODB_DB]
except Exception as e:
    print(f"Warning: MongoDB connection failed - {str(e)}")
    mongodb_client = None
    mongodb_db = None

# Add connection pooling for database operations
async def get_db_pool():
    """Get MongoDB connection pool."""
    try:
        return AsyncIOMotorClient(
            MONGODB_URL,
            maxPoolSize=50,
            minPoolSize=10,
            serverSelectionTimeoutMS=5000
        )
    except Exception as e:
        print(f"Warning: Failed to create MongoDB pool - {str(e)}")
        return None

# Initialize connection pools
http_session = aiohttp.ClientSession()
db_pool = None

@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup."""
    global db_pool
    try:
        db_pool = await get_db_pool()
        if db_pool:
            # Test connection
            await db_pool.server_info()
            print("MongoDB connection successful")
    except Exception as e:
        print(f"Warning: MongoDB startup connection failed - {str(e)}")
        db_pool = None

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up connections on shutdown."""
    await http_session.close()
    if db_pool:
        db_pool.close()

# Add request batching for efficiency
class BatchProcessor:
    def __init__(self, batch_size=10, timeout=0.1):
        self.batch_size = batch_size
        self.timeout = timeout
        self.batch = []
        self.batch_lock = asyncio.Lock()
        self.processing = False

    async def add_request(self, request):
        async with self.batch_lock:
            self.batch.append(request)
            if len(self.batch) >= self.batch_size and not self.processing:
                await self.process_batch()

    async def process_batch(self):
        self.processing = True
        try:
            batch = self.batch.copy()
            self.batch.clear()
            
            # Process requests in parallel
            tasks = [thread_pool.submit(process_request, req) for req in batch]
            return await asyncio.gather(*tasks)
        finally:
            self.processing = False

batch_processor = BatchProcessor()

# Add memory management
def optimize_memory():
    """Optimize memory usage periodically"""
    gc.collect()
    process = psutil.Process(os.getpid())
    if process.memory_percent() > 80:  # If memory usage is high
        gc.collect()
        if hasattr(torch, 'cuda'):
            torch.cuda.empty_cache()  # Clear GPU memory if available

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 