export interface AgentInfo {
  config: {
    name: string;
    description: string;
    tools: string[];
  };
  example_prompts: string[];
} 