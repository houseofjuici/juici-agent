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
      {
        id: 'digital_transform_analyst',
        name: 'Digital Transform Analyst',
        description: 'Analyzes your digital transformation needs'
      },
      {
        id: 'digital_transform_architect',
        name: 'Digital Transform Architect',
        description: 'Designs your digital transformation strategy'
      },
      {
        id: 'digital_transform_automator',
        name: 'Digital Transform Automator',
        description: 'Automates processes for digital transformation'
      }, 
      {
        id: 'digital_transform_designer',
        name: 'Digital Transform Designer',
        description: 'Creates designs for your digital interfaces'
      },
      {
        id: 'digital_transform_trainer',
        name: 'Digital Transform Trainer',
        description: 'Trains your team on digital transformation'
      },
      {
        id: 'digital_transform_measurer',
        name: 'Digital Transform Measurer',
        description: 'Measures the impact of digital transformation'
      },
      {
        id: 'blogsmith',
        name: 'BlogSmith',
        description: 'Creates engaging blog content'
      },
      {
        id: 'contractcopilot',
        name: 'ContractCopilot',
        description: 'Assists with contract analysis and creation'
      },
      {
        id: 'fitcoachai',
        name: 'FitCoachAI',
        description: 'Your personal AI fitness coach'
      },
      {
        id: 'funnelbot',
        name: 'FunnelBot',
        description: 'Optimizes your marketing funnels'
      }
    ];
    
    return res.status(200).json({ agents });
  } catch (error) {
    console.error('Error in agents API:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
} 