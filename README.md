# Juici Agents

A Next.js application for AI-powered agent interactions.

## Getting Started

First, set up the environment variables:

1. Copy `.env.local.example` to `.env.local` and adjust the values if needed:
   ```
   NEXT_PUBLIC_API_URL=https://juici-sandbox.vercel.app
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn
   ```

3. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## OpenAI API Key

This application allows users to provide their own OpenAI API key, which is stored locally in the browser:

1. Enter your OpenAI API key on the home page
2. The key is securely stored in your browser's localStorage
3. Your API key is never stored on our servers
4. The key is sent with each API request to authenticate with OpenAI

This approach allows you to use the application without sharing your API key with our servers and gives you control over your API usage and billing.

## Deployment to Vercel

This project is deployed on Vercel at [https://juici-sandbox.vercel.app](https://juici-sandbox.vercel.app).

To deploy your own version:

1. Push your repository to GitHub.
2. Connect your repository to Vercel.
3. No additional environment variables are required for basic deployment, as the application automatically detects Vercel URLs.
4. For custom domain deployments, set the `NEXT_PUBLIC_API_URL` environment variable in Vercel's project settings.

## API Endpoints

- `/api/agents` - Returns the list of available agents
- `/api/chat` - Handles chat interactions with agents
- `/api/upload` - Handles file uploads for agent analysis

## Development Notes

- The application automatically handles API URLs between development and production environments.
- All API endpoints include proper CORS headers for cross-origin requests.
- When deploying to Vercel, the app uses the Vercel URL or custom domain appropriately.

## Project Structure

- `/pages` - Next.js pages and API routes
- `/public` - Static assets 
- `/lib` - Utility functions and configuration
- `/components` - React components (if any)

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