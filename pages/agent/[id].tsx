import { useRouter } from 'next/router';
import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import Head from 'next/head';

interface Message {
  role: string;
  content: string;
  id: number;
}

export default function AgentPage() {
  const router = useRouter();
  const { id } = router.query;
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [agentName, setAgentName] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (id && typeof id === 'string') {
      // Format the agent name from the ID
      const formattedName = id
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
      setAgentName(formattedName);
    }
  }, [id]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input, id: Date.now() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          agent_name: id,
          message: input
        }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      setMessages(prev => [...prev, data]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, there was an error processing your request. Please try again.',
        id: Date.now()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const userMessage = { 
      role: 'user', 
      content: `[Uploaded an image: ${file.name}]`, 
      id: Date.now() 
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('image', file);
      if (id && typeof id === 'string') {
        formData.append('agent_name', id);
      }

      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      setMessages(prev => [...prev, data]);
    } catch (error) {
      console.error('Error uploading file:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, there was an error processing your image. Please try again.',
        id: Date.now()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      <Head>
        <title>{agentName || 'Agent'} | Juici Agents</title>
        <meta name="description" content={`Chat with ${agentName || 'our AI agent'}`} />
      </Head>
      
      <header className="bg-gray-800 p-4 shadow-md">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-purple-500">{agentName || 'Agent'}</h1>
          <Link href="/">
            <span className="bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 rounded">
              Back to Agents
            </span>
          </Link>
        </div>
      </header>
      
      <div className="flex-1 container mx-auto p-4 flex flex-col">
        <div className="flex-1 bg-gray-800 rounded-lg p-4 mb-4 overflow-y-auto max-h-[calc(100vh-250px)]">
          {messages.length === 0 ? (
            <div className="text-center text-gray-400 my-20">
              <p className="text-xl mb-2">Start a conversation with {agentName || 'the agent'}</p>
              <p>Ask a question or upload an image to analyze</p>
            </div>
          ) : (
            messages.map(message => (
              <div 
                key={message.id} 
                className={`mb-4 p-3 rounded-lg ${
                  message.role === 'user' 
                    ? 'bg-purple-900 ml-auto max-w-3xl' 
                    : 'bg-gray-700 mr-auto max-w-3xl'
                }`}
              >
                <p className="text-sm font-semibold mb-1">
                  {message.role === 'user' ? 'You' : agentName || 'Agent'}
                </p>
                <div className="prose prose-invert">
                  {message.content}
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
        
        <div className="bg-gray-800 rounded-lg p-4">
          <form onSubmit={handleSubmit} className="flex flex-col space-y-2">
            <div className="flex items-center">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message here..."
                className="flex-1 bg-gray-700 text-white rounded-lg p-2 outline-none focus:ring-2 focus:ring-purple-500"
                rows={2}
                disabled={isLoading}
              />
              <label className="ml-2 bg-teal-600 hover:bg-teal-700 text-white p-2 rounded-lg cursor-pointer">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <input 
                  type="file" 
                  className="hidden" 
                  accept="image/*" 
                  onChange={handleFileUpload}
                  disabled={isLoading}
                />
              </label>
              <button
                type="submit"
                className="ml-2 bg-purple-600 hover:bg-purple-700 text-white p-2 rounded-lg disabled:opacity-50"
                disabled={isLoading || !input.trim()}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
} 