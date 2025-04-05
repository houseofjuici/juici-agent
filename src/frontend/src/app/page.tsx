'use client';

import { useState, useEffect } from 'react';
import AgentSidebar from '@/components/AgentSidebar';
import ChatInterface from '@/components/ChatInterface';
import QuickStart from '@/components/QuickStart';
import { AgentInfo } from '@/types/agent';
import { Message } from '@/types/chat';

export default function Home() {
  const [agents, setAgents] = useState<AgentInfo[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Fetch available agents on component mount
    const fetchAgents = async () => {
      try {
        setIsLoading(true);
        // Use relative URL that will be handled by Vercel's rewrites
        const response = await fetch('/api/agents');
        if (!response.ok) {
          throw new Error('Failed to fetch agents');
        }
        const agentNames = await response.json();
        
        // For Vercel deployment, we'll use mock agent details
        const agentDetails = agentNames.map((name: string) => ({
          config: {
            name,
            description: `${name.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')} Agent`,
            version: '1.0.0'
          },
          example_prompts: [
            `Example prompt for ${name}`,
            `Another example for ${name}`
          ]
        }));
        
        setAgents(agentDetails);
        setError(null);
      } catch (error) {
        console.error('Failed to fetch agents:', error);
        setError('Failed to load agents. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAgents();
  }, []);

  const handleSelectAgent = (agentName: string) => {
    console.log('Selected agent:', agentName); // Debug log
    setSelectedAgent(agentName);
    setMessages([]);
    setError(null);
  };

  const handleSendMessage = async (message: string | File) => {
    if (!selectedAgent) return;

    setIsLoading(true);
    setError(null);
    setMessages((prev) => [...prev, { role: 'user', content: message instanceof File ? `Uploading image: ${message.name}` : message }]);

    try {
      let response;
      
      if (message instanceof File) {
        // Handle file upload
        const formData = new FormData();
        formData.append('file', message);
        formData.append('analysis_type', 'general');
        formData.append('context', '{}');

        response = await fetch('/api/upload', {
          method: 'POST',
          body: formData
        });
      } else {
        // Handle text message
        response = await fetch('/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            agent_name: selectedAgent,
            message: message
          }),
        });
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to send message');
      }

      if (response.headers.get('content-type')?.includes('text/event-stream')) {
        // Handle streaming response
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (reader) {
          let accumulatedContent = '';
          const messageId = Date.now();
          setMessages((prev) => [...prev, { role: 'assistant', content: '', id: messageId }]);

          while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            accumulatedContent += chunk;

            setMessages((prev) =>
              prev.map(msg =>
                msg.id === messageId
                  ? { ...msg, content: accumulatedContent }
                  : msg
              )
            );
          }
        }
      } else {
        // Handle regular JSON response
        const data = await response.json();
        setMessages((prev) => [...prev, { role: 'assistant', content: data.content }]);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      setError('Failed to send message');
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading && agents.length === 0) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#6A1B9A] mx-auto mb-4"></div>
          <p className="text-gray-600 font-manrope font-light">Loading agents...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-100">
      <AgentSidebar
        agents={agents}
        selectedAgent={selectedAgent}
        onSelectAgent={handleSelectAgent}
      />
      
      <main className="flex-1 p-4 overflow-hidden">
        {error && (
          <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}
        
        {selectedAgent ? (
          <ChatInterface
            agentName={selectedAgent}
            onSendMessage={handleSendMessage}
            messages={messages}
            isLoading={isLoading}
            examplePrompts={agents.find(a => a.config.name === selectedAgent)?.example_prompts || []}
          />
        ) : (
          <QuickStart />
        )}
      </main>
    </div>
  );
} 