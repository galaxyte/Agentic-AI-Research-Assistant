import React, { useState, useRef, useEffect } from 'react';
import { Send, AlertCircle, RefreshCw, Sparkles } from 'lucide-react';
import MessageBubble from './MessageBubble';
import { createQuery, getStreamUrl } from '../api';

const EXAMPLE_QUERIES = [
  "Explain the latest advancements in AI agent frameworks",
  "What are the benefits of multi-agent systems in AI?",
  "How does LangGraph compare to other agent orchestration tools?",
  "What is the current state of autonomous AI agents?"
];

const ChatUI = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentStage, setCurrentStage] = useState('');
  const messagesEndRef = useRef(null);
  const eventSourceRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Cleanup EventSource on unmount
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);
    setCurrentStage('Initializing...');

    try {
      // Create the query
      const { task_id } = await createQuery(input.trim(), true);

      // Add initial system message
      setMessages(prev => [...prev, {
        role: 'system',
        content: 'Starting research...',
        timestamp: new Date().toISOString(),
        stage: 'Initializing'
      }]);

      // Connect to SSE stream
      const streamUrl = getStreamUrl(task_id);
      const eventSource = new EventSource(streamUrl);
      eventSourceRef.current = eventSource;

      let assistantMessageIndex = null;
      let accumulatedResponse = '';

      eventSource.addEventListener('stage', (event) => {
        const data = JSON.parse(event.data);
        setCurrentStage(data.message);
        
        // Update or add system message with stage
        setMessages(prev => {
          const lastMessage = prev[prev.length - 1];
          if (lastMessage && lastMessage.role === 'system') {
            return [
              ...prev.slice(0, -1),
              {
                ...lastMessage,
                content: data.message,
                stage: data.stage,
                timestamp: data.timestamp
              }
            ];
          } else {
            return [
              ...prev,
              {
                role: 'system',
                content: data.message,
                stage: data.stage,
                timestamp: data.timestamp
              }
            ];
          }
        });
      });

      eventSource.addEventListener('log', (event) => {
        const log = JSON.parse(event.data);
        console.log('Agent log:', log);
      });

      eventSource.addEventListener('status', (event) => {
        const data = JSON.parse(event.data);
        setCurrentStage(data.message);
      });

      eventSource.addEventListener('response', (event) => {
        const data = JSON.parse(event.data);
        accumulatedResponse += data.chunk;

        setMessages(prev => {
          // Remove system message if it's the last one
          const filteredMessages = prev.filter((msg, idx) => 
            !(msg.role === 'system' && idx === prev.length - 1)
          );

          // Find or create assistant message
          if (assistantMessageIndex === null) {
            assistantMessageIndex = filteredMessages.length;
            return [
              ...filteredMessages,
              {
                role: 'assistant',
                content: accumulatedResponse,
                timestamp: new Date().toISOString()
              }
            ];
          } else {
            const updated = [...filteredMessages];
            updated[assistantMessageIndex] = {
              ...updated[assistantMessageIndex],
              content: accumulatedResponse
            };
            return updated;
          }
        });
      });

      eventSource.addEventListener('complete', (event) => {
        const data = JSON.parse(event.data);
        console.log('Research complete:', data);
        
        // Add metadata to the last assistant message
        setMessages(prev => {
          const updated = [...prev];
          if (updated[updated.length - 1]?.role === 'assistant') {
            updated[updated.length - 1].metadata = {
              confidence: data.confidence,
              sources_count: data.sources_count
            };
          }
          return updated;
        });

        setIsLoading(false);
        setCurrentStage('');
        eventSource.close();
        eventSourceRef.current = null;
      });

      eventSource.addEventListener('error', (event) => {
        console.error('SSE error:', event);
        
        let errorMessage = 'An error occurred during research';
        try {
          const data = JSON.parse(event.data);
          errorMessage = data.message || data.error || errorMessage;
        } catch (e) {
          // If parsing fails, use default message
        }

        setError(errorMessage);
        setIsLoading(false);
        setCurrentStage('');
        eventSource.close();
        eventSourceRef.current = null;

        setMessages(prev => [
          ...prev.filter(m => !(m.role === 'system' && prev.indexOf(m) === prev.length - 1)),
          {
            role: 'assistant',
            content: `❌ ${errorMessage}`,
            timestamp: new Date().toISOString()
          }
        ]);
      });

      eventSource.onerror = (err) => {
        console.error('EventSource error:', err);
        setError('Connection to server lost');
        setIsLoading(false);
        setCurrentStage('');
        eventSource.close();
        eventSourceRef.current = null;
      };

    } catch (err) {
      console.error('Error creating query:', err);
      setError(err.message || 'Failed to create query');
      setIsLoading(false);
      setCurrentStage('');
      
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: `❌ Error: ${err.message || 'Failed to create query'}`,
          timestamp: new Date().toISOString()
        }
      ]);
    }
  };

  const handleExampleClick = (query) => {
    setInput(query);
  };

  const handleReset = () => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    setMessages([]);
    setInput('');
    setIsLoading(false);
    setError(null);
    setCurrentStage('');
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <div className="bg-white shadow-md border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Agentic AI Research Assistant
                </h1>
                <p className="text-sm text-gray-500">
                  Multi-agent autonomous research powered by AI
                </p>
              </div>
            </div>
            <button
              onClick={handleReset}
              className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
              title="Reset conversation"
            >
              <RefreshCw className="w-4 h-4" />
              <span className="hidden sm:inline">Reset</span>
            </button>
          </div>
        </div>
      </div>

      {/* Current Stage Indicator */}
      {currentStage && (
        <div className="bg-blue-50 border-b border-blue-200">
          <div className="max-w-5xl mx-auto px-6 py-3">
            <div className="flex items-center gap-2 text-blue-700">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
              <span className="text-sm font-medium">{currentStage}</span>
            </div>
          </div>
        </div>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto scrollbar-thin">
        <div className="max-w-5xl mx-auto px-6 py-6">
          {messages.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Sparkles className="w-10 h-10 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-3">
                Welcome to Agentic AI Research Assistant
              </h2>
              <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
                Ask me anything! I'll search the web, analyze multiple sources, 
                validate facts, and provide you with comprehensive, well-researched answers.
              </p>
              
              {/* Example Queries */}
              <div className="max-w-2xl mx-auto">
                <p className="text-sm text-gray-500 mb-4">Try these example queries:</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {EXAMPLE_QUERIES.map((query, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleExampleClick(query)}
                      className="text-left p-4 bg-white rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-all group"
                    >
                      <p className="text-sm text-gray-700 group-hover:text-primary-700">
                        {query}
                      </p>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <>
              {messages.map((message, idx) => (
                <MessageBubble 
                  key={idx} 
                  message={message}
                  isLoading={isLoading && idx === messages.length - 1 && message.role === 'system'}
                />
              ))}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="bg-red-50 border-t border-red-200">
          <div className="max-w-5xl mx-auto px-6 py-3">
            <div className="flex items-center gap-2 text-red-700">
              <AlertCircle className="w-4 h-4" />
              <span className="text-sm">{error}</span>
              <button
                onClick={() => setError(null)}
                className="ml-auto text-red-700 hover:text-red-900"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 shadow-lg">
        <div className="max-w-5xl mx-auto px-6 py-4">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything..."
              disabled={isLoading}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2 font-medium shadow-md hover:shadow-lg"
            >
              <Send className="w-5 h-5" />
              <span className="hidden sm:inline">
                {isLoading ? 'Researching...' : 'Send'}
              </span>
            </button>
          </form>
          <p className="text-xs text-gray-500 mt-2 text-center">
            Powered by LangGraph • CrewAI • OpenAI • Weaviate
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatUI;

