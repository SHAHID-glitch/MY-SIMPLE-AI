import React from 'react';
import { useChat } from '../hooks/useChat';
import { X } from 'lucide-react';

interface SettingsProps {
  onClose: () => void;
}

export const Settings: React.FC<SettingsProps> = ({ onClose }) => {
  const { conversations, isDarkMode } = useChat();
  
  const totalMessages = conversations.reduce((sum, conv) => sum + conv.messages.length, 0);

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">Settings</h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
          >
            <X size={20} />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Theme */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Theme</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Currently: <span className="font-medium">{isDarkMode ? 'Dark' : 'Light'}</span>
            </p>
          </div>

          {/* Statistics */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Statistics</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Total Conversations</span>
                <span className="font-medium text-gray-900 dark:text-white">{conversations.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Total Messages</span>
                <span className="font-medium text-gray-900 dark:text-white">{totalMessages}</span>
              </div>
            </div>
          </div>

          {/* About */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">About</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Groq AI Assistant v1.0<br />
              Built with React & Tailwind CSS
            </p>
          </div>
        </div>

        <div className="flex gap-2 p-6 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
