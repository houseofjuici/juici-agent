// Serverless function for file upload API
import { IncomingForm } from 'formidable';
import { promises as fs } from 'fs';
import os from 'os';
import path from 'path';

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req, res) {
  try {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
      return res.status(200).end();
    }
    
    if (req.method !== 'POST') {
      return res.status(405).json({ error: 'Method not allowed' });
    }
    
    // In a Vercel environment, we'll send a mock response for image uploads
    const mockResponse = {
      role: 'assistant',
      content: `# Chart Analysis

This appears to be a chart image. Here's my analysis:

## Key Observations:
- The chart shows a clear trend in the data
- There are notable patterns that indicate important business insights
- The visualization effectively communicates the intended data relationships

## Insights:
1. The data shows important correlations between key metrics
2. The overall trend suggests positive growth in the measured variables
3. There are some outliers that warrant further investigation

## Recommendations:
- Consider adding more data points to strengthen the analysis
- Use a logarithmic scale for better visualization of the full data range
- Add annotations to highlight key inflection points

*This is a demonstration response in the Vercel environment.*`,
    };
    
    // Simulate a delay to mimic processing time
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return res.status(200).json(mockResponse);
  } catch (error) {
    console.error('Error in upload API:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
} 