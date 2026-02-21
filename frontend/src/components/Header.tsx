import React from 'react';
import { useChat } from '../hooks/useChat';
import { Moon, Sun, Trash2, Settings, Zap } from 'lucide-react';

interface HeaderProps {
  onSettingsClick?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onSettingsClick }) => {
  const { isDarkMode, toggleTheme, apiStatus, clearHistory } = useChat();

  const statusColor = 
    apiStatus === 'connected' ? 'text-green-500' :
    apiStatus === 'disconnected' ? 'text-red-500' :
    'text-yellow-500';

  return (
    <header className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 shadow-lg">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="text-3xl">🤖</div>
          <div>
            <h1 className="text-2xl font-bold">Groq AI Assistant</h1>
            <p className="text-sm opacity-90">Powered by Groq API</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          {/* API Status */}
          <div className="flex items-center gap-2 text-sm">
            <Zap size={18} className={statusColor} />
            <span className="hidden sm:inline">{apiStatus === 'connected' ? 'Connected' : 'Disconnected'}</span>
          </div>

          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 hover:bg-white/20 rounded-lg transition-colors"
            title="Toggle theme"
          >
            {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
          </button>

          {/* Clear History */}
          <button
            onClick={() => {
              if (window.confirm('Clear all conversations?')) {
                clearHistory();
              }
            }}
            className="p-2 hover:bg-white/20 rounded-lg transition-colors"
            title="Clear history"
          >
            <Trash2 size={20} />
          </button>

          {/* Settings */}
          <button
            onClick={onSettingsClick}
            className="p-2 hover:bg-white/20 rounded-lg transition-colors"
            title="Settings"
          >
            <Settings size={20} />
          </button>
        </div>
      </div>
    </header>
  );
};
