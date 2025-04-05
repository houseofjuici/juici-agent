import { useState, useRef, useEffect } from 'react';
import { Message } from '@/types/chat';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { ReactNode } from 'react';

interface ChatInterfaceProps {
  agentName: string;
  onSendMessage: (message: string | File) => Promise<void>;
  messages: Message[];
  isLoading: boolean;
  examplePrompts: string[];
}

interface CodeProps {
  node?: any;
  inline?: boolean;
  className?: string;
  children: ReactNode;
  [key: string]: any;
}

interface ChildProps {
  children: ReactNode;
}

// Add new LoadingSpinner component
const LoadingSpinner = () => (
  <div className="flex justify-start">
    <div className="bg-[#e0f2f1] rounded-lg p-4">
      <div className="w-8 h-8 relative">
        <div className="absolute w-full h-full border-4 border-[#6A1B9A] border-t-[#00897B] rounded-full animate-spin"></div>
      </div>
    </div>
  </div>
);

// Add new component for formatted message content
const FormattedMessage = ({ content }: { content: string }) => {
  // Function to process content sections
  const processContent = (text: string) => {
    // Split into major sections by double newlines
    const sections = text.split('\n\n').filter(s => s.trim());
    
    return sections.map((section, index) => {
      // Check if section is a header (all caps followed by colon)
      if (section.trim().match(/^[A-Z][A-Z\s]+:/)) {
        const [header, ...content] = section.split(':');
        return (
          <div key={index} className="mb-6">
            <div className="text-[#6A1B9A] font-bold font-mono mb-2">
              {header.trim()}:
            </div>
            <div className="pl-4 font-mono">
              {content.join(':').trim().split('\n').map((line, i) => {
                // Check if line is a list item
                if (line.trim().startsWith('-') || line.trim().startsWith('*')) {
                  return (
                    <div key={i} className="flex items-start mb-1">
                      <span className="text-[#00897B] mr-2">•</span>
                      <span>{line.trim().replace(/^[-*]\s*/, '')}</span>
                    </div>
                  );
                }
                // Regular line
                return (
                  <div key={i} className="mb-1">
                    {line.trim()}
                  </div>
                );
              })}
            </div>
          </div>
        );
      }

      // Check if section is a list
      if (section.trim().match(/^[-*]\s/m)) {
        return (
          <div key={index} className="mb-4 pl-4 font-mono">
            {section.trim().split('\n').map((line, i) => (
              <div key={i} className="flex items-start mb-1">
                <span className="text-[#00897B] mr-2">•</span>
                <span>{line.trim().replace(/^[-*]\s*/, '')}</span>
              </div>
            ))}
          </div>
        );
      }

      // Regular content
      return (
        <div key={index} className="mb-4 font-mono">
          {section.split('\n').map((line, i) => (
            <div key={i} className="mb-1">
              {line.trim()}
            </div>
          ))}
        </div>
      );
    });
  };

  return (
    <div className="bg-white p-4 rounded-lg">
      {processContent(content)}
    </div>
  );
};

export default function ChatInterface({ agentName, onSendMessage, messages, isLoading, examplePrompts }: ChatInterfaceProps) {
  const [input, setInput] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messageContainerRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [autoScroll, setAutoScroll] = useState(true);
  const [lastScrollPosition, setLastScrollPosition] = useState(0);

  // Function to check if user is near bottom of messages
  const isNearBottom = () => {
    if (messageContainerRef.current) {
      const container = messageContainerRef.current;
      const threshold = 100; // pixels from bottom
      return container.scrollHeight - container.scrollTop - container.clientHeight < threshold;
    }
    return true;
  };

  // Handle scroll events
  const handleScroll = () => {
    if (messageContainerRef.current) {
      const isBottom = isNearBottom();
      setAutoScroll(isBottom);
      setLastScrollPosition(messageContainerRef.current.scrollTop);
    }
  };

  // Scroll to bottom if autoScroll is enabled
  useEffect(() => {
    if (autoScroll && messageContainerRef.current) {
      messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
    }
  }, [messages, isLoading, autoScroll]);

  // Reset scroll state when changing agents
  useEffect(() => {
    setAutoScroll(true);
    setLastScrollPosition(0);
    if (messageContainerRef.current) {
      messageContainerRef.current.scrollTop = 0;
    }
  }, [agentName]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const message = input.trim();
    setInput('');
    setAutoScroll(true);
    await onSendMessage(message);
  };

  const handleFileUpload = async (file: File) => {
    if (!file) return;
    
    // Check if file is an image
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file');
      return;
    }
    
    setAutoScroll(true);
    await onSendMessage(file);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    await handleFileUpload(file);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleFileInputChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      await handleFileUpload(file);
    }
  };

  const handleExampleClick = (prompt: string) => {
    setInput(prompt);
    setAutoScroll(true);
  };

  // Format agent name for display
  const formatAgentName = (name: string): string => {
    if (name.startsWith('digital_transform_')) {
      return name.split('_')
        .slice(2)
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
    }
    return name;
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      {/* Chat Header */}
      <div className="p-6 border-b border-[#e0f2f1]">
        <h2 className="text-2xl font-manrope font-light text-[#6A1B9A]">{formatAgentName(agentName)}</h2>
      </div>

      {/* Messages */}
      <div 
        ref={messageContainerRef}
        className={`flex-1 overflow-y-auto p-6 space-y-6 ${isDragging ? 'bg-[#e0f2f1] bg-opacity-50' : ''}`}
        onScroll={handleScroll}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        {messages.length === 0 && (
          <div className="text-center text-gray-600 py-8">
            <h3 className="text-xl font-manrope font-light mb-4">Start a conversation with {formatAgentName(agentName)}</h3>
            {agentName === 'digital_transform_datadetective' && (
              <div className="mb-6">
                <p className="mb-2 font-manrope font-light">Upload a chart or data visualization:</p>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="px-4 py-2 bg-[#e0f2f1] hover:bg-[#00897B] hover:text-white rounded-lg transition-all duration-300 font-manrope font-light"
                >
                  Choose File
                </button>
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileInputChange}
                  accept="image/*"
                  className="hidden"
                />
                <p className="mt-2 text-sm text-gray-500">or drag and drop an image here</p>
              </div>
            )}
            <p className="mb-6 font-manrope font-light">Try these example prompts:</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {examplePrompts.map((prompt, index) => (
                <button
                  key={index}
                  onClick={() => handleExampleClick(prompt)}
                  className="p-4 text-left bg-[#e0f2f1] hover:bg-[#00897B] hover:text-white rounded-lg transition-all duration-300 font-manrope font-light"
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        )}
        
        {messages.map((message, index) => (
          <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[80%] rounded-lg p-4 font-manrope font-light ${
                message.role === 'user' 
                  ? 'bg-[#6A1B9A] text-white'
                  : 'bg-[#e0f2f1] text-gray-800'
              }`}
            >
              {message.role === 'user' ? (
                <p className="whitespace-pre-wrap">{message.content}</p>
              ) : (
                <FormattedMessage content={message.content} />
              )}
            </div>
          </div>
        ))}
        
        {isLoading && <LoadingSpinner />}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="p-6 border-t border-[#e0f2f1]">
        <form onSubmit={handleSubmit} className="flex space-x-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Ask ${formatAgentName(agentName)} something...`}
            className="flex-1 p-2 border border-[#e0f2f1] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#00897B] font-manrope font-light"
            disabled={isLoading}
          />
          {agentName === 'digital_transform_datadetective' && (
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="bg-[#e0f2f1] text-gray-800 px-4 py-2 rounded-lg hover:bg-opacity-90 transition-all font-manrope font-light"
              disabled={isLoading}
            >
              Upload
            </button>
          )}
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="bg-[#6A1B9A] text-white px-4 py-2 rounded-lg hover:bg-opacity-90 transition-all font-manrope font-light disabled:opacity-50"
          >
            Send
          </button>
        </form>
        {!autoScroll && (
          <button
            onClick={() => {
              setAutoScroll(true);
              messageContainerRef.current?.scrollTo({
                top: messageContainerRef.current.scrollHeight,
                behavior: 'smooth'
              });
            }}
            className="fixed bottom-24 right-8 bg-[#00897B] text-white p-2 rounded-full shadow-lg hover:bg-opacity-90 transition-all"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
} 