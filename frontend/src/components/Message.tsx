import React from 'react';
import { Copy, Check } from 'lucide-react';
import { Message as MessageType } from '../types';

interface MessageProps {
  message: MessageType;
}

export const Message: React.FC<MessageProps> = ({ message }) => {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isUser = message.role === 'user';
  
  // Ensure timestamp is a Date object
  const timestamp = message.timestamp instanceof Date 
    ? message.timestamp 
    : new Date(message.timestamp);

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-fade-in`}>
      <div
        className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-lg group relative ${
          isUser
            ? 'bg-blue-500 text-white rounded-br-none'
            : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-bl-none'
        }`}
      >
        <p className="break-words">{message.content}</p>
        <div className="flex items-center justify-between mt-2 text-xs opacity-70">
          <span>{timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
          {!isUser && (
            <button
              onClick={handleCopy}
              className="ml-2 opacity-0 group-hover:opacity-100 transition-opacity"
              title="Copy message"
            >
              {copied ? <Check size={14} /> : <Copy size={14} />}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
