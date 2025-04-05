// API route for handling chat messages
export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  // Handle OPTIONS request for CORS preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }

  try {
    const { agent_name, message } = req.body;

    // Validate input
    if (!agent_name || !message) {
      return res.status(400).json({ 
        error: 'Missing required parameters. Please provide agent_name and message.' 
      });
    }

    // In a real application, this is where you would:
    // 1. Call your AI service (OpenAI, Anthropic, etc.)
    // 2. Process the response
    // 3. Store the conversation in a database
    
    // For now, we'll return a mock response
    const mockResponses = {
      'digital_transform_analyst': `As a Digital Transform Analyst, I can help with your query: "${message}". \n\nDigital transformation involves integrating digital technology into all areas of your business. I recommend starting with a thorough assessment of your current digital capabilities and creating a roadmap for implementation.`,
      'content_creator': `Thanks for your message: "${message}". \n\nAs your Content Creator, I can develop engaging content tailored to your target audience. Let's start by defining your content goals and the platforms you want to focus on.`,
      'data_analyst': `Regarding your question: "${message}". \n\nAs a Data Analyst, I recommend we begin by identifying the key metrics and data sources relevant to your objectives. This will allow us to create meaningful visualizations and extract actionable insights.`
    };

    // Generate response based on agent type
    const responseContent = mockResponses[agent_name] || 
      `Thank you for your message: "${message}". \n\nI'm processing your request and will assist you shortly.`;
    
    // Small delay to simulate processing time
    await new Promise(resolve => setTimeout(resolve, 500));

    // Return the response
    return res.status(200).json({
      role: 'assistant',
      content: responseContent,
      id: Date.now()
    });
    
  } catch (error) {
    console.error('Error in chat API:', error);
    return res.status(500).json({ 
      role: 'assistant',
      content: 'Sorry, I encountered an error processing your request.',
      id: Date.now()
    });
  }
} 