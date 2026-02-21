import React, { useEffect, useRef } from 'react';
import { useChat } from '../hooks/useChat';
import { Message } from './Message';
import { AlertCircle, Loader } from 'lucide-react';

export const ChatArea: React.FC = () => {
  const { currentConversation, isLoading, error } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentConversation?.messages]);

  if (!currentConversation) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <p className="text-gray-500 dark:text-gray-400">No conversation selected</p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 bg-gradient-to-b from-transparent to-blue-50 dark:to-gray-800">
      {currentConversation.messages.length === 0 ? (
        <div className="flex items-center justify-center h-full">
          <div className="text-center">
            <div className="text-5xl mb-4">💬</div>
            <p className="text-gray-500 dark:text-gray-400">Start a conversation</p>
          </div>
        </div>
      ) : (
        <>
          {currentConversation.messages.map(message => (
            <Message key={message.id} message={message} />
          ))}
          
          {error && (
            <div className="flex gap-2 mb-4 p-3 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 rounded-lg">
              <AlertCircle size={20} className="flex-shrink-0" />
              <p className="text-sm">{error}</p>
            </div>
          )}

          {isLoading && (
            <div className="flex gap-2 items-center mb-4 p-3 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-lg">
              <Loader size={20} className="animate-spin flex-shrink-0" />
              <p className="text-sm">AI is thinking...</p>
            </div>
          )}

          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  );
};
