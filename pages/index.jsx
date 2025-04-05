import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Head from 'next/head';
import { getApiUrl } from '../lib/config';

export default function Home() {
  const [agents, setAgents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [keyStatus, setKeyStatus] = useState('');

  useEffect(() => {
    // Load API key from localStorage
    const savedApiKey = localStorage.getItem('openai_api_key');
    if (savedApiKey) {
      setApiKey(savedApiKey);
      setKeyStatus('API key loaded from storage');
    }

    async function fetchAgents() {
      try {
        // Use the configuration helper to get the proper API URL
        const response = await fetch(getApiUrl('agents'));
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
        setAgents(data.agents || []);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching agents:', error);
        setError('Failed to load agents. Please try again later.');
        setIsLoading(false);
      }
    }

    fetchAgents();
  }, []);

  const saveApiKey = () => {
    if (!apiKey.trim()) {
      setKeyStatus('Please enter a valid API key');
      return;
    }

    setIsSaving(true);
    
    // Store in localStorage
    localStorage.setItem('openai_api_key', apiKey.trim());
    
    // Simulate a brief loading state
    setTimeout(() => {
      setIsSaving(false);
      setKeyStatus('API key saved successfully');
    }, 500);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Head>
        <title>Juici Agents</title>
        <meta name="description" content="AI-powered agents for various tasks" />
      </Head>

      <div className="container mx-auto px-4 py-8">
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-bold mb-4" style={{ color: '#6A1B9A' }}>Juici Agents</h1>
          <p className="text-xl text-gray-300">Specialized AI agents for your unique needs</p>
        </header>

        {/* API Key Input Section */}
        <div className="mb-8 max-w-xl mx-auto">
          <div style={{ 
            backgroundColor: '#222', 
            padding: '24px', 
            borderRadius: '8px',
            marginBottom: '24px'
          }}>
            <h2 className="text-xl font-bold mb-3">Enter Your OpenAI API Key</h2>
            <p className="text-gray-300 mb-4">Your API key is stored locally in your browser and is never sent to our servers.</p>
            
            <div className="flex mb-2">
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="sk-..."
                className="flex-1 p-2 rounded-l text-gray-900"
              />
              <button
                onClick={saveApiKey}
                disabled={isSaving}
                style={{ 
                  backgroundColor: '#6A1B9A',
                  padding: '8px 16px',
                  borderRadius: '0 4px 4px 0',
                  cursor: isSaving ? 'not-allowed' : 'pointer'
                }}
              >
                {isSaving ? 'Saving...' : 'Save Key'}
              </button>
            </div>
            
            {keyStatus && (
              <p className="text-sm mt-2" style={{ color: keyStatus.includes('success') ? '#4caf50' : '#f44336' }}>
                {keyStatus}
              </p>
            )}
          </div>
        </div>

        {isLoading ? (
          <div className="text-center">
            <p className="mb-8">Loading Juici Agents...</p>
          </div>
        ) : error ? (
          <div className="text-center" style={{ backgroundColor: '#8B0000', padding: '16px', borderRadius: '8px' }}>
            <p>{error}</p>
            <div className="mt-8">
              <Link href="/agent/digital_transform_analyst">
                <span style={{ backgroundColor: '#6A1B9A', color: 'white', padding: '12px 24px', borderRadius: '8px', cursor: 'pointer' }}>
                  Try Digital Transform Analyst
                </span>
              </Link>
            </div>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '24px' }}>
            {agents && agents.length > 0 ? (
              agents.map((agent) => (
                <Link href={`/agent/${agent.id}`} key={agent.id}>
                  <div style={{ 
                    backgroundColor: '#222', 
                    padding: '24px', 
                    borderRadius: '8px', 
                    borderWidth: '2px',
                    borderColor: 'transparent',
                    transition: 'border-color 0.3s',
                    height: '100%',
                    cursor: 'pointer'
                  }}>
                    <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '8px', color: '#00897B' }}>
                      {agent.name}
                    </h2>
                    <p style={{ color: '#ccc', marginBottom: '16px' }}>{agent.description}</p>
                    <div style={{ marginTop: 'auto', paddingTop: '16px' }}>
                      <span style={{ 
                        backgroundColor: '#6A1B9A', 
                        color: 'white', 
                        padding: '8px 16px', 
                        borderRadius: '4px', 
                        display: 'inline-flex',
                        alignItems: 'center'
                      }}>
                        Chat with Agent
                      </span>
                    </div>
                  </div>
                </Link>
              ))
            ) : (
              <div className="text-center col-span-full">
                <p className="mb-8">No agents available. Try again later.</p>
                <div className="mt-8">
                  <Link href="/agent/digital_transform_analyst">
                    <span style={{ backgroundColor: '#6A1B9A', color: 'white', padding: '12px 24px', borderRadius: '8px', cursor: 'pointer' }}>
                      Try Digital Transform Analyst
                    </span>
                  </Link>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
} 