// Serverless function to list available agents
import fs from 'fs';
import path from 'path';

export default async function handler(req, res) {
  try {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
      return res.status(200).end();
    }
    
    if (req.method !== 'GET') {
      return res.status(405).json({ error: 'Method not allowed' });
    }
    
    // This is a mock list since we can't scan directories in Vercel functions
    const agents = [
      'digital_transform_analyst',
      'digital_transform_architect',
      'digital_transform_automator', 
      'digital_transform_designer',
      'digital_transform_trainer',
      'digital_transform_measurer',

      'blogsmith',
      'contractcopilot',
      'fitcoachai',
      'funnelbot'
    ];
    
    return res.status(200).json(agents);
  } catch (error) {
    console.error('Error in agents API:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
} 