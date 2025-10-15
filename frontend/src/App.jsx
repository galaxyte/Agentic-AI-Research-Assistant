import React, { useState, useEffect } from 'react';
import ChatUI from './components/ChatUI';
import { checkHealth } from './api';
import { AlertCircle, CheckCircle2, Loader2 } from 'lucide-react';

function App() {
  const [healthStatus, setHealthStatus] = useState(null);
  const [isCheckingHealth, setIsCheckingHealth] = useState(true);

  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        const health = await checkHealth();
        setHealthStatus(health);
      } catch (error) {
        console.error('Health check failed:', error);
        setHealthStatus({ status: 'error', error: error.message });
      } finally {
        setIsCheckingHealth(false);
      }
    };

    checkBackendHealth();
  }, []);

  if (isCheckingHealth) {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-primary-500 mx-auto mb-4" />
          <p className="text-gray-600">Connecting to backend...</p>
        </div>
      </div>
    );
  }

  if (healthStatus?.status === 'error') {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md">
          <div className="flex items-center gap-3 mb-4">
            <AlertCircle className="w-8 h-8 text-red-500" />
            <h2 className="text-xl font-bold text-gray-900">Backend Connection Failed</h2>
          </div>
          <p className="text-gray-600 mb-4">
            Unable to connect to the backend server. Please ensure:
          </p>
          <ul className="list-disc list-inside text-gray-600 space-y-2 mb-6">
            <li>The backend server is running on port 8000</li>
            <li>All environment variables are configured</li>
            <li>Dependencies are installed</li>
          </ul>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-500 mb-2">Start the backend with:</p>
            <code className="block bg-gray-900 text-gray-100 px-3 py-2 rounded text-sm">
              cd backend && python main.py
            </code>
          </div>
        </div>
      </div>
    );
  }

  // Show warning if some services are not configured
  const showWarning = healthStatus && (
    healthStatus.weaviate === 'disconnected' || 
    healthStatus.openai === 'not configured' || 
    healthStatus.tavily === 'not configured'
  );

  return (
    <div className="relative">
      {showWarning && (
        <div className="absolute top-0 left-0 right-0 bg-amber-500 text-white px-4 py-2 text-sm text-center z-50">
          <AlertCircle className="w-4 h-4 inline mr-2" />
          Some services are not fully configured. Check backend/.env for API keys.
        </div>
      )}
      <div className={showWarning ? 'pt-10' : ''}>
        <ChatUI />
      </div>
    </div>
  );
}

export default App;

