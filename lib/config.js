// Configuration file for environment-specific settings

// Get the base URL for API calls
const getBaseUrl = () => {
  // If running on Vercel in production
  if (process.env.VERCEL_URL) {
    return `https://${process.env.VERCEL_URL}`;
  }
  
  // If we have a custom API URL defined
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  
  // Default to the current origin during runtime or localhost during development
  return typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000';
};

// Create API URL paths
const config = {
  apiUrl: `${getBaseUrl()}/api`,
  routes: {
    agents: '/agents',
    chat: '/chat',
    upload: '/upload'
  }
};

// Helper to get full API URLs
export const getApiUrl = (endpoint) => {
  const base = config.apiUrl;
  const route = config.routes[endpoint] || endpoint;
  return `${base}${route}`;
};

export default config; 