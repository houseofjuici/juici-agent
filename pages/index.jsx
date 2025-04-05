import { useState, useEffect } from 'react';
import Link from 'next/link';
import Head from 'next/head';

export default function Home() {
  const [agents, setAgents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchAgents() {
      try {
        const response = await fetch('/api/agents');
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
        setAgents(data.agents || []);
      } catch (error) {
        console.error('Error fetching agents:', error);
        setError('Failed to load agents. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    }

    fetchAgents();
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Head>
        <title>Juici Agents</title>
        <meta name="description" content="AI-powered agents for various tasks" />
      </Head>

      <div className="container mx-auto px-4 py-8">
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-bold mb-4 text-purple-500">Juici Agents</h1>
          <p className="text-xl text-gray-300">Specialized AI agents for your unique needs</p>
        </header>

        {isLoading ? (
          <div className="flex justify-center">
            <div className="animate-pulse text-center">
              <p className="text-xl">Loading agents...</p>
            </div>
          </div>
        ) : error ? (
          <div className="bg-red-900 p-4 rounded-lg text-center">
            <p>{error}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent) => (
              <Link 
                href={`/agent/${agent.id}`} 
                key={agent.id}
                className="block"
              >
                <div className="bg-gray-800 rounded-lg p-6 h-full border-2 border-transparent hover:border-teal-500 transition-all duration-300">
                  <h2 className="text-2xl font-bold mb-2 text-teal-500">{agent.name}</h2>
                  <p className="text-gray-300 mb-4">{agent.description}</p>
                  <div className="mt-auto pt-4">
                    <span className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded inline-flex items-center">
                      Chat with Agent
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                      </svg>
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
} 