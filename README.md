# Juici Agents

A collection of pre-built AI agents powered by PraisonAI, designed to demonstrate various AI capabilities and serve as live demos for Embassai Toolkit's CLI/API.

## Available Agents

- **BlogSmith** - AI-powered content creator for generating high-quality blog posts
- **ContractCopilot** - Legal assistant for contract analysis and generation
- **FunnelBot** - Marketing copy generator for sales funnels
- **FitCoachAI** - Personalized fitness planning assistant

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/juici-agents.git
cd juici-agents
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run an agent:
```bash
cd BlogSmith
python run_agent.py
```

## Agent Structure

Each agent follows this structure:
```
AgentName/
├── agent_config.json    # Agent configuration
├── prompt.yaml         # Agent instructions
├── run_agent.py        # Main agent implementation
└── test_agent.py       # Test suite
```

## Testing

Run tests for a specific agent:
```bash
cd AgentName
pytest test_agent.py
```

## Integration with Embassai Toolkit

All agents are compatible with Embassai Toolkit's compression and audit features:

```bash
# Compress agent output
embassai compress --text "agent reply"

# Audit agent performance
embassai audit --agent BlogSmith
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 