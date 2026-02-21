import React, { useState } from 'react';
import { useChat } from '../hooks/useChat';
import { Send } from 'lucide-react';

export const InputArea: React.FC = () => {
  const { sendMessage, isLoading } = useChat();
  const [input, setInput] = useState('');
  const textareaRef = React.useRef<HTMLTextAreaElement>(null);

  const handleSend = async () => {
    if (input.trim() && !isLoading) {
      await sendMessage(input.trim());
      setInput('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px';
    }
  };

  return (
    <div className="p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
      <div className="flex gap-2">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder="Type your message... (Shift+Enter for new line)"
          className="flex-1 p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows={1}
          style={{ maxHeight: '120px' }}
          disabled={isLoading}
        />
        <button
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
          className="px-4 py-3 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white rounded-lg transition-colors flex items-center gap-2 font-medium"
        >
          {isLoading ? '...' : <><Send size={20} /></>}
        </button>
      </div>
      <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">Press Enter to send, Shift+Enter for new line</p>
    </div>
  );
};
