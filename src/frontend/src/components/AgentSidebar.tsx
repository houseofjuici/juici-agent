import { AgentInfo } from '@/types/agent';

interface AgentSidebarProps {
  agents: AgentInfo[];
  selectedAgent: string | null;
  onSelectAgent: (agentName: string) => void;
}

// Agent icons mapping
const agentIcons: { [key: string]: string } = {
  // Standard agents
  'FitCoachAI': '🏋️',
  'BlogSmith': '✍️',
  'FunnelBot': '📊',
  'ContractCopilot': '📝',
  // Digital Transform agents
  'digital_transform_analyst': '🔍',
  'digital_transform_architect': '🏗️',
  'digital_transform_designer': '🎨',
  'digital_transform_automator': '⚙️',
  'digital_transform_trainer': '📚',
  'digital_transform_measurer': '📈'
};

// Function to format agent name for display
const formatAgentName = (name: string): string => {
  if (name.startsWith('digital_transform_')) {
    return name.split('_')
      .slice(2) // Skip 'digital' and 'transform'
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
  return name;
};

// Function to group agents by type
const groupAgents = (agents: AgentInfo[]) => {
  const groups: { [key: string]: AgentInfo[] } = {
    'Digital Transform': [],
    'Standard': []
  };

  agents.forEach(agent => {
    if (agent.config.name.startsWith('digital_transform_')) {
      groups['Digital Transform'].push(agent);
    } else {
      groups['Standard'].push(agent);
    }
  });

  return groups;
};

export default function AgentSidebar({ agents, selectedAgent, onSelectAgent }: AgentSidebarProps) {
  const groupedAgents = groupAgents(agents);

  return (
    <div className="w-72 bg-white h-full shadow-lg">
      <div className="p-6 border-b border-[#e0f2f1]">
        <h1 className="text-2xl font-manrope font-light text-[#6A1B9A]">🤖 AI Agents Hub</h1>
      </div>
      
      <div className="p-6">
        <div className="space-y-6">
          {Object.entries(groupedAgents).map(([groupName, groupAgents]) => (
            <div key={groupName}>
              <h2 className="text-lg font-manrope font-medium text-[#00897B] mb-3">{groupName} Agents</h2>
              <div className="space-y-3">
                {groupAgents.map((agent) => (
                  <button
                    key={agent.config.name}
                    onClick={() => onSelectAgent(agent.config.name)}
                    className={`w-full text-left p-4 rounded-lg transition-all duration-300 font-manrope font-light ${
                      selectedAgent === agent.config.name
                        ? 'bg-[#6A1B9A] text-white'
                        : 'hover:bg-[#e0f2f1] text-gray-800'
                    }`}
                  >
                    <div className="flex items-center">
                      <span className="text-2xl mr-2">
                        {agentIcons[agent.config.name] || '🤖'}
                      </span>
                      <div>
                        <div className="text-lg">{formatAgentName(agent.config.name)}</div>
                        <div className="text-sm opacity-80">{agent.config.description}</div>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <div className="p-6 border-t border-[#e0f2f1] mt-auto">
        <div className="text-sm text-gray-600 font-manrope font-light">
          <p>Need help? Check out our</p>
          <a href="#" className="text-[#00897B] hover:underline">Quick Start Guide</a>
        </div>
      </div>
    </div>
  );
} 