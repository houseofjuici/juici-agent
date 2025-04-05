import os
import pytest
from dotenv import load_dotenv
from praisonaiagents import Agent
from run_agent import validate_input, RateLimiter

@pytest.fixture(autouse=True)
def setup_env():
    """Load environment variables and check for API key."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        pytest.skip("OPENAI_API_KEY not set or invalid")

@pytest.fixture
def agent():
    """Create a test agent instance."""
    return Agent(instructions="You are a fitness coach.")

def test_input_validation():
    """Test input validation security measures."""
    # Test valid inputs
    assert validate_input("Valid input") is True
    assert validate_input("Another valid input") is True
    
    # Test invalid inputs
    assert validate_input("") is False
    assert validate_input(" " * 1001) is False  # Too long
    assert validate_input("<script>alert('xss')</script>") is False  # Contains harmful characters
    assert validate_input("{}[]()") is False  # Contains harmful characters

def test_rate_limiting():
    """Test rate limiting functionality."""
    limiter = RateLimiter()
    user_id = "test_user"
    
    # Test within rate limit
    for _ in range(5):
        assert limiter.is_allowed(user_id) is True
    
    # Test exceeding rate limit
    assert limiter.is_allowed(user_id) is False

def test_workout_plan_generation(agent):
    """Test workout plan generation."""
    response = agent.start("Create a workout plan for a beginner with goals: strength training. Available equipment: bodyweight only")
    assert response is not None
    assert len(response) > 0
    assert "workout" in response.lower()
    # Check for any workout-related terms
    assert any(term in response.lower() for term in [
        "exercise",
        "training",
        "sets",
        "reps",
        "routine",
        "movement"
    ])

def test_nutrition_advice(agent):
    """Test nutrition advice generation."""
    response = agent.start("Provide nutrition advice for someone with no dietary restrictions and goals: muscle gain")
    assert response is not None
    assert len(response) > 0
    assert "nutrition" in response.lower()
    assert "diet" in response.lower()

def test_exercise_form_guidance(agent):
    """Test exercise form guidance."""
    response = agent.start("Guide proper form for squats for someone with beginner experience")
    assert response is not None
    assert len(response) > 0
    assert "form" in response.lower()
    # Check for alternative terms that indicate proper form guidance
    assert any(term in response.lower() for term in [
        "technique",
        "position",
        "stance",
        "posture",
        "alignment",
        "movement",
        "execution",
        "proper"
    ])

def test_progress_tracking(agent):
    """Test progress tracking functionality."""
    response = agent.start("Track progress for someone who has been working out for 3 months with goals: weight loss")
    assert response is not None
    assert len(response) > 0
    assert "progress" in response.lower()
    assert "track" in response.lower()

def test_safety_considerations(agent):
    """Test inclusion of safety considerations."""
    response = agent.start("Create a workout plan for a beginner with goals: strength training")
    assert response is not None
    assert any(term in response.lower() for term in [
        "safety",
        "warm-up",
        "cool-down",
        "rest",
        "recovery"
    ])

def test_personalization(agent):
    """Test personalization of recommendations."""
    response = agent.start("Create a workout plan for an advanced athlete with goals: endurance. Available equipment: full gym")
    assert response is not None
    assert len(response) > 0
    # Check for advanced-level terminology
    assert any(term in response.lower() for term in [
        "advanced",
        "intensity",
        "progression",
        "periodization"
    ])

def test_error_handling(agent):
    """Test error handling and response validation."""
    # Test with invalid input
    response = agent.start("")
    assert response is not None
    assert len(response) > 0
    
    # Test with very long input
    long_input = "test " * 1000
    response = agent.start(long_input)
    assert response is not None
    assert len(response) > 0 