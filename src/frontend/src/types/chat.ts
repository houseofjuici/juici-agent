export interface Message {
  role: 'user' | 'assistant';
  content: string;
  id?: number;  // Optional ID for streaming messages
} 