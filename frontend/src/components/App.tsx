import React, { useState } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { ChatArea } from './ChatArea';
import { InputArea } from './InputArea';
import { Settings } from './Settings';

export const App: React.FC = () => {
  const [showSettings, setShowSettings] = useState(false);

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
      <Header onSettingsClick={() => setShowSettings(true)} />
      
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        
        <div className="flex flex-col flex-1">
          <ChatArea />
          <InputArea />
        </div>
      </div>

      {showSettings && <Settings onClose={() => setShowSettings(false)} />}
    </div>
  );
};

export default App;
