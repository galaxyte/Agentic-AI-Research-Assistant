import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { User, Bot, Loader2 } from 'lucide-react';

const MessageBubble = ({ message, isLoading = false }) => {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';

  return (
    <div className={`chat-message ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex gap-3 max-w-[85%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
          isUser 
            ? 'bg-primary-500' 
            : isSystem 
            ? 'bg-amber-500' 
            : 'bg-gradient-to-br from-purple-500 to-pink-500'
        }`}>
          {isUser ? (
            <User className="w-6 h-6 text-white" />
          ) : (
            <Bot className="w-6 h-6 text-white" />
          )}
        </div>

        {/* Message Content */}
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          {/* Role Label */}
          <div className="text-xs text-gray-500 mb-1 px-1">
            {isUser ? 'You' : isSystem ? 'System' : 'AI Assistant'}
          </div>

          {/* Message Bubble */}
          <div className={`rounded-2xl px-4 py-3 ${
            isUser 
              ? 'bg-primary-500 text-white' 
              : isSystem
              ? 'bg-amber-50 text-amber-900 border border-amber-200'
              : 'bg-white text-gray-900 shadow-md border border-gray-100'
          } ${isUser ? 'rounded-tr-sm' : 'rounded-tl-sm'}`}>
            {isLoading ? (
              <div className="flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span className="text-sm">{message.content}</span>
              </div>
            ) : (
              <div className={`markdown-content ${isUser ? 'text-white' : ''}`}>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {message.content}
                </ReactMarkdown>
              </div>
            )}
          </div>

          {/* Timestamp */}
          {message.timestamp && (
            <div className="text-xs text-gray-400 mt-1 px-1">
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          )}

          {/* Agent Stage Indicator */}
          {message.stage && (
            <div className="text-xs text-gray-500 mt-1 px-1 flex items-center gap-1">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              {message.stage}
            </div>
          )}

          {/* Metadata */}
          {message.metadata && (
            <div className="text-xs text-gray-500 mt-2 px-1 space-y-1">
              {message.metadata.confidence && (
                <div className="flex items-center gap-2">
                  <span>Confidence:</span>
                  <div className="flex-1 bg-gray-200 rounded-full h-2 max-w-[100px]">
                    <div 
                      className="bg-green-500 h-2 rounded-full"
                      style={{ width: `${message.metadata.confidence * 100}%` }}
                    ></div>
                  </div>
                  <span>{(message.metadata.confidence * 100).toFixed(0)}%</span>
                </div>
              )}
              {message.metadata.sources_count && (
                <div>📚 {message.metadata.sources_count} sources analyzed</div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;

